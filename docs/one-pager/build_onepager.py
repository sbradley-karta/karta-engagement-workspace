#!/usr/bin/env python3
"""Build the combined one-pager (engagement-workspace-onepager.html) from data below.
Render: Chrome --headless --print-to-pdf. The screen SVG is reused from engagement-workspace-vision.html."""
import pathlib, re, base64

HERE = pathlib.Path(__file__).parent
vision = (HERE / "engagement-workspace-vision.html").read_text()
SVG = re.search(r'(<svg viewBox="0 0 760 500".*?</svg>)', vision, re.S).group(1)
LOGO = base64.b64encode((HERE / "../../design/brand/karta-k-white.png").read_bytes()).decode()

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

CALLOUTS = '''<g class="callouts">
  <circle cx="330" cy="80" r="13"/><text x="330" y="84.5">A</text>
  <circle cx="426" cy="122" r="13"/><text x="426" y="126.5">B</text>
  <circle cx="408" cy="308" r="13"/><text x="408" y="312.5">C</text>
  <circle cx="408" cy="386" r="13"/><text x="408" y="390.5">D</text>
</g>'''

SCREEN = SVG.replace('</svg>', CALLOUTS + '</svg>')

HTML = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Karta AI Engagement Workspace</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<style>
@page{{size:13.333in 7.5in;margin:0}}
:root{{--ink:#113A2A;--deep:#0C2A1E;--surface:#16452F;--raise:#1A4A37;--line:#2F6B4E;--line2:#24503C;--text:#F1F0ED;--muted:#B7C9BF;--faint:#7FA08F;--accent:#6FB08D;--soft:#1E5A42;--amber:#D6A85B;--red:#E08878;--sans:"Manrope",system-ui,-apple-system,"Segoe UI",sans-serif}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:var(--ink);height:7.5in;overflow:hidden}}
body{{width:13.333in;height:7.5in;color:var(--text);font-family:var(--sans);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{position:relative;width:13.333in;height:7.5in;padding:0.3in 0.5in 0.42in;display:flex;flex-direction:column}}
.hero{{display:grid;grid-template-columns:1fr 5.35in;gap:0.45in;align-items:center;margin-bottom:0.14in}}
.brand{{display:flex;align-items:center;gap:9px;margin-bottom:10px}}
.brand img{{width:22px;height:22px}}
.brand b{{font-size:9.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase}}
.brand span{{font-size:9.5px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;border-left:1px solid var(--line);padding-left:9px}}
.eyebrow{{font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:8px}}
h1{{font-size:29px;line-height:1.03;letter-spacing:-.03em;font-weight:800;margin:0 0 10px;text-wrap:balance}}
.promise{{font-size:11px;line-height:1.42;color:var(--muted);margin:0 0 10px}}
.promise b{{color:var(--text)}}
.benefits{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}}
.benefits li{{display:grid;grid-template-columns:22px 1fr;gap:10px;align-items:start}}
.benefits li i{{width:22px;height:22px;border-radius:50%;background:var(--accent);color:var(--ink);font-style:normal;font-weight:800;font-size:11px;display:flex;align-items:center;justify-content:center}}
.benefits b{{display:block;font-size:13px;font-weight:700;line-height:1.2}}
.benefits span{{display:block;font-size:10px;color:var(--muted);line-height:1.35;margin-top:1px}}
.proof{{margin-top:10px;font-size:9.6px;color:var(--muted);line-height:1.38}}
.proof b{{color:var(--text)}}
.screen svg{{display:block;width:100%;height:auto}}
svg text{{font-family:var(--sans)}}
.f{{fill:var(--surface);stroke:var(--line2);stroke-width:1}} .r{{fill:var(--raise);stroke:var(--line2);stroke-width:1}} .a{{fill:var(--soft);stroke:var(--accent);stroke-width:1.1}} .n{{fill:var(--accent)}}
.t{{fill:var(--text)}} .m{{fill:var(--muted)}} .fa{{fill:var(--faint)}} .ac{{fill:var(--accent)}} .am{{fill:var(--amber)}} .rd{{fill:var(--red)}} .ink{{fill:var(--ink)}}
.h{{font-size:11px;font-weight:700}} .h2{{font-size:15px;font-weight:800}} .s{{font-size:8px}} .s2{{font-size:8.6px}} .eb{{font-size:7px;font-weight:800;letter-spacing:.12em}} .tg{{font-size:6.6px;font-weight:800;letter-spacing:.08em}} .pill{{fill:none;stroke-width:0.9}}
.callouts circle{{fill:var(--accent);stroke:var(--ink);stroke-width:2.5}} .callouts text{{fill:var(--ink);font-size:13px;font-weight:800;text-anchor:middle}}
.sec{{display:flex;align-items:baseline;justify-content:space-between;margin:0 0 4px}}
.sec .eyebrow{{margin:0}}
.legend{{display:flex;gap:10px;align-items:center;font-size:8.4px;color:var(--muted);margin:0 0 7px;white-space:nowrap}}
.stages{{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}}
.stage .hd{{background:var(--surface);border:1px solid var(--line2);border-radius:6px;padding:5px 8px 4px;font-size:10.5px;font-weight:800;letter-spacing:-.01em;line-height:1.15;margin-bottom:6px}}
.stage .hd small{{display:block;font-size:8px;font-weight:500;color:var(--muted);margin-top:1px}}
.stage.side .hd{{background:var(--accent);color:var(--ink);border-color:var(--accent)}} .stage.side .hd small{{color:var(--ink);opacity:.8}}
.wf{{display:flex;justify-content:space-between;align-items:center;gap:6px;padding:4px 2px;border-bottom:1px solid var(--line2);font-size:9.2px;font-weight:600;line-height:1.22}}
.wf > span:first-child{{flex:1}} .wf .tag{{flex:none}}
.tag{{font-size:6.8px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;padding:2px 5px;border-radius:3px;white-space:nowrap;flex:none}}
.tag.live{{background:var(--accent);color:var(--ink)}} .tag.skill{{background:transparent;color:var(--accent);border:1px solid var(--accent)}} .tag.next{{background:transparent;color:var(--amber);border:1px solid var(--amber)}} .tag.later{{background:transparent;color:var(--faint);border:1px solid transparent;padding-left:0;padding-right:0}}
.why{{margin:5px 2px 0;font-size:8.2px;line-height:1.3;color:var(--muted)}}
.bottom{{display:grid;grid-template-columns:1fr 1.9fr;gap:0.3in;margin-top:0.1in;padding-top:0.08in;border-top:1px solid var(--line2)}}
.rules{{display:flex;flex-direction:column;gap:4px}}
.rules div{{font-size:8.7px;line-height:1.3;color:var(--muted);padding:2px 0;border-bottom:1px solid var(--line2)}}
.rules div b{{color:var(--text)}}
.rels{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.rel{{background:var(--surface);border:1px solid var(--line2);border-radius:6px;padding:6px 8px}}
.rel .m{{font-size:8.5px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}}
.rel b{{display:block;font-size:10.5px;font-weight:800;margin:1px 0 2px}}
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
