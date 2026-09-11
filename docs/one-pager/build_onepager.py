#!/usr/bin/env python3
"""Build the combined one-pager (engagement-workspace-onepager.html) from the data below.
Render: Chrome --headless --print-to-pdf --no-pdf-header-footer. Light page (Karta system). The screen mirrors the
workspace Home page (page/engagement-workspace.html) in its dark theme: top bar, rail with source chips,
seven-stage journey, and the three panels (Now, Needs attention, Evidence and decisions)."""
import pathlib, base64

HERE = pathlib.Path(__file__).parent
LOGO = base64.b64encode((HERE / "../../design/brand/karta-k-green.png").read_bytes()).decode()

HEADLINE = "Open Monday already knowing where your engagement stands."
PROMISE = ("Every Karta engagement gets its own AI-enabled workspace. Claude <b>reads the engagement's evidence</b>, "
           "<b>drafts Karta's artifacts</b> and <b>remembers every decision</b>, inside Karta's method and with a named person "
           "accountable for every output.")
BENEFITS = [
    ("A", "See where you stand", "The lifecycle, the next control point, and whether its evidence is ready."),
    ("B", "Know what needs attention", "Slipped dates, open decisions, capacity gaps. Calculated, not typed."),
    ("C", "Do the week's work without rebuilding context", "Status, sprint reviews and UAT scripts drafted from one approved record."),
    ("D", "One door for every AI capability", "Each arrives with an owner, a readiness label and a place on the lifecycle. Use and corrections are measured, so Karta knows what to scale."),
]
PROOF = ("<b>Real, and running.</b> Live for Legend since September 8, 2026. First Weekly Status approved and the deck built "
         "the next day. A new engagement is set up in about ten minutes.")

# stage: (name, subtitle, side, why, [(workflow, status)])  status: live | skill | next | later
STAGES = [
    ("Sales to Delivery", "handover", True, "Starts the record the whole engagement will use.",
     [("Sales Handover package", "later"), ("Kick-off deck and first two weeks", "later")]),
    ("Project Planning", "align · kick off", False, "Everything after it depends on setup being right.",
     [("Engagement setup and access check", "live"), ("Data intake coordination", "later")]),
    ("Foundations", "requirements · design", False, "Catches ambiguity and scope drift before build.",
     [("Meeting closeout into requirements", "next"), ("Design-to-scope reconciliation", "later")]),
    ("Build", "model · reports", False, "Weekly, measurable, and traceable as a by-product.",
     [("Weekly Status", "live"), ("Sprint review preparation", "next")]),
    ("Test", "UAT · sign-off", False, "Coverage comes free; scope disputes get settled.",
     [("UAT scripts from requirements", "skill"), ("Defect intake and triage", "later")]),
    ("Train & Deploy", "training · cutover", False, "The longest deliverables, drafted from the solution.",
     [("Role-based training material", "skill"), ("Go-live package and closeout", "later")]),
    ("Continuous Support", "handover · triage", True, "Support inherits the memory, not a folder.",
     [("Support handover with open items", "later"), ("Issue triage and recurring analysis", "later")]),
]

RELEASES = [
    ("October", "Foundation", "Weekly Status every Friday on two engagements. Ask Claude live. Capability catalog with owners and readiness. Teams onboarded in under an hour."),
    ("November", "Context", "Meeting notes from Granola and capacity from Harvest read into attention items and answers. Drafting tuned from a month of measured corrections."),
    ("December", "Beyond status", "Sprint review preparation live in Build. First Foundations Package piece: requirements, decisions and scope visible. The evidence for the scale decision."),
]

RULES = [
    ("Reads as the person looking", "No shared logins. Not on the project, you see nothing from it."),
    ("A named person approves", "Every client-facing output carries a reviewer's name and time."),
    ("Nothing sent by software", "The workspace produces. A person decides and sends."),
    ("Unknown is never Green", "Missing evidence is shown as missing and recorded."),
]

def tag(s):
    return {"live": '<span class="tag live">Live</span>', "skill": '<span class="tag skill">Skill</span>',
            "next": '<span class="tag next">Next</span>', "later": '<span class="tag later">Later</span>'}[s]

def stages_html():
    out = []
    for name, sub, side, why, wfs in STAGES:
        rows = "".join(f'<div class="wf"><span>{t}</span>{tag(s)}</div>' for t, s in wfs)
        out.append(f'<div class="stage{" side" if side else ""}"><div class="hd">{name}<small>{sub}</small></div>{rows}<p class="why">{why}</p></div>')
    return "".join(out)

def benefits_html():
    return "".join(f'<li><i>{k}</i><div><b>{t}</b><span>{d}</span></div></li>' for k, t, d in BENEFITS)

def releases_html():
    return "".join(f'<div class="rel"><div class="m">{m}</div><b>{t}</b><p>{d}</p></div>' for m, t, d in RELEASES)

def rules_html():
    return "".join(f'<div><b>{t}.</b> {d}</div>' for t, d in RULES)

# ---------------------------------------------------------------- screen: mirrors page/engagement-workspace.html Home (dark theme)
D = dict(ground="#111213", surface="#191B1C", raise_="#1F2122", topbar="#141516", line="#2C2F2E", line2="#3C403E",
         ink="#F2F3F2", text="#E4E7E5", muted="#A2A7A3", faint="#7E837F", accent="#2F6B4E", accent2="#6FB08D",
         soft="#18261F", chip="#1A2620", chipink="#7FBF9C", risk="#E0705F", warn="#D6A85B")

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

def screen_svg():
    o = []
    A = o.append
    A('<svg viewBox="0 0 900 520" role="img" aria-label="Illustrative future view of the engagement workspace home page in the Build stage.">')
    A('<defs><clipPath id="sc"><rect x="0" y="0" width="900" height="520" rx="12"/></clipPath></defs><g clip-path="url(#sc)">')
    A(f'<rect x="0" y="0" width="900" height="520" fill="{D["ground"]}"/>')
    # top bar
    A(f'<rect x="0" y="0" width="900" height="34" fill="{D["topbar"]}"/><line x1="0" y1="34" x2="900" y2="34" stroke="{D["line"]}"/>')
    A(f'<rect x="12" y="7" width="20" height="20" rx="4" fill="{D["accent"]}"/><text x="22" y="22" text-anchor="middle" fill="#fff" font-size="12" font-weight="800">K</text>')
    A(f'<line x1="40" y1="10" x2="40" y2="24" stroke="{D["line2"]}"/>')
    A(f'<text x="48" y="22" fill="{D["ink"]}" font-size="10" font-weight="700">Karta AI <tspan fill="{D["muted"]}" font-weight="500">Engagement Workspace</tspan></text>')
    A(f'<rect x="733" y="7" width="100" height="20" rx="10" fill="{D["accent"]}"/><text x="745" y="21" fill="#fff" font-size="8.5" font-weight="700">Ask Claude</text><rect x="800" y="10" width="27" height="14" rx="3" fill="{D["ink"]}"/><text x="804" y="20" fill="{D["accent"]}" font-size="6.2" font-weight="800">BETA</text>')
    for cx in (850, 870):
        A(f'<circle cx="{cx}" cy="17" r="8" fill="none" stroke="{D["line2"]}"/>')
    A(f'<circle cx="889" cy="17" r="8" fill="{D["accent"]}"/>')
    # rail
    A(f'<rect x="0" y="34" width="78" height="486" fill="{D["topbar"]}"/><line x1="78" y1="34" x2="78" y2="520" stroke="{D["line"]}"/>')
    nav = ["Home", "Weekly status", "Milestones", "RAID", "Decisions", "Artifacts", "Catalog"]
    for i, n in enumerate(nav):
        y = 44 + i * 27
        if i == 0:
            A(f'<rect x="6" y="{y-2}" width="66" height="26" rx="6" fill="{D["soft"]}"/>')
        col = D["accent2"] if i == 0 else D["muted"]
        A(f'<rect x="33" y="{y+2}" width="12" height="9" rx="2" fill="none" stroke="{col}" stroke-width="1.1"/>')
        A(f'<text x="39" y="{y+21}" text-anchor="middle" fill="{col}" font-size="6.4" font-weight="600">{esc(n)}</text>')
    A(f'<text x="10" y="326" fill="{D["faint"]}" font-size="5.6" font-weight="700" letter-spacing="0.8">SOURCES</text>')
    for i, n in enumerate(["Asana", "SharePoint", "Assembly Server", "Granola", "Harvest", "RAID log"]):
        y = 333 + i * 17
        A(f'<rect x="8" y="{y}" width="62" height="13" rx="3" fill="{D["surface"]}" stroke="{D["line"]}"/><circle cx="15" cy="{y+6.5}" r="2.2" fill="{D["accent2"]}"/><text x="20" y="{y+9.4}" fill="{D["ink"]}" font-size="6" font-weight="600">{esc(n)}</text>')
    A(f'<rect x="33" y="490" width="12" height="9" rx="2" fill="none" stroke="{D["muted"]}" stroke-width="1.1"/><text x="39" y="509" text-anchor="middle" fill="{D["muted"]}" font-size="6.4" font-weight="600">Config</text>')
    # header
    A(f'<text x="90" y="60" fill="{D["ink"]}" font-size="15" font-weight="800" letter-spacing="-0.3">Your engagement <tspan fill="{D["muted"]}" font-weight="500">· Anaplan FP&amp;A</tspan></text>')
    A(f'<rect x="548" y="46" width="176" height="18" rx="5" fill="{D["chip"]}"/><text x="556" y="58.5" fill="{D["chipink"]}" font-size="7.2" font-weight="700">Week in focus · September 7 to 11, 2026</text>')
    A(f'<text x="888" y="58.5" text-anchor="end" fill="{D["muted"]}" font-size="7.2">Overall status Green · approved Fri by M. Chen</text>')
    # journey
    stages = [("Project Planning", "Jun 1 – Jun 12 · complete", "done"), ("Foundations", "Jun 15 – Jul 3 · complete", "done"),
              ("Build", "Jul 6 – Sep 18 · current", "now"), ("Test", "Sep 21 – Oct 2 · upcoming", "next"),
              ("Train", "Sep 14 – Oct 9 · parallel", "par"), ("Deploy", "Oct 5 – Oct 16 · upcoming", "next"),
              ("Continuous Support", "from Oct 19 · upcoming", "next")]
    for i, (n, sub, st) in enumerate(stages):
        x = 90 + i * 114
        if st == "done":
            fill, stroke, tc, sc, dash = D["soft"], D["line"], D["accent2"], D["accent2"], ""
        elif st == "now":
            fill, stroke, tc, sc, dash = D["accent"], D["accent"], D["ink"], D["ink"], ""
        elif st == "par":
            fill, stroke, tc, sc, dash = D["surface"], D["accent2"], D["ink"], D["muted"], ' stroke-dasharray="3 2"'
        else:
            fill, stroke, tc, sc, dash = D["surface"], D["line2"], D["ink"], D["muted"], ""
        A(f'<rect x="{x}" y="86" width="108" height="36" rx="6" fill="{fill}" stroke="{stroke}"{dash}/>')
        A(f'<circle cx="{x+12}" cy="99" r="6" fill="none" stroke="{tc}" stroke-width="1.2"/>')
        if st == "done":
            A(f'<path d="M{x+9} 99l2.2 2.2 4-4.6" fill="none" stroke="{tc}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            A(f'<text x="{x+12}" y="101.5" text-anchor="middle" fill="{tc}" font-size="6.5" font-weight="800">{i+1}</text>')
        A(f'<text x="{x+22}" y="102" fill="{tc}" font-size="7.6" font-weight="700">{esc(n)}</text>')
        A(f'<text x="{x+8}" y="115" fill="{sc}" font-size="6.3">{esc(sub)}</text>')
    # cards
    for x, w in ((90, 346), (446, 216), (672, 216)):
        A(f'<rect x="{x}" y="132" width="{w}" height="376" rx="8" fill="{D["surface"]}" stroke="{D["line"]}"/>')
    # now panel
    A(f'<text x="102" y="152" fill="{D["ink"]}" font-size="10" font-weight="700">Now in Build</text><text x="424" y="152" text-anchor="end" fill="{D["muted"]}" font-size="7">Jul 6 to Sep 18 · week 6 of 11</text>')
    A(f'<text x="102" y="167" fill="{D["muted"]}" font-size="6.8">Configure the solution through a disciplined, traceable build and obtain documented</text><text x="102" y="177" fill="{D["muted"]}" font-size="6.8">business acceptance at each sprint review.</text>')
    A(f'<rect x="102" y="186" width="322" height="94" rx="7" fill="{D["soft"]}" stroke="{D["line"]}"/>')
    A(f'<rect x="112" y="196" width="9" height="8" rx="1.5" fill="none" stroke="{D["accent2"]}" stroke-width="1.1"/><text x="126" y="203" fill="{D["accent2"]}" font-size="5.8" font-weight="700" letter-spacing="0.8">NEXT CONTROL POINT</text><text x="414" y="203" text-anchor="end" fill="{D["accent2"]}" font-size="7" font-weight="700">Evidence 4 of 4 ready</text>')
    A(f'<text x="112" y="219" fill="{D["ink"]}" font-size="9" font-weight="700">Sprint 3 review · initial business acceptance</text>')
    A(f'<text x="112" y="231" fill="{D["muted"]}" font-size="6.4">Due Sep 26 · Owner: J. Rivera (client) · Decision: accept, follow up, or change</text>')
    for i, e in enumerate(["Demo items listed", "Requirements mapped", "Sprint 2 follow-ups closed", "Attendance confirmed"]):
        cx = 112 + (i % 2) * 158; cy = 240 + (i // 2) * 20
        A(f'<rect x="{cx}" y="{cy}" width="150" height="16" rx="4" fill="{D["surface"]}" stroke="{D["line"]}"/><circle cx="{cx+10}" cy="{cy+8}" r="5" fill="{D["accent"]}"/><path d="M{cx+7.5} {cy+8}l1.8 1.8 3.2-3.8" fill="none" stroke="#fff" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/><text x="{cx+20}" y="{cy+11}" fill="{D["text"]}" font-size="6.4">{esc(e)}</text>')
    A(f'<text x="102" y="298" fill="{D["faint"]}" font-size="5.8" font-weight="700" letter-spacing="0.8">STAGE DELIVERABLES</text><text x="266" y="298" fill="{D["faint"]}" font-size="5.8" font-weight="700" letter-spacing="0.8">RECOMMENDED NOW</text>')
    dl = [("Project build plan", "Approved", D["chipink"], D["chip"]), ("Data hub", "In progress", D["warn"], D["raise_"]), ("Configured dashboards", "Draft", D["muted"], D["raise_"]), ("Model documentation", "Drafting", D["muted"], D["raise_"])]
    for i, (n, st, tc, bg) in enumerate(dl):
        y = 306 + i * 22
        A(f'<line x1="102" y1="{y}" x2="252" y2="{y}" stroke="{D["line"]}"/><text x="102" y="{y+14}" fill="{D["ink"]}" font-size="7.2">{esc(n)}</text><rect x="196" y="{y+4}" width="56" height="14" rx="4" fill="{bg}"/><text x="224" y="{y+13.6}" text-anchor="middle" fill="{tc}" font-size="6" font-weight="700">{esc(st)}</text>')
    rec = [("Create weekly status", "This week’s evidence, client deck", "start"), ("Prepare sprint review", "Demo items, requirements", "next"),
           ("Close out a workshop", "Granola into decisions", "next"), ("Draft UAT scripts", "From requirements, traceable", "later"),
           ("Generate a mockup", "Requirement to editable visual", "start")]
    for i, (n, sub, k) in enumerate(rec):
        y = 304 + i * 30
        A(f'<line x1="266" y1="{y}" x2="424" y2="{y}" stroke="{D["line"]}"/><rect x="266" y="{y+4}" width="20" height="20" rx="5" fill="{D["raise_"]}" stroke="{D["line"]}"/><rect x="272" y="{y+10}" width="8" height="8" rx="1.5" fill="none" stroke="{D["accent2"]}" stroke-width="1.1"/>')
        A(f'<text x="292" y="{y+13}" fill="{D["ink"]}" font-size="7.2" font-weight="700">{esc(n)}</text><text x="292" y="{y+22}" fill="{D["muted"]}" font-size="6">{esc(sub)}</text>')
        if k == "start":
            A(f'<rect x="386" y="{y+6}" width="38" height="16" rx="4" fill="{D["accent"]}"/><text x="405" y="{y+17}" text-anchor="middle" fill="#fff" font-size="6.8" font-weight="700">Start</text>')
        else:
            tc = D["warn"] if k == "next" else D["muted"]
            A(f'<rect x="376" y="{y+6}" width="48" height="16" rx="4" fill="{D["raise_"]}"/><text x="400" y="{y+17}" text-anchor="middle" fill="{tc}" font-size="6.4" font-weight="700">{"Next" if k=="next" else "Later"}</text>')
    # attention
    A(f'<text x="458" y="152" fill="{D["ink"]}" font-size="10" font-weight="700">Needs attention</text><rect x="606" y="141" width="44" height="14" rx="4" fill="{D["raise_"]}"/><text x="628" y="151" text-anchor="middle" fill="{D["risk"]}" font-size="6.4" font-weight="700">2 urgent</text>')
    att = [("2 milestones past date, no new date", "Load automation · Cost center map", True), ("Decision awaiting sign-off", "Allocations phasing · Sep 16 workshop", True),
           ("Capacity next week", "3 PTO days across the team · Harvest", False), ("Sprint 3 evidence complete", "Ready for the review", False),
           ("Open risk, 12 days", "Source data quality · RAID log", False), ("Stage dates confirmed", "Sep 5 by the engagement owner", False)]
    for i, (t, sub, urgent) in enumerate(att):
        y = 166 + i * 47
        A(f'<line x1="458" y1="{y}" x2="650" y2="{y}" stroke="{D["line"]}"/><rect x="458" y="{y+8}" width="18" height="18" rx="5" fill="{D["raise_"]}" stroke="{D["line"]}"/><rect x="463" y="{y+13}" width="8" height="8" rx="1.5" fill="none" stroke="{D["muted"]}" stroke-width="1.1"/>')
        tx = 482
        if urgent:
            A(f'<circle cx="485" cy="{y+14}" r="2.2" fill="{D["risk"]}"/>'); tx = 491
        A(f'<text x="{tx}" y="{y+17}" fill="{D["ink"]}" font-size="7" font-weight="700">{esc(t)}</text><text x="482" y="{y+28}" fill="{D["muted"]}" font-size="6.2">{esc(sub)}</text>')
        A(f'<path d="M644 {y+13}l3 3-3 3" fill="none" stroke="{D["faint"]}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>')
    # evidence
    A(f'<text x="684" y="152" fill="{D["ink"]}" font-size="10" font-weight="700">Evidence and decisions</text><text x="876" y="152" text-anchor="end" fill="{D["accent2"]}" font-size="6.6" font-weight="600">Capability catalog</text>')
    ev = [("Weekly status v6 approved", "Fri · M. Chen · Green overall", "Approved"), ("KCG_Status 9-12-2026.pptx", "Built Fri · saved to SharePoint", "Deck"),
          ("Decision: allocations phasing", "Workshop Sep 16 · Granola", "Decision"), ("Mockup approved", "Opex planning page v3", "Approved"),
          ("UAT scripts drafted", "From 42 approved requirements", "Draft"), ("Data hub load complete", "Completed Sep 4 · Asana", "Complete")]
    for i, (t, sub, tg) in enumerate(ev):
        y = 166 + i * 47
        A(f'<line x1="684" y1="{y}" x2="876" y2="{y}" stroke="{D["line"]}"/><rect x="684" y="{y+8}" width="18" height="18" rx="5" fill="{D["raise_"]}" stroke="{D["line"]}"/><rect x="689" y="{y+13}" width="8" height="8" rx="1.5" fill="none" stroke="{D["muted"]}" stroke-width="1.1"/>')
        A(f'<text x="708" y="{y+17}" fill="{D["ink"]}" font-size="7" font-weight="600">{esc(t)}</text><text x="708" y="{y+28}" fill="{D["muted"]}" font-size="6.2">{esc(sub)}</text>')
        A(f'<rect x="828" y="{y+10}" width="48" height="14" rx="4" fill="{D["chip"]}"/><text x="852" y="{y+19.6}" text-anchor="middle" fill="{D["chipink"]}" font-size="6" font-weight="700">{esc(tg)}</text>')
    A('</g>')
    A(f'<rect x="0.5" y="0.5" width="899" height="519" rx="12" fill="none" stroke="{D["line2"]}"/>')
    # callouts A–D: journey/control point, attention, recommended, catalog
    for letter, cx, cy in (("A", 426, 86), ("B", 662, 132), ("C", 446, 318), ("D", 446, 380)):
        A(f'<circle cx="{cx}" cy="{cy}" r="13" fill="#2A654E" stroke="#FFFFFF" stroke-width="2.5"/><text x="{cx}" y="{cy+4.5}" text-anchor="middle" fill="#FFFFFF" font-size="13" font-weight="800">{letter}</text>')
    A('</svg>')
    return "".join(o)

SCREEN = screen_svg()

HTML = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Karta AI Engagement Workspace</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<style>
@page{{size:13.333in 7.5in;margin:0}}
:root{{--ground:#FFFFFF;--raise:#F5F4F2;--ink:#113A2A;--text:#22302A;--muted:#6E6961;--faint:#979187;--line:#E4E2DE;--line2:#C9C5BE;--accent:#2A654E;--soft:#EAF1ED;--amber:#9A6B1F;--sans:"Manrope",system-ui,-apple-system,"Segoe UI",sans-serif}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:var(--ground);height:7.5in;overflow:hidden}}
body{{width:13.333in;height:7.5in;color:var(--text);font-family:var(--sans);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{position:relative;width:13.333in;height:7.5in;padding:0.3in 0.5in 0.42in;display:flex;flex-direction:column}}
.hero{{display:grid;grid-template-columns:1fr 5.7in;gap:0.4in;align-items:center;margin-bottom:0.1in}}
.brand{{display:flex;align-items:center;gap:9px;margin-bottom:10px}}
.brand img{{width:22px;height:22px}}
.brand b{{font-size:9.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink)}}
.brand span{{font-size:9.5px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;border-left:1px solid var(--line2);padding-left:9px}}
.eyebrow{{font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}}
h1{{font-size:29px;line-height:1.03;letter-spacing:-.03em;font-weight:800;margin:0 0 10px;text-wrap:balance;color:var(--ink)}}
.promise{{font-size:11px;line-height:1.42;color:var(--muted);margin:0 0 10px}}
.promise b{{color:var(--ink)}}
.benefits{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}}
.benefits li{{display:grid;grid-template-columns:22px 1fr;gap:10px;align-items:start}}
.benefits li i{{width:22px;height:22px;border-radius:50%;background:var(--accent);color:#fff;font-style:normal;font-weight:800;font-size:11px;display:flex;align-items:center;justify-content:center}}
.benefits b{{display:block;font-size:13px;font-weight:700;line-height:1.2;color:var(--ink)}}
.benefits span{{display:block;font-size:10px;color:var(--muted);line-height:1.35;margin-top:1px}}
.proof{{margin-top:10px;font-size:9.6px;color:var(--muted);line-height:1.38}}
.proof b{{color:var(--ink)}}
.screen svg{{display:block;width:100%;height:auto;font-family:var(--sans);filter:drop-shadow(0 6px 18px rgba(17,58,42,.18))}}
.sec{{display:flex;align-items:baseline;justify-content:space-between;margin:0 0 4px}}
.sec .eyebrow{{margin:0}}
.legend{{display:flex;gap:10px;align-items:center;font-size:8.4px;color:var(--muted);margin:0 0 7px;white-space:nowrap}}
.stages{{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}}
.stage .hd{{background:var(--ink);color:#fff;border-radius:6px;padding:5px 8px 4px;font-size:10.5px;font-weight:800;letter-spacing:-.01em;line-height:1.15;margin-bottom:6px}}
.stage .hd small{{display:block;font-size:8px;font-weight:500;color:#B7C9BF;margin-top:1px}}
.stage.side .hd{{background:var(--accent)}} .stage.side .hd small{{color:#DCEAE2}}
.wf{{display:flex;justify-content:space-between;align-items:center;gap:6px;padding:4px 2px;border-bottom:1px solid var(--line);font-size:9.2px;font-weight:600;line-height:1.22;color:var(--ink)}}
.wf > span:first-child{{flex:1}} .wf .tag{{flex:none}}
.tag{{font-size:6.8px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:2px 5px;border-radius:3px;white-space:nowrap;flex:none}}
.tag.live{{background:var(--accent);color:#fff}} .tag.skill{{background:#fff;color:var(--accent);border:1px solid var(--accent)}} .tag.next{{background:#fff;color:var(--amber);border:1px solid var(--amber)}} .tag.later{{background:transparent;color:var(--faint);border:1px solid transparent;padding-left:0;padding-right:0}}
.why{{margin:5px 2px 0;font-size:8.2px;line-height:1.3;color:var(--muted)}}
.bottom{{display:grid;grid-template-columns:1fr 1.9fr;gap:0.3in;margin-top:0.06in;padding-top:0.07in;border-top:1px solid var(--line2)}}
.rules{{display:flex;flex-direction:column;gap:2px}}
.rules div{{font-size:8.7px;line-height:1.3;color:var(--muted);padding:1px 0;border-bottom:1px solid var(--line)}}
.rules div b{{color:var(--ink)}}
.rels{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.rel{{background:var(--raise);border:1px solid var(--line);border-radius:6px;padding:6px 8px}}
.rel .m{{font-size:8.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}}
.rel b{{display:block;font-size:10.5px;font-weight:800;margin:1px 0 2px;color:var(--ink)}}
.rel p{{margin:0;font-size:8.3px;line-height:1.3;color:var(--muted)}}
.foot{{position:absolute;left:0.5in;right:0.5in;bottom:0.2in;display:flex;justify-content:space-between;font-size:8px;color:var(--faint)}}
</style></head>
<body>
<div class="page">
  <div class="hero">
    <div>
      <div class="brand"><img alt="" src="data:image/png;base64,{LOGO}"><b>Karta Consulting Group</b><span>Engagement Delivery</span></div>
      <div class="eyebrow">Karta AI Engagement Workspace</div>
      <h1>{HEADLINE}</h1>
      <p class="promise">{PROMISE}</p>
      <ul class="benefits">{benefits_html()}</ul>
      <p class="proof">{PROOF}</p>
    </div>
    <div class="screen">{SCREEN}</div>
  </div>

  <div class="sec"><div class="eyebrow">A digital partner at every stage of Karta's methodology · the two highest-value workflows per stage</div></div>
  <div class="legend"><span class="tag live">Live</span>in the workspace today <span class="tag skill">Skill</span>today in a consultant's Claude session, joins the workspace later <span class="tag next">Next</span>the 90-day push <span class="tag later">Later</span>roadmap</div>
  <div class="stages">{stages_html()}</div>

  <div class="bottom">
    <div><div class="eyebrow" style="margin-bottom:6px">How it stays under control</div><div class="rules">{rules_html()}</div></div>
    <div><div class="eyebrow" style="margin-bottom:6px">The next 90 days · Project Status Reporting first, one release a month</div><div class="rels">{releases_html()}</div></div>
  </div>
  <div class="foot"><span>The screen is illustrative and shows planned capabilities beside live ones; the engagement, people and decisions on it are examples. Release contents are the working plan and will be confirmed at each monthly review.</span><span>September 2026 · Karta AI strategy</span></div>
</div>
</body></html>
'''
(HERE / "engagement-workspace-onepager.html").write_text(HTML)
print("built", len(HTML))
