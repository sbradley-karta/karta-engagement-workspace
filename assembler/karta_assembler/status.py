"""Deterministic Weekly Status logic.

Everything here is derived in code and tested. The language model never sets these values.
Rules are documented in docs/contracts/README.md and must change there first.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Iterable, Optional


class MilestoneStatus(str, Enum):
    COMPLETE = "Complete"
    ON_TRACK = "On Track"
    AT_RISK = "At Risk"
    OFF_TRACK = "Off Track"
    UNKNOWN = "Unknown"


class AssessmentStatus(str, Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"
    UNKNOWN = "Unknown"
    NOT_ASSESSED = "Not assessed"


def _to_date(value: Optional[str | date]) -> Optional[date]:
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def governing_date(original_date: Optional[str | date], new_date: Optional[str | date]) -> Optional[date]:
    """New Date governs. Falls back to the original date. None when neither exists."""
    nd = _to_date(new_date)
    return nd if nd is not None else _to_date(original_date)


def variance_days(original_date: Optional[str | date], new_date: Optional[str | date]) -> Optional[int]:
    """Days the approved new date sits after the original. None unless both exist."""
    od, nd = _to_date(original_date), _to_date(new_date)
    if od is None or nd is None:
        return None
    return (nd - od).days


def derive_milestone_status(
    completed: bool,
    original_date: Optional[str | date],
    new_date: Optional[str | date],
    as_of: str | date,
) -> MilestoneStatus:
    """Rule, evaluated in order:
    completed -> Complete; no dates -> Unknown; governing date before as_of -> Off Track;
    new date later than original -> At Risk; otherwise On Track.
    """
    if completed:
        return MilestoneStatus.COMPLETE
    gd = governing_date(original_date, new_date)
    if gd is None:
        return MilestoneStatus.UNKNOWN
    today = _to_date(as_of)
    if gd < today:
        return MilestoneStatus.OFF_TRACK
    v = variance_days(original_date, new_date)
    if v is not None and v > 0:
        return MilestoneStatus.AT_RISK
    return MilestoneStatus.ON_TRACK


_ROLLUP_RANK = {
    AssessmentStatus.RED: 4,
    AssessmentStatus.YELLOW: 3,
    AssessmentStatus.UNKNOWN: 2,
    AssessmentStatus.NOT_ASSESSED: 2,
    AssessmentStatus.GREEN: 1,
}


def rollup_overall(statuses: Iterable[AssessmentStatus | str]) -> AssessmentStatus:
    """Worst-of rollup. Any Red -> Red; else any Yellow -> Yellow; else any Unknown or
    Not assessed -> Unknown; else Green. An empty input is Not assessed, never Green."""
    items = [AssessmentStatus(s) for s in statuses]
    if not items:
        return AssessmentStatus.NOT_ASSESSED
    worst = max(items, key=lambda s: _ROLLUP_RANK[s])
    if worst in (AssessmentStatus.UNKNOWN, AssessmentStatus.NOT_ASSESSED):
        return AssessmentStatus.UNKNOWN
    return worst


@dataclass(frozen=True)
class Period:
    start: date
    end: date

    @property
    def label(self) -> str:
        if self.start.year == self.end.year and self.start.month == self.end.month:
            return f"{self.start.strftime('%B')} {self.start.day} to {self.end.day}, {self.end.year}"
        return f"{self.start.strftime('%B')} {self.start.day} to {self.end.strftime('%B')} {self.end.day}, {self.end.year}"


def status_period(as_of: str | date) -> Period:
    """Monday through Friday of the work week containing as_of. A weekend as_of belongs to the week just ended."""
    d = _to_date(as_of)
    monday = d - timedelta(days=d.weekday())
    return Period(start=monday, end=monday + timedelta(days=4))


def milestone_from_asana(task: dict, as_of: str | date, new_date: Optional[str] = None) -> dict:
    """Map one Asana task (observed shape: due_on populated, start_on usually null) to a milestone
    record with derived fields. `new_date` is the approved re-plan date from the reviewer or the
    previous deck; Asana carries only one date, so the original is due_on."""
    original = task.get("due_on") or task.get("start_on")
    completed = bool(task.get("completed"))
    status = derive_milestone_status(completed, original, new_date, as_of)
    return {
        "name": strip_build_prefix(task.get("name", "")),
        "completed": completed,
        "completed_at": task.get("completed_at"),
        "original_date": original,
        "new_date": new_date,
        "status": status.value,
        "variance_days": variance_days(original, new_date),
        "source": {"system": "asana", "id": str(task.get("gid", ""))},
    }


def strip_build_prefix(name: str) -> str:
    """Content rule carried from the existing skill: drop a leading 'Build:' prefix from milestone names."""
    n = name.strip()
    return n[6:].strip() if n.lower().startswith("build:") else n


def in_sections(task: dict, section_names: Iterable[str]) -> bool:
    """Client-side section filter. Asana's sections_any filter was observed to be unreliable."""
    wanted = {s.lower() for s in section_names}
    for m in task.get("memberships") or []:
        sec = (m.get("section") or {}).get("name", "")
        if sec.lower() in wanted:
            return True
    return False
