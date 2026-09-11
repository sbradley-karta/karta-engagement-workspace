// AI strategy weekly status: one clean slide. Build with node (pptxgenjs 3.12). Output beside this file.
// Content is the draft for the first weekly status, Friday September 12, 2026. Edit the arrays below week to week.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
const INK="113A2A", SALEM="2A654E", STONE="979187", MUTED="6E6961", LINE="C9C5BE", LINE2="E4E2DE", SOFT="EAF1ED", RAISE="F5F4F2", WHITE="FFFFFF", YELLOW="D9A421", RED="5F211B";
const F="Arial";
const ROOT="/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-delivery-workspace";
const logoGreen = fs.readFileSync(ROOT+"/design/brand/karta-k-green.png").toString("base64");
function T(s, text, o){ s.addText(text, Object.assign({ fontFace: F, isTextBox: true, margin: 0 }, o)); }
function eyebrow(s, text, x, y, w){ T(s, text, { x, y, w, h: 0.2, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 }); s.addShape(pres.shapes.LINE, { x, y: y + 0.26, w, h: 0, line: { color: LINE, width: 0.75 } }); }
function pill(s, x, y, w, status, size){ const c = { Green: SALEM, Yellow: YELLOW, Red: RED }[status] || STONE;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: size || 0.24, rectRadius: 0.12, fill: { color: c }, line: { color: c } });
  T(s, status.toUpperCase(), { x, y, w, h: size || 0.24, fontSize: (size ? 10 : 7.5), bold: true, color: WHITE, align: "center", valign: "middle", charSpacing: 1 }); }
function bullets(s, items, o){ s.addText(items.map((t, i) => ({ text: t, options: { bullet: { indent: 12 }, breakLine: i < items.length - 1, paraSpaceAfter: 6 } })), Object.assign({ fontFace: F, isTextBox: true, margin: 0, fontSize: 10, color: INK, valign: "top" }, o)); }

// ---------------------------------------------------------------- content
const WEEK = "Week of September 7 to 11, 2026";
const DATE = "September 12, 2026";
const OVERALL = "Green";
const OVERALL_NOTE = "One workstream Yellow: platform accounts and IT consent.";

const DONE = [
  "Legend workspace live September 8. First Weekly Status approved and the client deck built September 9.",
  "Blank template with a non-technical setup screen. A new engagement stands up in about ten minutes.",
  "Cold test under way: two colleagues setting up a second workspace unassisted to expose the gaps.",
  "Karta GitHub and Google Cloud accounts approved September 9. Setup request sent to Marianna.",
  "One self-contained code repository with a documented operating model, solution design and showcase.",
];
const NEXT = [
  "Weekly Status every Friday on Legend and the second engagement.",
  "Fold in the cold-test findings. Re-check the Legend SharePoint link and stage dates.",
  "Karta GitHub organization and Cloud account set up. Move the repository and the assembly service.",
  "Follow up with IT on Microsoft Entra admin consent.",
  "Ethan's review of the status contracts and vocabulary.",
];
const DECISIONS = [
  ["Decision", "Confirm the 90-day release dates: October 3, October 31, December 5, scale review December 12."],
  ["Decision", "Name the second pilot engagement and its reviewer."],
  ["Risk", "Entra admin consent pending with IT. Until granted, reviewers save decks to SharePoint themselves and connector sign-in stays deferred. Interim mode is running."],
  ["Watch", "Practitioner time to run Weekly Status each week alongside client work."],
];
const WORKSTREAMS = [
  ["Engagement Workspace · Project Status Reporting", "Green", "Live for Legend. Weekly Status v1 approved and deck built. Setup, Home, Weekly Status, Config and pilot measures in place."],
  ["Foundations Package · requirements to mockups", "Green", "Mockup Generator in use. BRD, Design Deck and Integration Matrix skills in progress. Meeting closeout into requirements is the next piece."],
  ["Governance and operating model", "Green", "Capability catalog with owners and readiness labels. Named approvals recorded. Idea, Invest, Pilot, Scale pipeline defined. Protected main, pull requests and CI documented."],
  ["Platform, accounts and IT", "Yellow", "GitHub and Cloud accounts approved, setup week of September 14. Entra admin consent pending. Cloud spend to date $0.36 against a $300 credit."],
  ["Skills and practitioner enablement", "Green", "Complete: Estimator, Win Story, Industry One Pager, RFP Questions, Status Decks, RAID Log updates, Granola to Asana follow-ups. Six more in progress across Foundations and Build."],
];
const MILESTONES = [
  ["Sep 12", "Status 1", "today"],
  ["Oct 3", "Release 1 · Foundation", "Two engagements, Ask Claude, catalog"],
  ["Oct 31", "Release 2 · Context", "Granola and Harvest feed attention"],
  ["Dec 5", "Release 3 · Beyond status", "Sprint review prep, Foundations piece"],
  ["Dec 12", "Scale review", "what to scale, change, or stop"],
];

// ---------------------------------------------------------------- slide
const s = pres.addSlide();
s.background = { color: WHITE };
s.addImage({ data: "image/png;base64," + logoGreen, x: 0.5, y: 0.42, w: 0.34, h: 0.34 });
T(s, "KARTA CONSULTING GROUP", { x: 0.95, y: 0.44, w: 4, h: 0.3, fontSize: 9.5, bold: true, color: INK, charSpacing: 2 });
T(s, "AI strategy · Weekly status · " + DATE, { x: 7.3, y: 0.44, w: 5.53, h: 0.3, fontSize: 9.5, color: STONE, align: "right" });

T(s, "AI strategy: weekly status", { x: 0.5, y: 0.98, w: 9.5, h: 0.5, fontSize: 26, bold: true, color: INK });
T(s, WEEK + " · first weekly status of the 90-day push", { x: 0.5, y: 1.5, w: 8.3, h: 0.28, fontSize: 12, color: MUTED });
T(s, "OVERALL", { x: 10.4, y: 1.0, w: 0.9, h: 0.4, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5, valign: "middle", align: "right" });
pill(s, 11.43, 1.0, 1.4, OVERALL, 0.4);
T(s, OVERALL_NOTE, { x: 9.0, y: 1.48, w: 3.83, h: 0.3, fontSize: 9, color: MUTED, align: "right" });

// three columns
const CY = 2.1, CW = 3.91, CG = 0.3;
eyebrow(s, "ACCOMPLISHED THIS WEEK", 0.5, CY, CW);
bullets(s, DONE, { x: 0.5, y: CY + 0.4, w: CW, h: 2.0 });
eyebrow(s, "PLANNED NEXT WEEK", 0.5 + CW + CG, CY, CW);
bullets(s, NEXT, { x: 0.5 + CW + CG, y: CY + 0.4, w: CW, h: 2.0 });
const DX = 0.5 + 2 * (CW + CG);
eyebrow(s, "DECISIONS, RISKS AND WATCH ITEMS", DX, CY, CW);
let dy = CY + 0.4;
DECISIONS.forEach(d => { const kind = d[0], lines = Math.ceil(d[1].length / 48), h = 0.15 * lines + 0.04;
  const c = kind === "Risk" ? YELLOW : kind === "Decision" ? SALEM : STONE;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: DX, y: dy + 0.01, w: 0.68, h: 0.18, rectRadius: 0.03, fill: { color: c }, line: { color: c } });
  T(s, kind.toUpperCase(), { x: DX, y: dy + 0.01, w: 0.68, h: 0.18, fontSize: 6.5, bold: true, color: WHITE, align: "center", valign: "middle", charSpacing: 1 });
  T(s, d[1], { x: DX + 0.78, y: dy, w: CW - 0.78, h, fontSize: 9, color: INK, valign: "top" });
  dy += h + 0.1; });

// workstreams
const WY = 4.45;
eyebrow(s, "WORKSTREAMS", 0.5, WY, 3.3);
eyebrow(s, "STATUS", 3.95, WY, 0.8);
eyebrow(s, "WHERE IT STANDS", 4.95, WY, 7.88);
WORKSTREAMS.forEach((w, i) => { const y = WY + 0.36 + i * 0.32;
  T(s, w[0], { x: 0.5, y, w: 3.3, h: 0.3, fontSize: 10, bold: true, color: INK, valign: "middle" });
  pill(s, 3.95, y + 0.04, 0.8, w[1]);
  T(s, w[2], { x: 4.95, y, w: 7.88, h: 0.3, fontSize: 8.5, color: MUTED, valign: "middle" });
  s.addShape(pres.shapes.LINE, { x: 0.5, y: y + 0.31, w: 12.33, h: 0, line: { color: LINE2, width: 0.75 } }); });

// 90-day strip
const SY = 6.45;
T(s, "90-DAY PUSH · ONE RELEASE A MONTH · DATES PROPOSED, TO CONFIRM TODAY", { x: 0.5, y: SY, w: 8, h: 0.2, fontSize: 8.5, bold: true, color: SALEM, charSpacing: 1.5 });
const X0 = 1.1, X1 = 12.2, LY = SY + 0.52;
s.addShape(pres.shapes.LINE, { x: X0, y: LY, w: X1 - X0, h: 0, line: { color: LINE, width: 1 } });
MILESTONES.forEach((m, i) => { const x = X0 + (X1 - X0) * i / (MILESTONES.length - 1), today = i === 0;
  s.addShape(pres.shapes.OVAL, { x: x - 0.07, y: LY - 0.07, w: 0.14, h: 0.14, fill: { color: today ? SALEM : WHITE }, line: { color: SALEM, width: 1.25 } });
  T(s, m[0], { x: x - 1.0, y: LY - 0.32, w: 2.0, h: 0.2, fontSize: 9, bold: true, color: INK, align: "center" });
  T(s, m[1], { x: x - 1.0, y: LY + 0.12, w: 2.0, h: 0.18, fontSize: 8.5, bold: true, color: SALEM, align: "center" });
  T(s, m[2], { x: x - 1.0, y: LY + 0.3, w: 2.0, h: 0.18, fontSize: 7.5, color: MUTED, align: "center" }); });

s.addNotes("First weekly status of the AI program, " + DATE + ". Overall Green with one Yellow workstream.\n\n" +
  "Accomplished: " + DONE.join(" ") + "\n\nPlanned: " + NEXT.join(" ") + "\n\n" +
  DECISIONS.map(d => d[0] + ": " + d[1]).join("\n") + "\n\n" +
  "Workstreams: " + WORKSTREAMS.map(w => w[0] + " is " + w[1] + ". " + w[2]).join(" ") + "\n\n" +
  "The 90-day dates are proposed and should be confirmed in this meeting. Each release is reviewed at month end; contents are the working plan.");

const out = ROOT + "/docs/slides/ai-strategy-status-2026-09-12.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out));
