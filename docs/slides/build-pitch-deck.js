const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
const INK="113A2A", SALEM="2A654E", STONE="979187", MUTED="6E6961", LINE="C9C5BE", LINE2="E4E2DE", SOFT="EAF1ED", RAISE="F5F4F2", WHITE="FFFFFF", AMBER="9A6B1F", RED="A63D30";
const F="Arial";
const logoGreen = fs.readFileSync("/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-delivery-workspace/design/brand/karta-k-green.png").toString("base64");
const logoWhite = fs.readFileSync("/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-delivery-workspace/design/brand/karta-k-white.png").toString("base64");
let n = 0;
function T(s, text, o){ s.addText(text, Object.assign({ fontFace: F, isTextBox: true, margin: 0 }, o)); }
function chrome(s, dark){
  n++;
  s.background = { color: dark ? INK : WHITE };
  s.addImage({ data: "image/png;base64," + (dark ? logoWhite : logoGreen), x: 0.5, y: 0.42, w: 0.34, h: 0.34 });
  T(s, "KARTA CONSULTING GROUP", { x: 0.95, y: 0.44, w: 4, h: 0.3, fontSize: 9.5, bold: true, color: dark ? WHITE : INK, charSpacing: 2 });
  T(s, "Karta AI Engagement Workspace · September 12, 2026", { x: 7.3, y: 0.44, w: 5.5, h: 0.3, fontSize: 9.5, color: dark ? "B7C9BF" : STONE, align: "right" });
  T(s, String(n), { x: 12.5, y: 6.95, w: 0.4, h: 0.3, fontSize: 9, color: dark ? "B7C9BF" : STONE, align: "right" });
}
function title(s, text, dark){ T(s, text, { x: 0.5, y: 1.05, w: 12.3, h: 0.9, fontSize: 30, bold: true, color: dark ? WHITE : INK, valign: "top" }); }
function lede(s, text, dark, y){ T(s, text, { x: 0.5, y: y || 1.95, w: 10.5, h: 0.7, fontSize: 14, color: dark ? "D6E2DB" : MUTED, valign: "top" }); }
function card(s, x, y, w, h, head, body, opts){
  opts = opts || {};
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: opts.fill || WHITE }, line: { color: opts.line || LINE2, width: 1, dashType: opts.dash ? "dash" : "solid" } });
  let yy = y + 0.2;
  if (opts.num){ s.addShape(pres.shapes.OVAL, { x: x + 0.22, y: yy, w: 0.36, h: 0.36, fill: { color: SALEM }, line: { color: SALEM } });
    T(s, String(opts.num), { x: x + 0.22, y: yy, w: 0.36, h: 0.36, fontSize: 11, bold: true, color: WHITE, align: "center", valign: "middle" }); yy += 0.48; }
  if (opts.eyebrow){ T(s, opts.eyebrow, { x: x + 0.22, y: yy, w: w - 0.44, h: 0.22, fontSize: 8.5, bold: true, color: opts.eyebrowColor || SALEM, charSpacing: 1.5 }); yy += 0.26; }
  T(s, head, { x: x + 0.22, y: yy, w: w - 0.44, h: opts.headH || 0.5, fontSize: opts.headSize || 14, bold: true, color: INK, valign: "top" }); yy += (opts.headH || 0.5);
  if (body) T(s, body, { x: x + 0.22, y: yy, w: w - 0.44, h: y + h - yy - 0.15, fontSize: opts.bodySize || 11, color: MUTED, valign: "top" });
}
function bullets(s, items, o){
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6 } })), Object.assign({ fontFace: F, isTextBox: true, fontSize: 13, color: INK, valign: "top" }, o));
}
function arrow(s, x1, y1, x2, y2, acc){
  s.addShape(pres.shapes.LINE, { x: Math.min(x1,x2), y: Math.min(y1,y2), w: Math.abs(x2-x1), h: Math.abs(y2-y1), flipH: x2 < x1, flipV: y2 < y1, line: { color: acc ? SALEM : STONE, width: acc ? 1.75 : 1.25, endArrowType: "triangle" } });
}

// 1 Title
{ const s = pres.addSlide(); chrome(s, true);
  T(s, "Karta AI Engagement Workspace", { x: 0.5, y: 2.2, w: 12, h: 0.9, fontSize: 40, bold: true, color: WHITE });
  T(s, "Bringing our AI strategy into the daily work of every project team", { x: 0.5, y: 3.15, w: 11, h: 0.7, fontSize: 20, color: "D6E2DB" });
  T(s, "A common place for consultants to use AI with the project context, Karta methodology and governance needed to improve delivery.", { x: 0.5, y: 4.0, w: 9.5, h: 0.8, fontSize: 14, color: "B7C9BF" });
  T(s, "Status and showcase for Will Evans and Paul Gregov · Sean Bradley · Friday, September 12, 2026", { x: 0.5, y: 6.3, w: 11, h: 0.4, fontSize: 11, color: "B7C9BF" });
  s.addNotes("The Karta AI Engagement Workspace brings our AI strategy into the daily work of each project team. It gives consultants a common place to use AI with the project context, Karta methodology, and governance needed to improve delivery."); }

// 2 Situation, complication, resolution on one page
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "Our AI strategy needs a home inside every engagement");
  const cols = [
    ["SITUATION", "The strategy is set and the work is real",
     ["Strengthen our consultants, improve client delivery, reduce repetitive effort.", "Meaningful experimentation and promising capabilities are already underway."], false],
    ["COMPLICATION", "Context is scattered, and every new capability makes that worse",
     ["The plan is in Asana, documents in SharePoint, the rest in meetings and people's heads. Consultants rebuild it for every status, design and handover.", "Each AI capability needs that same context, and teams need to know what is ready, when to use it, and how to review it."], false],
    ["RESOLUTION", "One workspace per engagement, on a shared Karta foundation",
     ["Where the engagement stands in Karta's lifecycle, what needs attention, and which capabilities help next.", "Project evidence, delivery guidance and reviewed outputs in one consistent experience. Improve it once, and every project benefits."], true]];
  cols.forEach((c, i) => { const x = 0.5 + i * 4.15, w = 3.95, y = 2.15, h = 3.55, acc = c[3];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: acc ? SOFT : WHITE }, line: { color: acc ? SALEM : LINE2, width: acc ? 1.25 : 1 } });
    T(s, c[0], { x: x + 0.25, y: y + 0.22, w: w - 0.5, h: 0.24, fontSize: 9, bold: true, color: SALEM, charSpacing: 1.5 });
    T(s, c[1], { x: x + 0.25, y: y + 0.5, w: w - 0.5, h: 0.95, fontSize: acc ? 17 : 16, bold: true, color: INK, valign: "top" });
    s.addText(c[2].map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < c[2].length - 1, paraSpaceAfter: 8 } })), { x: x + 0.25, y: y + 1.5, w: w - 0.5, h: h - 1.7, fontFace: F, isTextBox: true, fontSize: 12, color: acc ? INK : MUTED, valign: "top" });
    if (i < 2) arrow(s, x + w, y + 1.0, x + w + 0.2, y + 1.0, true); });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 5.95, w: 12.33, h: 0.8, rectRadius: 0.1, fill: { color: RAISE }, line: { color: LINE2, width: 1 } });
  T(s, "The opportunity now is to turn the activity already underway into reusable ways of working that Karta can support, measure and scale.", { x: 0.75, y: 6.05, w: 11.8, h: 0.6, fontSize: 14, bold: true, color: INK, valign: "middle" });
  s.addNotes("Our AI strategy focuses on strengthening our consultants, improving client delivery, and reducing repetitive effort. We already have meaningful experimentation and promising capabilities underway. The opportunity now is to turn that activity into reusable ways of working that Karta can support, measure, and scale.\n\nToday, understanding an engagement takes effort. The plan is in Asana, documents are in SharePoint, and important context lives in meetings and individual knowledge. Consultants repeatedly gather and interpret that information to prepare a status report, develop a design, or bring another team member up to speed. As we introduce more AI capabilities, each needs relevant project context. Our teams also need to understand which capabilities are ready, when to use them, and how to review the results.\n\nThe Engagement Workspace gives each project its own home for that work."); }

// 4 The workspace
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "The Engagement Workspace gives each project its own home for that work");
  lede(s, "One workspace per engagement, on a shared foundation we improve across projects as we learn.");
  // journey strip
  const stages = ["Project Planning","Foundations","Build","Test","Train","Deploy","Continuous Support"];
  stages.forEach((st, i) => { const x = 0.5 + i * 1.77; const cur = i === 2;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.96, w: 1.67, h: 0.62, rectRadius: 0.08, fill: { color: cur ? SALEM : WHITE }, line: { color: cur ? SALEM : LINE, width: 1 } });
    T(s, (i + 1) + "  " + st, { x: x + 0.1, y: 2.96, w: 1.5, h: 0.62, fontSize: 10, bold: true, color: cur ? WHITE : INK, valign: "middle" }); });
  T(s, "KARTA'S DELIVERY LIFECYCLE · WHERE THE ENGAGEMENT STANDS", { x: 0.5, y: 2.7, w: 8, h: 0.22, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  const cols = [["What needs attention", "Milestones past their date, open high-priority items, missing sources and unconfirmed dates, calculated from the evidence, not typed in."],["Which capabilities can help next", "Weekly Status, sprint review preparation, meeting capture, UAT preparation, each placed on the stage where it belongs and labelled by readiness."],["Evidence, guidance and reviewed outputs", "Project evidence from the systems of record, Karta's delivery guidance for the current stage, and the approved outputs, all in one consistent experience."]];
  cols.forEach((c, i) => card(s, 0.5 + i * 4.15, 3.75, 3.95, 2.35, c[0], c[1], { headSize: 14, bodySize: 11.5, headH: 0.55 }));
  T(s, "Each engagement has its own workspace. The shared foundation lets us improve the experience across projects as we learn.", { x: 0.5, y: 6.3, w: 12.33, h: 0.4, fontSize: 12.5, color: MUTED, italic: true });
  s.addNotes("The Engagement Workspace gives each project its own home for that work. A team member can see where the engagement stands in Karta's delivery lifecycle, what needs attention, and which capabilities can help with the next activity. The workspace brings together project evidence, delivery guidance, and reviewed outputs in a consistent experience. Each engagement has its own workspace. The shared foundation lets us improve that experience across projects as we learn."); }

// 4b One-page showcase (mirrors docs/one-pager/engagement-workspace-onepager.pdf; stands alone)
{ const s = pres.addSlide(); chrome(s, false);
  const shot = fs.readFileSync("/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-delivery-workspace/docs/one-pager/engagement-workspace-home-sample.png").toString("base64");
  const L = 0.5, LW = 5.95;
  T(s, "KARTA AI ENGAGEMENT WORKSPACE", { x: L, y: 0.92, w: LW, h: 0.22, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  T(s, "Open Monday already knowing where your engagement stands.", { x: L, y: 1.14, w: LW, h: 0.95, fontSize: 24, bold: true, color: INK, valign: "top" });
  s.addText([{ text: "Every Karta engagement gets its own AI-enabled workspace. Claude " }, { text: "reads the engagement's evidence", options: { bold: true, color: INK } }, { text: ", " }, { text: "drafts Karta's artifacts", options: { bold: true, color: INK } }, { text: " and " }, { text: "remembers every decision", options: { bold: true, color: INK } }, { text: ", inside Karta's method and with a named person accountable for every output." }],
    { x: L, y: 2.1, w: LW, h: 0.58, fontFace: F, isTextBox: true, margin: 0, fontSize: 10.5, color: MUTED, valign: "top" });
  const ben = [["A", "See where you stand", "The lifecycle, the next control point, and whether its evidence is ready."],
               ["B", "Know what needs attention", "Slipped dates, open decisions, capacity gaps. Calculated, not typed."],
               ["C", "Do the week's work without rebuilding context", "Status, sprint reviews and UAT scripts drafted from one approved record."],
               ["D", "One door for every AI capability", "Each has an owner, a readiness label and a stage. Use and corrections are measured."]];
  ben.forEach((b, i) => { const y = 2.72 + i * 0.4;
    s.addShape(pres.shapes.OVAL, { x: L, y: y + 0.02, w: 0.26, h: 0.26, fill: { color: SALEM }, line: { color: SALEM } });
    T(s, b[0], { x: L, y: y + 0.02, w: 0.26, h: 0.26, fontSize: 9.5, bold: true, color: WHITE, align: "center", valign: "middle" });
    T(s, b[1], { x: L + 0.36, y, w: LW - 0.36, h: 0.2, fontSize: 11.5, bold: true, color: INK });
    T(s, b[2], { x: L + 0.36, y: y + 0.19, w: LW - 0.36, h: 0.2, fontSize: 8.5, color: MUTED }); });
  s.addText([{ text: "Real, and running. ", options: { bold: true, color: INK } }, { text: "Live for Legend since September 8, 2026. First Weekly Status approved and the deck built the next day. A new engagement is set up in about ten minutes." }],
    { x: L, y: 4.34, w: LW, h: 0.34, fontFace: F, isTextBox: true, margin: 0, fontSize: 9, color: MUTED, valign: "top" });
  // screenshot with callouts
  const IX = 6.75, IY = 0.95, IW = 6.08, IH = IW * 780 / 1440;
  s.addImage({ data: "image/png;base64," + shot, x: IX, y: IY, w: IW, h: IH, rounding: false });
  [["A", 35.4, 16.0], ["B", 49.3, 25.2], ["C", 48.4, 63.0], ["D", 8.1, 50.5]].forEach(c => { const cx = IX + IW * c[1] / 100, cy = IY + IH * c[2] / 100;
    s.addShape(pres.shapes.OVAL, { x: cx - 0.15, y: cy - 0.15, w: 0.3, h: 0.3, fill: { color: SALEM }, line: { color: WHITE, width: 1.75 } });
    T(s, c[0], { x: cx - 0.15, y: cy - 0.15, w: 0.3, h: 0.3, fontSize: 10, bold: true, color: WHITE, align: "center", valign: "middle" }); });
  // lifecycle
  function tag(x, y, kind){ const k = { live: ["Live", SALEM, WHITE, SALEM], skill: ["Skill", WHITE, SALEM, SALEM], next: ["Next", WHITE, AMBER, AMBER], later: ["Later", WHITE, STONE, WHITE] }[kind];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 0.42, h: 0.17, rectRadius: 0.03, fill: { color: k[1] }, line: { color: k[3], width: 0.75 } });
    T(s, k[0].toUpperCase(), { x, y, w: 0.42, h: 0.17, fontSize: 6, bold: true, color: k[2], align: "center", valign: "middle", charSpacing: 1 }); }
  T(s, "A DIGITAL PARTNER AT EVERY STAGE · THE TWO HIGHEST-VALUE WORKFLOWS PER STAGE", { x: 0.5, y: 4.8, w: 6.2, h: 0.2, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  const leg = [["live", "in the workspace today"], ["skill", "in a Claude session today"], ["next", "the 90-day push"], ["later", "roadmap"]];
  let lx = 6.7; leg.forEach(l => { const lw = l[1].length * 0.05 + 0.05; tag(lx, 4.81, l[0]); T(s, l[1], { x: lx + 0.46, y: 4.79, w: lw, h: 0.2, fontSize: 7.5, color: MUTED, valign: "middle" }); lx += 0.46 + lw + 0.1; });
  const stages = [["Sales to Delivery", "handover", true, [["Sales Handover package", "later"], ["Kick-off deck, first two weeks", "later"]]],
                  ["Project Planning", "align · kick off", false, [["Engagement setup, access check", "live"], ["Data intake coordination", "later"]]],
                  ["Foundations", "requirements · design", false, [["Meeting closeout to requirements", "next"], ["Design-to-scope reconciliation", "later"]]],
                  ["Build", "model · reports", false, [["Weekly Status", "live"], ["Sprint review preparation", "next"]]],
                  ["Test", "UAT · sign-off", false, [["UAT scripts from requirements", "skill"], ["Defect intake and triage", "later"]]],
                  ["Train & Deploy", "training · cutover", false, [["Role-based training material", "skill"], ["Go-live package and closeout", "later"]]],
                  ["Continuous Support", "handover · triage", true, [["Support handover, open items", "later"], ["Issue triage, recurring analysis", "later"]]]];
  const SW = 1.66, SG = 0.118;
  stages.forEach((st, i) => { const x = 0.5 + i * (SW + SG), y = 5.06;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: SW, h: 0.46, rectRadius: 0.06, fill: { color: st[2] ? SALEM : INK }, line: { color: st[2] ? SALEM : INK } });
    T(s, st[0], { x: x + 0.1, y: y + 0.05, w: SW - 0.2, h: 0.22, fontSize: 10, bold: true, color: WHITE });
    T(s, st[1], { x: x + 0.1, y: y + 0.26, w: SW - 0.2, h: 0.16, fontSize: 7.5, color: "B7C9BF" });
    st[3].forEach((wf, k) => { const wy = y + 0.54 + k * 0.34;
      T(s, wf[0], { x: x + 0.02, y: wy, w: SW - 0.5, h: 0.3, fontSize: 8.5, bold: true, color: INK, valign: "middle" });
      tag(x + SW - 0.42, wy + 0.065, wf[1]);
      s.addShape(pres.shapes.LINE, { x, y: wy + 0.32, w: SW, h: 0, line: { color: LINE2, width: 0.75 } }); }); });
  // control rules + releases
  T(s, "HOW IT STAYS UNDER CONTROL", { x: 0.5, y: 6.35, w: 4.6, h: 0.2, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  const rules = [["Reads as the person looking.", " No shared logins."], ["A named person approves.", " Every client output carries a name and time."], ["Nothing sent by software.", " People decide and send."], ["Unknown is never Green.", " Missing evidence is shown as missing."]];
  s.addText(rules.flatMap((r, i) => [{ text: r[0], options: { bold: true, color: INK } }, { text: r[1], options: { color: MUTED, breakLine: i < rules.length - 1 } }]),
    { x: 0.5, y: 6.55, w: 4.6, h: 0.56, fontFace: F, isTextBox: true, margin: 0, fontSize: 8, color: MUTED, valign: "top", paraSpaceAfter: 1 });
  T(s, "THE NEXT 90 DAYS · PROJECT STATUS REPORTING FIRST, ONE RELEASE A MONTH", { x: 5.3, y: 6.35, w: 7.2, h: 0.2, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  const rel = [["OCTOBER · Foundation", "Weekly Status every Friday on two engagements. Ask Claude live. Capability catalog with owners and readiness."],
               ["NOVEMBER · Context", "Granola notes and Harvest capacity read into attention items and answers. Drafting tuned from measured corrections."],
               ["DECEMBER · Beyond status", "Sprint review preparation live in Build. First Foundations Package piece. The evidence for the scale decision."]];
  rel.forEach((r, i) => { const x = 5.3 + i * 2.42;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 6.56, w: 2.3, h: 0.52, rectRadius: 0.05, fill: { color: RAISE }, line: { color: LINE2, width: 0.75 } });
    T(s, r[0], { x: x + 0.1, y: 6.59, w: 2.1, h: 0.15, fontSize: 7.5, bold: true, color: SALEM, charSpacing: 1 });
    T(s, r[1], { x: x + 0.1, y: 6.73, w: 2.1, h: 0.34, fontSize: 7, color: MUTED, valign: "top" }); });
  T(s, "The screen is the workspace running on sample data; the engagement, people and decisions on it are fictional.", { x: 0.5, y: 7.16, w: 11.5, h: 0.18, fontSize: 7, color: STONE, italic: true });
  s.addNotes("This page stands alone as the showcase. Every Karta engagement gets its own AI-enabled workspace. Claude reads the engagement's evidence, drafts Karta's artifacts and remembers every decision, inside Karta's method and with a named person accountable for every output.\n\nThe screen is the real workspace Home page running on sample data (Northwind Foods, a fictional Anaplan FP&A engagement in Build week 10): the seven-stage journey, the next control point with its evidence, stage deliverables, the capabilities recommended for this stage, what needs attention, and the evidence and decisions on record.\n\nWhy each stage matters: Sales to Delivery starts the record the whole engagement will use. Project Planning: everything after it depends on setup being right. Foundations catches ambiguity and scope drift before build. Build is weekly, measurable and traceable as a by-product. Test: coverage comes free and scope disputes get settled. Train and Deploy: the longest deliverables, drafted from the solution. Continuous Support inherits the memory, not a folder.\n\nTags: Live is in the workspace today. Skill runs today in a consultant's Claude session and joins the workspace later. Next is the 90-day push. Later is roadmap. Release contents are the working plan and will be confirmed at each monthly review."); }

// 5 Imagine
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "Imagine opening your engagement workspace at the start of the week");
  const steps = [["Orient", "See the current stage, the milestones and what information is missing."],["Open Weekly Status", "The workspace reads the available evidence from Asana and SharePoint, as you."],["Draft", "One click. Claude prepares a draft narrative and suggests a status for each area."],["Review and approve", "A reviewer applies their judgment, corrects the content and approves under their own name."],["Deck and record", "The workspace produces the KCG status deck and retains the approved record, with who and when."]];
  steps.forEach((st, i) => { const x = 0.5 + i * 2.5; card(s, x, 2.2, 2.3, 2.6, st[0], st[1], { num: i + 1, headSize: 14, bodySize: 11.5 }); if (i < 4) arrow(s, x + 2.3, 3.5, x + 2.5, 3.5, true); });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 5.1, w: 12.33, h: 1.3, rectRadius: 0.1, fill: { color: SOFT }, line: { color: SALEM, width: 1 } });
  T(s, "WHAT STAYS WITH PEOPLE", { x: 0.75, y: 5.25, w: 5, h: 0.25, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  T(s, "Judgment, correction and approval. Nothing reaches a client that a named person did not approve, and nothing is sent by software. Dates, status colors and the file itself are produced by code, not by the model. Missing evidence is shown as missing, never as good news.", { x: 0.75, y: 5.5, w: 11.8, h: 0.85, fontSize: 12.5, color: INK });
  s.addNotes("Imagine opening your engagement workspace at the start of the week. You can orient yourself to the current stage, review milestones and missing information, and open Weekly Status. The workspace reads the available evidence and helps prepare a draft. A reviewer applies their judgment, corrects the content, and approves it. The workspace then produces the deck and retains the approved record."); }

// 6 Where we are
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "This is running today");
  lede(s, "We have recorded an approved status and generated the deck for Legend. That gives us a concrete starting point for demonstrating the experience and measuring its value.");
  const facts = [["Legend · Continuous Support", "First engagement workspace live. Weekly Status version 1 approved on September 9 and the deck built the same day."],["Gates 0 to 6 closed", "Proof of concept, connector spike, contracts, deck builder, Weekly Status end to end, home screen, pilot readiness. Each proved before the next began."],["About ten minutes", "To stand up a new engagement from the blank template: names, the owner, and links to Asana, SharePoint, Granola and Harvest."],["A second workspace in a cold test", "Two colleagues who have not seen it before are setting one up to show us where the gaps are."]];
  facts.forEach((f, i) => card(s, 0.5 + (i % 2) * 6.2, 2.95 + Math.floor(i / 2) * 1.65, 6.1, 1.5, f[0], f[1], { headSize: 14, bodySize: 11.5 }));
  T(s, "Today the reviewer saves and distributes the deck. Once IT approves a one-time consent, the deck saves straight into the engagement's SharePoint folder as the reviewer.", { x: 0.5, y: 6.3, w: 12.33, h: 0.45, fontSize: 12, color: MUTED, italic: true });
  s.addNotes("We have already recorded an approved status and generated deck for Legend. Today, the reviewer saves and distributes that deck. That gives us a concrete starting point for demonstrating the experience and measuring its value."); }

// 7 Two priorities
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "Our first two priorities show how the workspace supports different parts of delivery");
  card(s, 0.5, 2.15, 6.05, 3.0, "Project Status Reporting", "A recurring activity with measurable preparation effort and clear reuse across engagements.\n\nEvidence read as the consultant, a drafted narrative, deterministic status, a named approval, and a deck on the KCG template. Live for Legend; weekly on two engagements through the pilot.", { eyebrow: "PRIORITY 1 · EVERY STAGE", headSize: 17, headH: 0.55, bodySize: 12 });
  card(s, 6.78, 2.15, 6.05, 3.0, "The Foundations Package", "From business requirements to mockups, addressing ambiguity before build.\n\nMakes requirements, assumptions, decisions and scope boundaries visible so teams can identify gaps and improve the handoff into development. The Mockup Generator is the first piece already in use.", { eyebrow: "PRIORITY 2 · FOUNDATIONS", headSize: 17, headH: 0.55, bodySize: 12 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 5.4, w: 12.33, h: 1.15, rectRadius: 0.1, fill: { color: RAISE }, line: { color: LINE2, width: 1 } });
  T(s, "The workspace gives these capabilities a place in the engagement journey. Some run directly inside it; others may first connect to guided workflows in a consultant's Claude session. Over time, reviewed outputs from one activity inform the next, so context is not rebuilt.", { x: 0.75, y: 5.55, w: 11.8, h: 0.85, fontSize: 12.5, color: INK, valign: "middle" });
  s.addNotes("Our first two priorities show how the workspace can support different parts of delivery. Project Status Reporting addresses a recurring activity with measurable preparation effort and clear reuse across engagements. The Foundations Package, from business requirements to mockups, addresses ambiguity before build. It helps make requirements, assumptions, decisions, and scope boundaries visible so teams can identify gaps and improve the handoff into development. The workspace gives these capabilities a place in the engagement journey. Some will run directly inside it; others may initially connect to guided workflows in a consultant's Claude session. Over time, reviewed outputs from one activity can help inform subsequent work, reducing the need to reconstruct context."); }

// 8 Governance at Karta level
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "As we integrate more AI, governance matters more, not less");
  lede(s, "At the Karta level: a consistent process for deciding which opportunities receive investment, which enter a pilot, and which are ready to scale.");
  const stages = [["Idea", "Any employee can contribute one."],["Invest", "Worth building? A named owner and defined boundaries."],["Pilot", "Proven on a real engagement, with evidence gathered."],["Scale", "Turned on for others, with readiness set to Validated."]];
  stages.forEach((st, i) => { const x = 0.5 + i * 3.1; card(s, x, 2.95, 2.9, 1.7, st[0], st[1], { num: i + 1, headSize: 15, bodySize: 11.5 }); if (i < 3) arrow(s, x + 2.9, 3.8, x + 3.1, 3.8, true); });
  T(s, "EVERY CAPABILITY WE FORMALLY ADVANCE NEEDS", { x: 0.5, y: 4.95, w: 8, h: 0.22, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  const needs = [["An owner", "accountable for it"],["Defined boundaries", "what it does and does not do"],["Evidence of value", "and of quality"],["Adoption", "sustained, unprompted use"],["Acceptable risk", "reviewed and understood"]];
  needs.forEach((nd, i) => { const x = 0.5 + i * 2.5; s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 5.25, w: 2.3, h: 1.1, rectRadius: 0.08, fill: { color: SOFT }, line: { color: SALEM, width: 1 } }); T(s, nd[0], { x: x + 0.15, y: 5.35, w: 2.0, h: 0.4, fontSize: 13, bold: true, color: INK }); T(s, nd[1], { x: x + 0.15, y: 5.75, w: 2.0, h: 0.5, fontSize: 11, color: MUTED }); });
  s.addNotes("As we integrate more AI, governance becomes increasingly important. At the Karta level, we need a consistent process for deciding which opportunities receive investment, which enter a pilot, and which are ready to scale. Any employee can contribute an idea. Each capability we formally advance needs an owner, defined boundaries, and evidence of value, quality, adoption, and acceptable risk."); }

// 9 Governance in everyday delivery
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "The workspace is where governance becomes part of everyday delivery");
  lede(s, "Teams should know which capabilities are available for their engagement, whether each is experimental or validated, what information it uses, and what review is required.");
  const have = [["Named approval records", "Every approved status carries the reviewer's name, email and time."],["Visible source gaps", "A missing source or an unknown date is shown, recorded with the deck, and never turned Green."],["Readiness labels", "Piloted, Experimental, Validated, on every capability in the catalog."],["Pilot measures", "Time to approval, corrections to the draft, assessments overridden, errors after approval, adoption."]];
  T(s, "ALREADY IN PLACE", { x: 0.5, y: 2.85, w: 6, h: 0.22, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  have.forEach((h, i) => card(s, 0.5 + (i % 2) * 3.12, 3.12 + Math.floor(i / 2) * 1.5, 3.0, 1.38, h[0], h[1], { headSize: 12.5, bodySize: 10.5, headH: 0.4 }));
  T(s, "GOVERNANCE CONTINUES AFTER RELEASE", { x: 7.0, y: 2.85, w: 6, h: 0.22, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.0, y: 3.12, w: 5.83, h: 2.88, rectRadius: 0.1, fill: { color: SOFT }, line: { color: SALEM, width: 1 } });
  bullets(s, ["Where people use a capability, and where they do not", "What they correct, and how often", "What issues arise after approval", "Whether the workflow is getting better week over week"], { x: 7.25, y: 3.3, w: 5.4, h: 1.7, fontSize: 12.5 });
  T(s, "That evidence lets us refine capabilities, expand the successful ones, or withdraw those that do not meet expectations. We will strengthen enforcement and oversight as adoption grows.", { x: 7.25, y: 5.0, w: 5.4, h: 0.9, fontSize: 11.5, color: MUTED });
  s.addNotes("The Engagement Workspace is where those governance decisions become part of everyday delivery. Our intent is for teams to understand which capabilities are available for their engagement, whether they are experimental or validated, what information they use, and what review is required. We already have elements of that foundation: named approval records, visible source gaps, capability readiness labels, and pilot measures. We will strengthen enforcement and oversight as adoption grows. Governance also continues after release. We need to see where people use a capability, what they correct, what issues arise, and whether the workflow improves. That evidence lets us refine capabilities, expand successful ones, or withdraw those that do not meet expectations."); }

// 10 What makes this Karta's
{ const s = pres.addSlide(); chrome(s, true);
  title(s, "What makes this Karta's is how we combine AI with our delivery expertise", true);
  const pts = [["Our methodology shapes the capabilities", "The seven-stage lifecycle, our templates and our review practices decide how each capability works, not the other way round."],["Established systems stay authoritative", "Asana, SharePoint and the rest remain the record. The workspace reads them as the person looking and never becomes a competing source of truth."],["Missing evidence stays visible", "Unknown is a status. A gap is recorded with the deck. Nothing defaults to good news."],["People stay accountable", "A named reviewer approves every client-facing output. Software produces; people decide and send."]];
  pts.forEach((p, i) => { const x = 0.5 + (i % 2) * 6.2, y = 2.2 + Math.floor(i / 2) * 1.55;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 6.1, h: 1.4, rectRadius: 0.1, fill: { color: "1A4A37" }, line: { color: "2F6B4E", width: 1 } });
    T(s, p[0], { x: x + 0.22, y: y + 0.18, w: 5.7, h: 0.4, fontSize: 14, bold: true, color: WHITE }); T(s, p[1], { x: x + 0.22, y: y + 0.6, w: 5.7, h: 0.75, fontSize: 11.5, color: "D6E2DB" }); });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 5.45, w: 12.33, h: 1.15, rectRadius: 0.1, fill: { color: "6FB08D" }, line: { color: "6FB08D", width: 1 } });
  T(s, "DEVELOPING OUR CONSULTANTS", { x: 0.75, y: 5.58, w: 5, h: 0.25, fontSize: 8.5, bold: true, color: INK, charSpacing: 1.5 });
  T(s, "Experienced colleagues turn effective practices into reusable guidance. Junior colleagues apply that guidance in real work and develop their judgment through coaching and reviewer feedback.", { x: 0.75, y: 5.85, w: 11.8, h: 0.7, fontSize: 13, color: INK });
  s.addNotes("What makes this Karta's is how we combine AI with our delivery expertise. Our methodology, templates, and review practices shape how the capabilities work. Established systems remain authoritative, missing evidence stays visible, and people remain accountable for client-facing outputs. This also supports the development of our consultants. Experienced colleagues can turn effective practices into reusable guidance. Junior colleagues can apply that guidance in real work and develop their judgment through coaching and reviewer feedback."); }

// 11 Next 90 days
{ const s = pres.addSlide(); chrome(s, false);
  title(s, "The next 90 days are about proving this works beyond the initial demonstration");
  const cols = [["Validate the two priority workflows", "Weekly Status every week on two engagements. The Foundations Package from requirements to mockups on a live engagement."],["Establish the minimum governance and operating foundation", "The capability pipeline, owners and readiness labels in the catalog, the stand-up and onboarding processes, Karta-owned code and hosting."],["Develop practitioner capability through participation", "Consultants run the workflows, correct the drafts, and their corrections shape the next version."]];
  cols.forEach((c, i) => card(s, 0.5 + i * 4.15, 2.15, 3.95, 2.25, c[0], c[1], { num: i + 1, headSize: 14, bodySize: 11.5, headH: 0.75 }));
  T(s, "WHAT WE WILL MEASURE", { x: 0.5, y: 4.65, w: 6, h: 0.22, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
  const m = [["Preparation effort", "minutes from draft to approval"],["Output quality", "errors found after approval"],["Corrections", "how much of the draft a reviewer changed"],["Sustained use", "approvals and distinct reviewers, week over week"]];
  m.forEach((x, i) => { const px = 0.5 + i * 3.1; s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px, y: 4.92, w: 2.9, h: 1.15, rectRadius: 0.08, fill: { color: SOFT }, line: { color: SALEM, width: 1 } }); T(s, x[0], { x: px + 0.18, y: 5.03, w: 2.55, h: 0.4, fontSize: 13.5, bold: true, color: INK }); T(s, x[1], { x: px + 0.18, y: 5.45, w: 2.55, h: 0.55, fontSize: 11, color: MUTED }); });
  T(s, "Those results tell us what to scale, what to change, and where to focus next. The workspace records them automatically; nobody keeps a spreadsheet.", { x: 0.5, y: 6.25, w: 12.33, h: 0.45, fontSize: 12.5, color: MUTED, italic: true });
  s.addNotes("The next 90 days are about proving that this works beyond the initial demonstration. We will validate the two priority workflows, establish the minimum governance and operating foundation, and develop practitioner capability through participation. We will measure preparation effort, output quality, corrections, and sustained use. Those results will tell us what to scale, what to change, and where to focus next."); }

// 12 Close
{ const s = pres.addSlide(); chrome(s, true);
  T(s, "A common place for our consultants to apply AI.\nA consistent way for Karta to introduce, govern and improve it.", { x: 0.5, y: 2.1, w: 12.3, h: 1.6, fontSize: 28, bold: true, color: WHITE });
  T(s, "Our ambition is for every engagement to benefit from Karta's collective expertise, supported by AI and accountable human judgment.", { x: 0.5, y: 3.9, w: 10.5, h: 0.9, fontSize: 17, color: "D6E2DB" });
  T(s, "THIS MONTH", { x: 0.5, y: 5.2, w: 4, h: 0.25, fontSize: 8.5, bold: true, color: "6FB08D", charSpacing: 1.5 });
  bullets(s, ["Weekly Status every week on Legend and the second engagement", "IT consent, so decks save to SharePoint on their own and new members connect without a prompt", "Karta-owned GitHub and Google Cloud accounts, approved September 9, set up with Marianna"], { x: 0.5, y: 5.45, w: 12, h: 1.2, fontSize: 12.5, color: WHITE });
  s.addNotes("The Engagement Workspace gives our consultants a common place to apply AI and gives Karta a consistent way to introduce, govern, and improve those capabilities. Our ambition is for every engagement to benefit from Karta's collective expertise, supported by AI and accountable human judgment."); }

const out = "/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-delivery-workspace/docs/slides/engagement-workspace-pitch.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out));
