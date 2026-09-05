"""Deterministic Project Status deck assembly.

Input: a base deck (the previous week's deck, or the KCG template) and an approved-values
document. Output: deck bytes plus a manifest. The model is never involved here.

Content rules carried from Ethan Sweeney's weekly-status-deck skill: New Date governs, drop a
leading 'Build:' prefix, cap bulleted text by wrapped-line budget (about 48 characters per line,
about 14 lines), and phrase an empty risks table as 'No open risks or issues outstanding.'
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from datetime import date, datetime
from typing import Optional

from pptx import Presentation
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml.ns import qn

from .status import AssessmentStatus, derive_milestone_status, rollup_overall, status_period, variance_days

SERVICE_VERSION = "0.2.0"
DEFAULT_TEMPLATE = Path(__file__).parent / "templates" / "KCG_Status_Template.pptx"
MAX_APPROVED_BYTES = 524_288
LINE_CHARS = 48
LINE_BUDGET = 14
MILESTONE_ROWS = 10
RAID_ROWS = 3
EMPTY_RISKS_TEXT = "No open risks or issues outstanding."

STATUS_THEME_COLOR = {
    "Green": MSO_THEME_COLOR.ACCENT_1,
    "Yellow": MSO_THEME_COLOR.ACCENT_5,
    "Red": MSO_THEME_COLOR.ACCENT_6,
    "Unknown": MSO_THEME_COLOR.BACKGROUND_2,
    "Not assessed": MSO_THEME_COLOR.BACKGROUND_2,
}

OVALS = {"overall": "Oval 22", "scope_schedule": "Oval 1", "resources": "Oval 11", "data": "Oval 12"}


class ApprovedValuesError(ValueError):
    """The document is not fit to build from. The message is for the reviewer."""


@dataclass
class Manifest:
    filename: str
    size_bytes: int = 0
    sha256: str = ""
    warnings: list[str] = field(default_factory=list)
    service_version: str = SERVICE_VERSION
    approved_values_sha256: str = ""

    def to_dict(self) -> dict:
        return self.__dict__.copy()


# --- helpers ---------------------------------------------------------------

def _d(value: Optional[str]) -> Optional[date]:
    return date.fromisoformat(value[:10]) if value else None


def short_date(value: Optional[str]) -> str:
    """m/d as the template shows it. Empty for None."""
    d = _d(value)
    return f"{d.month}/{d.day}" if d else ""


def long_date(value: str) -> str:
    d = _d(value)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def deck_filename(client: str, as_of: str) -> str:
    """Observed convention: KCG_Status DoTERRA 8-26-2026.pptx"""
    d = _d(as_of)
    return f"KCG_Status {client} {d.month}-{d.day}-{d.year}.pptx"


def wrapped_lines(text: str, chars: int = LINE_CHARS) -> int:
    return max(1, math.ceil(len(text) / chars))


def fit_to_budget(items: list[str], budget: int = LINE_BUDGET, chars: int = LINE_CHARS) -> tuple[list[str], list[str]]:
    """Keep items in order until the wrapped-line budget is spent. Returns (kept, dropped)."""
    kept, used = [], 0
    for i, it in enumerate(items):
        n = wrapped_lines(it, chars)
        if used + n > budget:
            return kept, items[i:]
        kept.append(it)
        used += n
    return kept, []


def set_text(shape_or_cell, text: str) -> None:
    """Replace text while keeping the first run's formatting."""
    tf = shape_or_cell.text_frame
    paras = tf.paragraphs
    first = paras[0]
    runs = first.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        first.add_run().text = text
    for extra in paras[1:]:
        extra._p.getparent().remove(extra._p)
    for br in first._p.findall(qn("a:br")):
        first._p.remove(br)


def set_bullets(cell, items: list[str]) -> None:
    """Rewrite a cell as one bulleted paragraph per item, cloning the first paragraph's formatting.
    An empty list leaves one empty paragraph so the cell keeps its formatting."""
    tf = cell.text_frame
    template = copy.deepcopy(tf.paragraphs[0]._p)
    tx_body = tf._txBody
    for p in list(tf.paragraphs):
        tx_body.remove(p._p)
    for it in items or [""]:
        p = copy.deepcopy(template)
        for tag in ("a:br", "a:fld"):
            for el in p.findall(qn(tag)):
                p.remove(el)
        runs = p.findall(qn("a:r"))
        if runs:
            for r in runs[1:]:
                p.remove(r)
            runs[0].find(qn("a:t")).text = it
        else:
            r = copy.deepcopy(template.find(qn("a:r"))) if template.find(qn("a:r")) is not None else None
            if r is None:
                from lxml import etree
                r = etree.SubElement(p, qn("a:r"))
                etree.SubElement(r, qn("a:t"))
            r.find(qn("a:t")).text = it
            end = p.find(qn("a:endParaRPr"))
            if end is not None:
                end.addprevious(r)
            else:
                p.append(r)
        tx_body.append(p)


def shape_by_name(slide, name: str):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise ApprovedValuesError(f"The base deck has no shape named {name!r} on the Project Status slide. Check the template version.")


def find_status_slide(prs):
    for s in prs.slides:
        names = {sh.name for sh in s.shapes}
        if {"Table 14", "Table 16", "Table 9"} <= names:
            return s
    raise ApprovedValuesError("No Project Status slide found in the base deck.")


# --- validation --------------------------------------------------------------

def validate_approved_values(av: dict) -> None:
    """Refuse documents that are drafts, oversized, or whose derived fields disagree with their inputs."""
    raw = json.dumps(av, separators=(",", ":")).encode("utf-8")
    if len(raw) > MAX_APPROVED_BYTES:
        raise ApprovedValuesError(f"Approved values are {len(raw):,} bytes; the limit is {MAX_APPROVED_BYTES:,}.")
    ap = av.get("approval") or {}
    for k in ("reviewer_name", "reviewer_email", "approved_at", "version"):
        if not ap.get(k):
            raise ApprovedValuesError("This document has no named approval. Approve it in the workspace before generating a deck.")
    as_of = av["as_of"]
    for m in av.get("milestones", []):
        expected = derive_milestone_status(m["completed"], m.get("original_date"), m.get("new_date"), as_of).value
        if m["status"] != expected:
            raise ApprovedValuesError(f"Milestone {m['name']!r} carries status {m['status']!r} but the rule derives {expected!r}.")
        if m.get("variance_days") != variance_days(m.get("original_date"), m.get("new_date")):
            raise ApprovedValuesError(f"Milestone {m['name']!r} variance does not match its dates.")
    a = av["assessments"]
    expected_overall = rollup_overall([a["scope_schedule"]["status"], a["resources"]["status"], a["data"]["status"]]).value
    if av["overall"]["status"] != expected_overall:
        raise ApprovedValuesError(f"Overall status {av['overall']['status']!r} does not match the worst-of rollup {expected_overall!r}.")
    p = status_period(as_of)
    if av["period"]["start"] != p.start.isoformat() or av["period"]["end"] != p.end.isoformat():
        raise ApprovedValuesError("The status period does not match the as-of date's work week.")


# --- build -------------------------------------------------------------------

def default_base_deck() -> bytes:
    """The bundled, optimized KCG status template. Used when no previous deck is supplied."""
    return DEFAULT_TEMPLATE.read_bytes()


def build_deck(base_pptx: Optional[bytes], av: dict) -> tuple[bytes, Manifest]:
    if base_pptx is None:
        base_pptx = default_base_deck()
    validate_approved_values(av)
    manifest = Manifest(filename=deck_filename(av["engagement"]["client"], av["as_of"]))
    manifest.approved_values_sha256 = hashlib.sha256(json.dumps(av, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    prs = Presentation(io.BytesIO(base_pptx))

    # Slide 1 date
    title = prs.slides[0]
    for sh in title.shapes:
        if sh.name == "Text Placeholder 2" and sh.has_text_frame:
            set_text(sh, long_date(av["as_of"]))

    s = find_status_slide(prs)

    # Table 8: project info
    t8 = shape_by_name(s, "Table 8").table
    set_text(t8.cell(0, 0), f"Project Name: {av['engagement']['project_name']}")
    set_text(t8.cell(1, 1), ", ".join(av.get("project_managers") or []) or " ")
    set_text(t8.cell(2, 1), f"Week of {short_date(av['period']['start'])}")

    # Table 9 + ovals: statuses with text cues
    t9 = shape_by_name(s, "Table 9").table
    overall = av["overall"]["status"]
    set_text(t9.cell(0, 0), f"Overall Status: {overall}")
    a = av["assessments"]
    for row, key in ((1, "scope_schedule"), (2, "resources"), (3, "data")):
        set_text(t9.cell(row, 1), a[key]["status"])
    for key, status in (("overall", overall), ("scope_schedule", a["scope_schedule"]["status"]),
                        ("resources", a["resources"]["status"]), ("data", a["data"]["status"])):
        oval = shape_by_name(s, OVALS[key])
        oval.fill.solid()
        oval.fill.fore_color.theme_color = STATUS_THEME_COLOR[status]

    # Table 14: milestones
    t14 = shape_by_name(s, "Table 14").table
    ms = av.get("milestones", [])
    if len(ms) > MILESTONE_ROWS:
        manifest.warnings.append(f"{len(ms)} milestones supplied; the slide shows {MILESTONE_ROWS}. The last {len(ms) - MILESTONE_ROWS} were left off.")
    for i in range(MILESTONE_ROWS):
        r = i + 1
        if i < len(ms):
            m = ms[i]
            set_text(t14.cell(r, 0), m["name"])
            set_text(t14.cell(r, 1), short_date(m.get("original_date")))
            set_text(t14.cell(r, 2), short_date(m.get("new_date") or m.get("original_date")))
            set_text(t14.cell(r, 3), m["status"])
        else:
            for c in range(4):
                set_text(t14.cell(r, c), "")

    # Table 16: accomplishments and planned activities, budgeted
    t16 = shape_by_name(s, "Table 16").table
    for col, key in ((0, "accomplishments"), (1, "planned_activities")):
        kept, dropped = fit_to_budget(av.get(key, []))
        if dropped:
            manifest.warnings.append(f"{len(dropped)} {key.replace('_', ' ')} item(s) did not fit the {LINE_BUDGET}-line budget and were left off.")
        set_bullets(t16.cell(1, col), kept)

    # Table 19: RAID
    t19 = shape_by_name(s, "Table 19").table
    raid = av.get("raid", [])
    if len(raid) > RAID_ROWS:
        manifest.warnings.append(f"{len(raid)} RAID items supplied; the slide shows {RAID_ROWS}. The last {len(raid) - RAID_ROWS} were left off.")
    if not raid:
        set_text(t19.cell(1, 0), "")
        set_text(t19.cell(1, 1), EMPTY_RISKS_TEXT)
        set_text(t19.cell(1, 2), "")
        set_text(t19.cell(1, 3), "")
        for r in range(2, RAID_ROWS + 1):
            for c in range(4):
                set_text(t19.cell(r, c), "")
    else:
        for i in range(RAID_ROWS):
            r = i + 1
            if i < len(raid):
                it = raid[i]
                label = it["type"] + (f" ({it['priority']})" if it.get("priority") else "")
                set_text(t19.cell(r, 0), label)
                set_text(t19.cell(r, 1), it["description"])
                set_text(t19.cell(r, 2), it.get("mitigation", ""))
                set_text(t19.cell(r, 3), it.get("status", ""))
            else:
                for c in range(4):
                    set_text(t19.cell(r, c), "")

    out = io.BytesIO()
    prs.save(out)
    data = out.getvalue()
    manifest.size_bytes = len(data)
    manifest.sha256 = hashlib.sha256(data).hexdigest()
    return data, manifest
