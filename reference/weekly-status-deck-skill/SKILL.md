---
name: weekly-status-deck
description: Build or update a Karta Consulting Group client "Project Status" PowerPoint deck — Title, Project Goal & Objectives, Timeline & Resourcing, and a data-driven Project Status slide — sourced from that client's Design Document, Asana project, RAID log, and recent meeting notes. Draft the Project Status fields into a review artifact first, then assemble the deck only after the user finalizes. Use whenever the user asks to build/update/draft a weekly (or periodic) status deck, status report, or steer co deck for a named client.
---

# weekly-status-deck (browser build)

**This is the claude.ai / browser-sandbox variant of the desktop weekly-status-deck
skill.** The original lives at `C:\Users\EthanSweeney\SWE\Current Projects\Weekly
Status\skills\weekly-status-deck\SKILL.md` and builds the deck via PowerShell +
PowerPoint COM automation — that only works because it runs on Ethan's own
Windows machine with PowerPoint installed and direct filesystem access to his
synced OneDrive drive. None of that exists in claude.ai's sandbox: no
PowerShell, no COM, no PowerPoint application, no local drive letters. This
version rebuilds the same slide-editing logic on `python-pptx` instead, and
sources/delivers files through whatever connectors or chat-upload/download the
runtime actually has, instead of raw filesystem paths.

**Status: first draft, not yet validated against a real claude.ai session.**
The machine this was authored on has no working Python install, so none of the
python-pptx code below has been run end-to-end — it's written against
documented python-pptx behavior and known workarounds, not verified against
this specific template file. Treat the first real run as a validation pass,
not a rubber stamp: read every gotcha comment in `scripts/pptx_helpers.py`
before trusting its output, and do the verification steps at the bottom of
this file before calling a build done. If something in this file turns out to
be wrong once actually run, fix it here (and note the fix) rather than
special-casing around it silently — the next person to use this needs the
corrected version, not a one-off patch.

The one thing that has NOT changed from the desktop version is the *content*
logic — what goes on each slide, how milestones are sourced, how the Project
Status fields are drafted, the ~14-line accomplishments cap, the empty-risks
phrasing, etc. That's all reused as-is below. Only the mechanics of opening,
editing, and delivering the .pptx file are rewritten.

## Trigger and required input

The client name is the only thing strictly required — every path below derives
from it. If ambiguous, ask. You'll also want to know whether this is the
client's **first** status deck or an **update** to an existing one — look for
an existing `KCG_<Client> Status Report.pptx`-pattern file (see Source files)
before assuming either way.

## Source files — how to actually get them in a browser session

The desktop skill reads these off a mapped OneDrive drive letter by fixed
path. In claude.ai there is no guaranteed direct filesystem access to
SharePoint, so get each source file the first way below that's actually
available in the running session, in this preference order:

1. **A file the user already attached to the conversation.** Cheapest, most
   reliable, works for every account regardless of what's connected — if the
   user (or their manager) drops the Template, Design Document, or previous
   status deck into the chat, use that directly.
2. **A connected SharePoint tool**, if the account has one. This session (the
   one this file was authored in) has `sharepoint_search` /
   `sharepoint_upload_file` / related tools from an MCP connector — search for
   the file by name pattern, then read/download it. **Verify the actual tool
   names available in whatever session runs this** — connector tool names can
   differ by account or connector version; don't assume these exact names
   carry over. If no SharePoint-shaped tool is available, fall through to (3).
3. **Ask the user to upload it.** If neither (1) nor (2) gets you the file,
   say plainly which file is missing (Template / Design Document / previous
   deck) and ask the user to attach it — don't guess at content or invent
   placeholder data.

The three files needed, same as the desktop version:

1. **Template**: `KCG_Status Template.pptx` (Karta's firmwide status deck template).
2. **Design Document**: `KCG_Design Document_<Client>.pptx`, for a first build.
3. **Previous deck** (update path, read-only source): filename pattern
   `<YYYYMMDD> KCG_<Client> Status Report.pptx`, most recent by date.

**Output delivery:** same rule as the desktop skill, for the same reason —
never assume you can write the finished deck back into a client's shared
folder on the user's behalf. Deliver the built .pptx as a file the user can
download from the conversation. If a SharePoint upload tool is available and
the user explicitly asks you to place it back into their shared folder, that's
fine to do — but ask first (uploading/overwriting a file in shared storage is
not something to do by default), exactly like the "explicit permission
required" rule for anything that touches shared state.

## Why python-pptx, and what it can't do that COM could

No PowerShell/COM in this sandbox, but there should be a real Python with
`python-pptx` importable (pip install it if not: `pip install python-pptx`).
Dot-source, so to speak, the shared helpers:

```python
import sys
sys.path.insert(0, "/path/to/this/skill/scripts")  # wherever the uploaded skill's files land in the sandbox
from pptx_helpers import (
    find_shape_by_exact_text, get_leaf_shapes_containing_text,
    replace_text_in_run, set_cell_text, get_cell_text_frame,
    rewrite_bulleted_cell, copy_slide_from_external,
    add_position_marker, set_picture_size_preserve_aspect,
    try_export_slide_png,
)
```

Two real gaps vs. the desktop skill, both documented in detail in the helper
module's docstrings — read them before you hit either case:

- **Cross-presentation slide copy.** COM's `Slides.Item(n).Copy()` /
  `Slides.Paste()` has no python-pptx equivalent; `copy_slide_from_external`
  reimplements it via direct XML copying, including re-linking picture
  relationships into the destination package. This is the single riskiest
  piece of this rewrite — verify it actually produces a correct slide
  (open the result, check every shape rendered, not just that it didn't
  throw) before trusting it on a real client deck.
- **No slide-to-PNG export.** COM's `.Export()` always works because real
  PowerPoint is present. python-pptx has no equivalent; `try_export_slide_png`
  shells out to LibreOffice headless conversion as a best effort, which may
  not be installed in a given sandbox. If it's not available, fall back to
  structural verification (see "Verification before calling it done") and
  say plainly that visual QA wasn't possible, rather than skipping
  verification silently or claiming a visual check that didn't happen.

There's no "synced file co-authoring hang" risk here the way there was on
Ethan's OneDrive-synced drive (see the desktop skill's note on that) — the
sandbox filesystem is local and ephemeral, not sync-contended. Still work on
one local copy per build and don't reopen a file you're mid-edit on in a
second process, as ordinary good practice, but the specific PowerPoint-hang
failure mode that section documents doesn't apply here.

## The 4-slide treatment plan

Identical to the desktop skill:

| # | Slide | Source | Treatment |
|---|---|---|---|
| 1 | Title | Template (first build) or previous deck (update) | Manual — see below |
| 2 | Project Goal & Objectives | Design Document (first build) or previous deck (update) | Whole-cloth copy via `copy_slide_from_external`, strip internal artifacts |
| 3 | Timeline & Resourcing | Design Document (first build) or previous deck (update) | Whole-cloth copy, strip internal artifacts, position marker — see below |
| 4 | Project Status | Live data (Asana, RAID log, meeting notes) via review artifact | Rebuilt every time — see below |

### Finding slides 2 and 3 — don't trust slide numbers

Same rule as the desktop skill: design docs vary in length per client: scan
slide titles, don't assume a fixed index.

- Goals slide: title text is (near-)exactly `Project Goal & Objectives`.
  `find_shape_by_exact_text(slide, "Project Goal & Objectives")` against each
  slide's title placeholder, or just check `slide.shapes.title.text` if the
  layout has one.
- Timeline slide: title contains `Timeline` and `Resourc` — exact wording
  varies client to client.

Once found, copy whole-cloth with `copy_slide_from_external` — these slides
already carry the client's real logo and content.

**Strip stray internal artifacts before finalizing.** Same as the desktop
skill — use `get_leaf_shapes_containing_text` for anything that looks like an
internal reviewer tag or name (Cinemark's design doc had a highlighted
"Tyler" textbox) and delete it (`shape._element.getparent().remove(shape._element)`).
Check the copied slide's full shape list and text dump, since there's no
guaranteed PNG export to eyeball it the way the desktop skill can.

### Slide 1 — Title

Same content rule as the desktop skill:
- Set the title placeholder to the project's descriptive name, pulled from the
  Design Document's opening sentence.
- Set the date placeholder to an ordinal-suffix date ("August 20th, 2026") —
  default to today's date, or a Weekly Status meeting date found via a
  connected calendar tool if one's available, same reasoning as the desktop
  skill (a deck isn't always built the day before the meeting).
- Replace the logo: `set_picture_size_preserve_aspect` at the original
  placeholder's footprint, vertically centered on its old box.

**The Project Status slide (slide 4) has its own separate logo placeholder** —
same as the desktop skill's note. Don't assume slide 1 is the only place a
placeholder logo lives.

### Finding the client's real logo

Same as the desktop skill: the Design Document's Goals slide carries the real
logo, usually top-right, small. Export it (or just re-check its rendered
bounds/position) before trusting it's the right image — without COM's
`shape.Export()`, the practical check is: read the picture's dimensions and
position, and cross-reference against what the desktop skill's build notes say
to expect for this client, rather than eyeballing a raster export.

### New Date, not Orig. Date

Same rule, verbatim: wherever a slipped Milestones table (Orig./New Date
columns) exists, always read New Date, never Orig. Date, for status inference
and Timeline positioning.

### Slide 3 — Timeline & Resourcing position marker

Same rule as the desktop skill: automate the "you are here" marker on every
build, no need to ask first. Confirmed shape (from the desktop skill's direct
inspection of a real hand-edited deck): a vertical dashed connector, template
"Yellow" color, spanning from the header table's bottom edge to the bottom of
the lowest phase-bar rectangle, positioned at the horizontal midpoint of
whichever week column's date range contains today.

```python
# left/top/bottom are the same landmark shapes the desktop skill uses:
# top = header_table.top + header_table.height
# bottom = lowest_phase_bar.top + lowest_phase_bar.height
# left = week_column_left + week_column_width / 2  (rough placement is fine)
add_position_marker(slide3, left_emu, top_emu, bottom_emu)
```

Same scope note as the desktop skill on a Go-Live slip (append-only week
extension) — narrow, rare, build it against the real slide when it comes up
rather than generically now.

## Slide 4 — Project Status

### Step 1: draft in a review artifact, don't write to the deck directly

**Identical data-sourcing rules to the desktop skill — reuse verbatim, not
re-derived:**

- **Milestones** — from the client's Asana project sections (Kickoff/
  Foundations/Build/UAT/Deploy), one row per task, `start_on` as the date,
  status inferred from completion + dates relative to today (cross-check
  against the RAID log for anything the Asana status field hasn't caught up
  with yet — e.g. a task still showing "Off Track" after the RAID log records
  its sign-off).
- **Project Manager(s)** — blank on first build; carry forward from the
  previous deck on an update.
- **Status Period** — the current work week, computed directly.
- **Overall Status** — defaults Green; auto-derives as the worst of Scope &
  Schedule / Resources / Data, not an independent selector.
- **Accomplishments / Planned Activities** — Asana completions + meeting notes
  (backward-looking), upcoming calendar events for Planned Activities
  (forward-looking). Cap by estimated wrapped-line count (~48 chars/line)
  against a ~14-line budget, not bullet count. Only surface a genuine
  milestone-type event (sign-off, review, completion, risk resolved), not
  routine follow-up chatter.
- **Risks** — straight from the RAID log; genuinely often empty.

**Rendering the review step is the one place the mechanism has to change.**
The desktop skill uses a Claude-Code-specific inline widget tool. In a browser
session, publish the same 5-component review layout (Milestone grid,
project-info grid, overall-status grid, two bulleted rich-text boxes, risk
grid) as a Claude **Artifact** (interactive HTML) instead — same visual
layout and editability, different underlying mechanism. Don't assume the
artifact can call back into this skill's Python state directly (that depends
on runtime capabilities that may not be enabled for every account) — the
safe, portable pattern is: render the artifact for the user to review, then
ask them to confirm or list edits in their next chat message, and only then
proceed to Step 2 with their finalized values. Only reach for a live
callback-from-artifact mechanism if you've confirmed (via the
`artifact-capabilities` skill or equivalent) that the running account
actually supports it.

### Step 2: known-good edits, once you have finalized data

Same table/shape names as the desktop skill (confirmed by direct inspection —
reuse rather than re-discovering, but re-verify against the actual template if
it's ever revised):

| Shape name | Contents |
|---|---|
| `Table 8` | Project Name (merged row 1) / Project Manager(s) / Status Period |
| `Table 9` | Overall Status text (row 1) / 3 blank sub-category rows |
| `Oval 22`, `Oval 1`, `Oval 11`, `Oval 12` | Status color dots — Overall / Scope & Schedule / Resources / Data |
| `Table 14` | Milestones (Milestone/Start Date/Status, 1-indexed rows starting at row 2) |
| `Table 16` | Activities Completed & Planned (row 2 holds the bulleted lists, col 1 = accomplishments, col 2 = planned) |
| `Table 19` | Key Risks & Issues |

Green/Yellow/Red RGB values, same constants as the desktop skill: Green
`(0x67, 0x99, 0x22)` from int `6786602`, Yellow `(0x21, 0xa1, 0x99)` from int
`2204889` — reuse `add_position_marker`'s default rather than a new literal
for the Yellow value specifically, since it's the same color as the Slide 3
marker. Red `4871627`. For an all-Green status: strip the " Yellow Red"
substring from `Table 9` cell (1,1) via `replace_text_in_run`, and set all 4
ovals' fill color to Green.

```python
tbl14 = find_table_by_name(slide4, "Table 14")  # write this small helper per-shape.name lookup, or inline it
set_cell_text(tbl14, 2, 1, "Kickoff deck finalized")
set_cell_text(tbl14, 2, 2, "7/14")
set_cell_text(tbl14, 4, 3, "Complete")
```

**Milestone table column widths.** Same overflow risk as the desktop skill —
after deleting a column or adding many rows, check the resulting table height
against the space before "Key Risks & Issues" below it. python-pptx table
column widths are set via `table.columns[i].width = Emu(...)`; row heights via
`table.rows[i].height = Emu(...)`. Same known-good numbers as the desktop
skill apply since it's the same template: Milestone col ~135pt, Start Date
~64pt, Status ~72.48pt; for a 12-row Milestones table, 9pt font + reduced cell
margins + ~16pt row height, same reasoning — PowerPoint (and, presumably,
however this template's XML defines row-height behavior) only actually shrinks
a table below its content's natural height once font/margins are also
reduced, not from row-height alone. **Not yet re-verified under python-pptx
specifically** — check the actual rendered/measured result on first real use
rather than assuming the numbers transfer exactly.

**Drop the "Build:" prefix from milestone names** — same rule, e.g. "Build:
Reporting & Security" → "Reporting & Security".

**Bulleted cell rewrites** (Accomplishments/Planned): use
`rewrite_bulleted_cell`, not `set_cell_text` — see its docstring for why (bold
handling, preserving the template's bullet formatting).

**Empty-risks phrasing:** same as the desktop skill — "No open risks or
issues outstanding." not "...identified this period."

## Resolving "which client project"

Same rule as the desktop skill: in real deployment, bake the client name into
whatever's driving the run (a scheduled task's prompt, or just the user's
chat message asking for a specific client) rather than resolving it from
memory or a bootstrapping conversation.

## Verification before calling it done

- **Prefer** `try_export_slide_png` for every touched slide and actually look
  at the result — table overflow, wrong formatting, and stray artifacts are
  all things a text dump won't show.
- **If that returns False** (no LibreOffice in the sandbox), fall back to:
  explicitly reading back every table's row/column count and full cell-text
  dump after any add/delete/rewrite, and say plainly in your response that
  visual QA wasn't possible in this environment — don't claim a visual check
  that didn't happen.
- Confirm the picture relationship rewrite in `copy_slide_from_external`
  actually produced a valid, viewable image — reopen the saved file fresh (a
  second `Presentation(path)` call) and check the copied picture shape's
  `.image.blob` is non-empty, rather than trusting that no exception was
  thrown during the copy.
