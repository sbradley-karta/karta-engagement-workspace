from datetime import date

import pytest

from karta_assembler.status import (
    AssessmentStatus,
    MilestoneStatus,
    derive_milestone_status,
    governing_date,
    in_sections,
    milestone_from_asana,
    rollup_overall,
    status_period,
    strip_build_prefix,
    variance_days,
)

AS_OF = date(2026, 9, 4)  # a Friday


# --- milestone status -------------------------------------------------------

def test_completed_wins_regardless_of_dates():
    assert derive_milestone_status(True, "2026-01-01", None, AS_OF) is MilestoneStatus.COMPLETE
    assert derive_milestone_status(True, None, None, AS_OF) is MilestoneStatus.COMPLETE


def test_missing_evidence_is_unknown_never_on_track():
    assert derive_milestone_status(False, None, None, AS_OF) is MilestoneStatus.UNKNOWN


def test_future_original_date_is_on_track():
    assert derive_milestone_status(False, "2026-09-18", None, AS_OF) is MilestoneStatus.ON_TRACK


def test_date_equal_to_as_of_is_still_on_track():
    assert derive_milestone_status(False, "2026-09-04", None, AS_OF) is MilestoneStatus.ON_TRACK


def test_past_original_date_without_replan_is_off_track():
    assert derive_milestone_status(False, "2026-08-14", None, AS_OF) is MilestoneStatus.OFF_TRACK


def test_new_date_governs_over_past_original():
    # Original slipped, approved new date is in the future: judged against the new date.
    assert derive_milestone_status(False, "2026-08-14", "2026-09-25", AS_OF) is MilestoneStatus.AT_RISK


def test_new_date_in_the_past_is_off_track():
    assert derive_milestone_status(False, "2026-08-14", "2026-08-28", AS_OF) is MilestoneStatus.OFF_TRACK


def test_new_date_earlier_than_original_is_on_track():
    assert derive_milestone_status(False, "2026-10-02", "2026-09-25", AS_OF) is MilestoneStatus.ON_TRACK


def test_new_date_only_no_original():
    assert governing_date(None, "2026-09-25") == date(2026, 9, 25)
    assert derive_milestone_status(False, None, "2026-09-25", AS_OF) is MilestoneStatus.ON_TRACK
    assert variance_days(None, "2026-09-25") is None


def test_variance_days():
    assert variance_days("2026-08-14", "2026-09-25") == 42
    assert variance_days("2026-09-25", "2026-09-18") == -7
    assert variance_days("2026-09-25", None) is None


# --- rollup -----------------------------------------------------------------

@pytest.mark.parametrize("statuses,expected", [
    (["Green", "Green", "Green"], AssessmentStatus.GREEN),
    (["Green", "Yellow", "Green"], AssessmentStatus.YELLOW),
    (["Yellow", "Red", "Green"], AssessmentStatus.RED),
    (["Green", "Green", "Unknown"], AssessmentStatus.UNKNOWN),
    (["Green", "Not assessed", "Green"], AssessmentStatus.UNKNOWN),
    (["Yellow", "Unknown", "Green"], AssessmentStatus.YELLOW),
    (["Red", "Not assessed", "Unknown"], AssessmentStatus.RED),
])
def test_rollup_worst_of(statuses, expected):
    assert rollup_overall(statuses) is expected


def test_rollup_never_green_with_missing_evidence():
    for gap in ("Unknown", "Not assessed"):
        assert rollup_overall(["Green", "Green", gap]) is not AssessmentStatus.GREEN


def test_rollup_of_nothing_is_not_green():
    assert rollup_overall([]) is AssessmentStatus.NOT_ASSESSED


# --- period -----------------------------------------------------------------

def test_status_period_is_monday_to_friday():
    p = status_period(date(2026, 9, 2))  # Wednesday
    assert (p.start, p.end) == (date(2026, 8, 31), date(2026, 9, 4))
    assert p.label == "August 31 to September 4, 2026"


def test_status_period_on_a_weekend_belongs_to_the_week_just_ended():
    p = status_period(date(2026, 9, 6))  # Sunday
    assert (p.start, p.end) == (date(2026, 8, 31), date(2026, 9, 4))


def test_status_period_single_month_label():
    assert status_period(date(2026, 9, 9)).label == "September 7 to 11, 2026"


# --- asana mapping (observed shape: due_on set, start_on null) -------------

SYNTHETIC_TASKS = [
    {"gid": "1", "name": "Build: Data Hub loaded", "completed": True, "completed_at": "2026-08-20T15:00:00.000Z",
     "due_on": "2026-08-21", "start_on": None, "memberships": [{"section": {"name": "Project Milestones"}}]},
    {"gid": "2", "name": "Requirements sign-off", "completed": False, "completed_at": None,
     "due_on": "2026-08-14", "start_on": None, "memberships": [{"section": {"name": "Project Milestones"}}]},
    {"gid": "3", "name": "UAT start", "completed": False, "completed_at": None,
     "due_on": "2026-09-21", "start_on": None, "memberships": [{"section": {"name": "Project Milestones"}}]},
    {"gid": "4", "name": "Undated task", "completed": False, "completed_at": None,
     "due_on": None, "start_on": None, "memberships": [{"section": {"name": "Project Milestones"}}]},
    {"gid": "5", "name": "Routine chore", "completed": False, "completed_at": None,
     "due_on": "2026-09-10", "start_on": None, "memberships": [{"section": {"name": "Admin"}}]},
]


def test_section_filter_is_client_side_and_case_insensitive():
    kept = [t for t in SYNTHETIC_TASKS if in_sections(t, ["project milestones"])]
    assert [t["gid"] for t in kept] == ["1", "2", "3", "4"]


def test_asana_mapping_derives_status_and_strips_prefix():
    rows = [milestone_from_asana(t, AS_OF) for t in SYNTHETIC_TASKS[:4]]
    assert rows[0]["name"] == "Data Hub loaded" and rows[0]["status"] == "Complete"
    assert rows[1]["status"] == "Off Track" and rows[1]["original_date"] == "2026-08-14"
    assert rows[2]["status"] == "On Track"
    assert rows[3]["status"] == "Unknown" and rows[3]["variance_days"] is None
    assert all(r["source"] == {"system": "asana", "id": r["source"]["id"]} for r in rows)


def test_asana_mapping_with_approved_new_date():
    row = milestone_from_asana(SYNTHETIC_TASKS[1], AS_OF, new_date="2026-09-25")
    assert row["status"] == "At Risk" and row["variance_days"] == 42


def test_strip_build_prefix_only_at_start():
    assert strip_build_prefix("Build: Thing") == "Thing"
    assert strip_build_prefix("Rebuild: Thing") == "Rebuild: Thing"
