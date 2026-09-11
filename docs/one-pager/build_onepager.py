#!/usr/bin/env python3
"""Build the combined one-pager (engagement-workspace-onepager.html) from the data below.
Render: Chrome --headless --print-to-pdf --no-pdf-header-footer. Light page (Karta system). The screen is a
screenshot of the real workspace page running on sample data (page/make-sample-page.py), dark theme."""
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

# ---------------------------------------------------------------- screen: a screenshot of the real app with sample data
# Produce it with:  cd page && python3 make-sample-page.py && Chrome --headless=new --screenshot --window-size=1440,780
#   --force-device-scale-factor=2 file://.../page/dist/engagement-workspace-sample.html  (copy to engagement-workspace-home-sample.png)
SHOT = base64.b64encode((HERE / "engagement-workspace-home-sample.png").read_bytes()).decode()
CALLOUTS = [("A", 35.4, 16.0), ("B", 49.3, 25.2), ("C", 48.4, 63.0), ("D", 8.1, 50.5)]   # percent of the image, left and top
SCREEN = ('<div class="shot"><img alt="The engagement workspace home page for a sample engagement in Build: journey, next control point, deliverables, recommended capabilities, attention items, evidence and decisions." src="data:image/png;base64,' + SHOT + '">'
          + "".join(f'<i class="co" style="left:{x}%;top:{y}%">{k}</i>' for k, x, y in CALLOUTS) + '</div>')

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
.hero{{display:grid;grid-template-columns:1fr 6in;gap:0.4in;align-items:center;margin-bottom:0.1in}}
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
.shot{{position:relative}}
.shot img{{display:block;width:100%;height:auto;border-radius:8px;border:1px solid #2C2F2E;box-shadow:0 8px 22px rgba(17,58,42,.2)}}
.co{{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:var(--accent);border:2.5px solid #fff;color:#fff;font-style:normal;font-weight:800;font-size:13px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.35)}}
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
  <div class="foot"><span>The screen is the workspace running on sample data; the engagement, people and decisions on it are fictional, and Next marks planned capabilities beside live ones. Release contents are the working plan and will be confirmed at each monthly review.</span><span>September 2026 · Karta AI strategy</span></div>
</div>
</body></html>
'''
(HERE / "engagement-workspace-onepager.html").write_text(HTML)
print("built", len(HTML))
