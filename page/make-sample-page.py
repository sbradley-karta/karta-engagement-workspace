#!/usr/bin/env python3
"""Build a self-contained sample of the engagement workspace with a mock runtime and fictional data.

Output: page/dist/engagement-workspace-sample.html (dist is not committed). Open it in any browser: the page
believes it is running in the Claude viewer with every connector connected, one approved weekly status and one
built deck. Nothing is read from a real system. Used for screenshots in marketing material
(docs/one-pager). The fictional engagement is Northwind Foods · Anaplan FP&A, in Build week 10 of 11.

    python3 make-sample-page.py [--light]
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).parent
SRC = HERE / "engagement-workspace.html"
OUT = HERE / "dist" / "engagement-workspace-sample.html"
DARK = "--light" not in sys.argv

ROOT = "engagements/this"
STAGES = [
    ("planning", "Project Planning", "2026-06-01", "2026-06-12", "stage", True),
    ("foundations", "Foundations", "2026-06-15", "2026-07-03", "stage", True),
    ("build", "Build", "2026-07-06", "2026-09-18", "stage", True),
    ("test", "Test", "2026-09-21", "2026-10-02", "stage", True),
    ("train", "Train", "2026-09-14", "2026-10-09", "parallel", True),
    ("deploy", "Deploy", "2026-10-05", "2026-10-16", "stage", True),
    ("support", "Continuous Support", "2026-10-19", None, "stage", True),
]

CONFIG = {
    "schema_version": "1.2",
    "engagement_id": "northwind-anaplan-fpa",
    "client": "Northwind Foods",
    "project_name": "Anaplan FP&A",
    "owner": {"name": "A. Patel", "email": "apatel@example.com"},
    "roles": {"reviewers": [{"name": "M. Chen", "email": "mchen@example.com"}], "members": []},
    "stages": [{"id": i, "name": n, "start": s, "end": e, "kind": k, "contracted": c} for i, n, s, e, k, c in STAGES],
    "stages_confirmed_at": "2026-09-04",
    "control_points": [{
        "stage": "build", "name": "Sprint 3 review · initial business acceptance", "due": "2026-09-11",
        "owner": "J. Rivera (client)", "decision": "accept, follow up, or change",
        "evidence": [{"item": "Demo items listed", "state": "ok"}, {"item": "Requirements mapped", "state": "ok"},
                     {"item": "Sprint 2 follow-ups closed", "state": "ok"}, {"item": "Attendance confirmed", "state": "ok"}],
    }],
    "deliverables": {"build": [
        {"name": "Project build plan", "state": "Approved"}, {"name": "Data hub", "state": "In progress"},
        {"name": "Configured dashboards", "state": "Draft"}, {"name": "Model documentation", "state": "Not started"},
    ]},
    "sources": {
        "asana": {"project_url": "https://app.asana.com/1/1/project/1200000000000001", "project_gid": "1200000000000001",
                  "project_name": "Northwind Foods Anaplan FP&A", "verified": True,
                  "milestone_section_names": ["Project Milestones"], "milestone_resource_subtype": "milestone"},
        "sharepoint": {"engagement_folder_url": "https://example.sharepoint.com/:f:/s/Documents/sample", "drive_id": "b!sample",
                       "folder_item_id": "01SAMPLEFOLDER", "folder_web_url": "https://example.sharepoint.com/sites/Documents/Northwind",
                       "label": "Northwind Foods / Anaplan FP&A", "status_folder_item_id": "01SAMPLESTATUS",
                       "status_folder_web_url": "https://example.sharepoint.com/sites/Documents/Northwind/00 - Project Management/Status & Steer Co",
                       "verified": True},
        "granola": {"folder_name": "Northwind Anaplan", "folder_id": "g1", "note_count": 23, "verified": True},
        "harvest": {"project": "Northwind", "project_id": 1, "project_name": "Northwind Foods – Anaplan FP&A", "client_name": "Northwind Foods", "code": "NWF-FPA", "verified": True},
    },
    "capabilities": [
        {"id": "status", "name": "Create weekly status", "description": "Review this week’s evidence and prepare the client deck", "readiness": "Piloted", "owner": "A. Patel", "live": True, "stages": ["planning", "foundations", "build", "test", "train", "deploy"]},
        {"id": "sprint", "name": "Prepare sprint review", "description": "What will be shown, requirements covered, evidence", "readiness": "Next", "owner": "A. Patel", "live": False, "stages": ["build"]},
        {"id": "meeting", "name": "Capture meeting outcomes", "description": "Turn workshop notes into actions and decisions", "readiness": "Next", "owner": "Unassigned", "live": False, "stages": ["planning", "foundations", "build"]},
        {"id": "mockup", "name": "Generate a mockup", "description": "Turn requirements or an idea into an editable visual", "readiness": "Piloted", "owner": "A. Patel", "live": True, "stages": ["foundations", "build"]},
        {"id": "uat", "name": "Prepare for UAT", "description": "Turn approved requirements into test scripts", "readiness": "Later", "owner": "Unassigned", "live": False, "stages": ["test"]},
        {"id": "onboard", "name": "Onboarding brief", "description": "Bring a new team member up to speed from the approved record", "readiness": "Later", "owner": "Unassigned", "live": False, "stages": ["planning", "foundations", "build", "test", "train", "deploy", "support"]},
    ],
    "support": {"route": "Message A. Patel in Teams"},
    "updated_at": "2026-09-04T16:00:00Z", "updated_by": "apatel@example.com",
}

def ms(name, orig, new=None, completed=False, completed_at=None, status="On Track", var=None, gid="1"):
    return {"name": name, "completed": completed, "completed_at": completed_at, "original_date": orig, "new_date": new,
            "status": status, "variance_days": var, "source": {"system": "asana", "id": gid}}

APPROVED_AT = "2026-09-04T21:10:00Z"
APPROVED = {
    "schema_version": "1.0",
    "engagement": {"engagement_id": "northwind-anaplan-fpa", "client": "Northwind Foods", "project_name": "Anaplan FP&A"},
    "period": {"start": "2026-08-31", "end": "2026-09-04", "label": "August 31 to September 4, 2026"}, "as_of": "2026-09-04",
    "project_managers": [],
    "milestones": [
        ms("Sprint 1 review", "2026-07-24", completed=True, completed_at="2026-07-24T20:00:00Z", status="Complete", gid="11"),
        ms("Sprint 2 review", "2026-08-21", completed=True, completed_at="2026-08-21T20:00:00Z", status="Complete", gid="12"),
        ms("Load automation complete", "2026-09-08", status="Off Track", gid="13"),
        ms("Cost center map signed off", "2026-09-09", status="Off Track", gid="14"),
        ms("Sprint 3 review", "2026-09-11", status="On Track", gid="15"),
        ms("Build complete", "2026-09-18", new="2026-09-25", status="At Risk", var=7, gid="16"),
        ms("UAT complete", "2026-10-02", status="On Track", gid="17"),
        ms("Go-live", "2026-10-16", status="On Track", gid="18"),
    ],
    "assessments": {"scope_schedule": {"status": "Green", "rationale": "Build complete moved one week with client agreement; go-live unchanged."},
                    "resources": {"status": "Green", "rationale": "Team fully staffed through go-live."},
                    "data": {"status": "Green", "rationale": "Data hub load complete for all four source systems."}},
    "overall": {"status": "Green", "derivation": "worst_of"},
    "accomplishments": ["Data hub load completed for all four source systems", "Opex planning page v3 approved by finance leads", "Driver-based revenue model configured and reconciled to FY25 actuals"],
    "planned_activities": ["Sprint 3 review with initial business acceptance", "Allocations phasing decision at the September 16 workshop", "Begin UAT script drafting from approved requirements"],
    "raid": [{"type": "Risk", "priority": "High", "description": "Source data quality in the cost center hierarchy could delay allocations testing", "mitigation": "Finance to publish the corrected hierarchy by September 12", "status": "Open"},
             {"type": "Dependency", "priority": "Medium", "description": "Allocations phasing decision needed before Sprint 4", "mitigation": "Decision on the September 16 workshop agenda", "status": "Open"}],
    "source_gaps": [],
    "sources": [{"system": "asana", "retrieved_at": APPROVED_AT, "locator": "1200000000000001"}],
    "approval": {"reviewer_name": "M. Chen", "reviewer_email": "mchen@example.com", "approved_at": APPROVED_AT, "version": 6},
    "correction_capture": {"model_drafted_fields": ["accomplishments", "planned_activities", "raid"], "reviewer_changed_fields": ["planned_activities"],
                           "model_recommended_assessments": {"scope_schedule": "Yellow", "resources": "Green", "data": "Green"}},
}

JOB = {"schema_version": "1.0", "job_id": "sample-job", "engagement_id": "northwind-anaplan-fpa", "approved_values": {"version": 6, "sha256": "sample"},
       "state": "Built", "requested_by": "mchen@example.com", "requested_at": "2026-09-04T21:12:00Z", "updated_at": "2026-09-04T21:14:00Z",
       "delivery": "sharepoint", "deck": {"filename": "KCG_Status Northwind 9-4-2026.pptx", "saved_by_member": True}}

def task(gid, name, due, completed=False, completed_at=None, milestone=True, assignee="A. Patel"):
    t = {"gid": gid, "name": name, "due_on": due, "start_on": None, "completed": completed, "completed_at": completed_at,
         "assignee": {"name": assignee}, "memberships": [{"section": {"name": "Project Milestones" if milestone else "Build"}}]}
    if milestone:
        t["resource_subtype"] = "milestone"
    return t

TASKS = [
    task("11", "Sprint 1 review", "2026-07-24", True, "2026-07-24T20:00:00Z"),
    task("12", "Sprint 2 review", "2026-08-21", True, "2026-08-21T20:00:00Z"),
    task("13", "Load automation complete", "2026-09-08"),
    task("14", "Cost center map signed off", "2026-09-09"),
    task("15", "Sprint 3 review", "2026-09-11"),
    task("16", "Build complete", "2026-09-18"),
    task("17", "UAT complete", "2026-10-02"),
    task("18", "Go-live", "2026-10-16"),
    task("21", "Opex planning page v3 approved", "2026-09-08", True, "2026-09-08T18:30:00Z", milestone=False),
    task("22", "Driver-based revenue model reconciled to FY25 actuals", "2026-09-04", True, "2026-09-04T15:00:00Z", milestone=False, assignee="R. Okafor"),
    task("23", "Allocations phasing workshop", "2026-09-16", milestone=False),
    task("24", "Draft UAT scripts", "2026-09-18", milestone=False),
]

DECKS = [{"name": "KCG_Status Northwind 9-4-2026.pptx", "driveId": "b!sample", "id": "01SAMPLEDECK", "lastModifiedDateTime": "2026-09-04T21:14:00Z"}]

DOCS = {ROOT + "/config/current": CONFIG,
        ROOT: {"latestApprovedVersion": 6, "latestApprovedAt": APPROVED_AT, "latestApprovedBy": "M. Chen", "updatedAt": APPROVED_AT},
        ROOT + "/approved/v6": APPROVED}
COLS = {ROOT + "/jobs": [JOB], ROOT + "/measures": []}

MOCK = """<script>
/* Sample runtime: stands in for the Claude viewer. Every read returns fictional data. */
(function(){
  var DOCS=%s, COLS=%s, TASKS=%s, DECKS=%s;
  function snap(v){return {data:function(){return v},exists:v!=null};}
  function later(fn){setTimeout(fn,0);}
  var db={
    doc:function(p){return {
      onSnapshot:function(cb){later(function(){cb(snap(DOCS[p]||null))});return function(){}},
      get:function(){return Promise.resolve(snap(DOCS[p]||null))},
      set:function(v){DOCS[p]=v;return Promise.resolve()},
      update:function(v){DOCS[p]=Object.assign({},DOCS[p]||{},v);return Promise.resolve()}};},
    collection:function(p){var q={
      onSnapshot:function(cb){later(function(){cb({docs:(COLS[p]||[]).map(snap)})});return function(){}},
      orderBy:function(){return q},limit:function(){return q},
      get:function(){return Promise.resolve({docs:(COLS[p]||[]).map(snap)})}};return q;}
  };
  var SERVERS=["Asana","Microsoft 365","Granola","Harvest App","Karta Assembly"];
  var mcp={
    listTools:function(){return Promise.resolve({servers:SERVERS.map(function(s){return {server:s,tools:[]}})})},
    watchTool:function(server,tool,args,cb){later(function(){
      var payload=tool==="asana_search_tasks"?{data:TASKS}:DECKS;
      cb({type:"result",result:{payload:payload,cache:{storedAt:Date.now()-6*60000}}});});return function(){}},
    callTool:function(){return Promise.resolve({payload:{}})}
  };
  var sample={json:function(){var e=new Error("Drafting is not available in the sample page.");e.code="not_granted";return Promise.reject(e);}};
  window.claude={use:function(n){return Promise.resolve({db:db,mcp:mcp,sample:sample}[n]||null)}};
})();
</script>
""" % (json.dumps(DOCS), json.dumps(COLS), json.dumps(TASKS), json.dumps(DECKS))

html = SRC.read_text()
html = html.replace("<title>Karta Engagement Workspace</title>", "<title>Northwind Foods · Anaplan FP&amp;A (sample)</title>", 1)
i = html.index("<script>")
html = html[:i] + MOCK + html[i:]
wrapped = ('<!doctype html><html lang="en"%s><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif;background:#faf9f7}img{max-width:100%%}[hidden]{display:none!important}</style>'
           '</head><body>%s</body></html>') % (' data-theme="dark"' if DARK else "", html)
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(wrapped)
print("wrote", OUT, len(wrapped))
