const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
const INK="113A2A", SALEM="2A654E", STONE="979187", MUTED="6E6961", LINE="C9C5BE", SOFT="EAF1ED", RAISE="F5F4F2", WHITE="FFFFFF", WARN="9A6B1F";
const F="Arial";
const s = pres.addSlide();
s.background = { color: WHITE };
const logo = fs.readFileSync("/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-delivery-workspace/design/brand/karta-k-green.png").toString("base64");
s.addImage({ data: "image/png;base64," + logo, x: 0.4, y: 0.32, w: 0.34, h: 0.34 });
s.addText("Karta Engagement Workspace: what it is and where it lives", { x: 0.85, y: 0.25, w: 10.2, h: 0.48, fontFace: F, fontSize: 22, bold: true, color: INK, isTextBox: true, margin: 0 });
s.addText("One workspace page per engagement reads the tools we already use, drafts the weekly status with Claude, and hands a finished deck to a named person who approves it. Client data stays where it lives today.", { x: 0.85, y: 0.76, w: 12.0, h: 0.42, fontFace: F, fontSize: 10.5, color: MUTED, isTextBox: true, margin: 0 });

function zone(x, y, w, h, label, karta) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: WHITE }, line: { color: karta ? SALEM : LINE, width: karta ? 1.25 : 1, dashType: karta ? "dash" : "sysDot" } });
  s.addText(label, { x: x + 0.12, y: y + 0.06, w: w - 0.24, h: 0.22, fontFace: F, fontSize: 7.5, bold: true, color: STONE, charSpacing: 1.5, isTextBox: true, margin: 0 });
}
function box(x, y, w, h, title, body, acc, dashed) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.06, fill: { color: acc ? SOFT : RAISE }, line: { color: acc ? SALEM : LINE, width: acc ? 1 : 0.75, dashType: dashed ? "dash" : "solid" } });
  s.addText([{ text: title, options: { bold: true, color: INK, fontSize: 9.5, breakLine: true } }, { text: body, options: { color: MUTED, fontSize: 8 } }], { x: x + 0.08, y: y + 0.04, w: w - 0.16, h: h - 0.08, fontFace: F, isTextBox: true, margin: 0, valign: "top" });
}
function arrow(x1, y1, x2, y2, acc, dashed) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2), w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  s.addShape(pres.shapes.LINE, { x, y, w, h, flipH: x2 < x1, flipV: y2 < y1, line: { color: acc ? SALEM : INK, width: acc ? 1.5 : 1, endArrowType: "triangle", dashType: dashed ? "dash" : "solid" } });
}
function num(x, y, n) {
  s.addShape(pres.shapes.OVAL, { x: x - 0.11, y: y - 0.11, w: 0.22, h: 0.22, fill: { color: SALEM }, line: { color: SALEM } });
  s.addText(String(n), { x: x - 0.11, y: y - 0.11, w: 0.22, h: 0.22, fontFace: F, fontSize: 7.5, bold: true, color: WHITE, align: "center", valign: "middle", isTextBox: true, margin: 0 });
}
const ZY = 1.28, ZH = 4.55;
// zones
zone(0.4, ZY, 2.4, ZH, "THE CONSULTANT'S DESK", false);
zone(3.0, ZY, 3.2, ZH, "KARTA'S CLAUDE TEAM ACCOUNT · ANTHROPIC", true);
zone(6.4, ZY, 3.2, ZH, "KARTA'S SYSTEMS OF RECORD", false);
zone(9.8, ZY, 3.13, 2.75, "KARTA-OWNED CLOUD", true);
zone(9.8, 4.2, 3.13, 1.63, "THE CLIENT", false);
// desk
box(0.52, 1.62, 2.16, 0.78, "Browser · claude.ai", "Opens the engagement workspace page with their own Karta seat.");
box(0.52, 2.5, 2.16, 0.7, "Claude Desktop / Claude Code", "Karta skills for ad hoc work, same connectors.");
box(0.52, 3.3, 2.16, 0.55, "PowerPoint", "Opens the finished deck.");
box(0.52, 3.95, 2.16, 0.7, "Outlook and Teams", "Where a person sends the deck. The workspace never sends.");
s.addText("Nothing is installed on the laptop.", { x: 0.52, y: 5.3, w: 2.16, h: 0.3, fontFace: F, fontSize: 7.5, color: MUTED, italic: true, isTextBox: true, margin: 0 });
// claude account
box(3.12, 1.62, 2.96, 0.78, "Engagement workspace pages", "One published page per engagement, shared only with the staffed team. Live: Legend · Continuous Support.", true);
box(3.12, 2.5, 2.96, 0.62, "Claude", "Drafts the words and suggests a status, only when a consultant clicks Draft.");
box(3.12, 3.22, 2.96, 1.2, "Connectors", "Asana · Microsoft 365 · Granola · Harvest · Karta Assembly. Every call runs as the consultant who is looking, with their own access.");
box(3.12, 4.52, 2.96, 1.2, "Page database", "Approved status values with the approver's name, the engagement configuration, deck history. Visible to the staffed team. Holds only what a person approved.");
// systems of record
box(6.52, 1.62, 2.96, 1.5, "Microsoft 365 · Karta tenant", "SharePoint client folders: last deck read, new deck saved.\nEntra ID: sign-in for the deck builder, once IT approves.\nOutlook: planned evidence.  Teams: people send the deck.");
box(6.52, 3.22, 2.96, 0.6, "Asana", "Projects, tasks, milestones. Read live on every open.");
box(6.52, 3.92, 2.96, 0.6, "Granola", "Meeting notes. Folder linked; reads planned.");
box(6.52, 4.62, 2.96, 0.6, "Harvest", "Time and budget. Project linked; reads planned.");
box(6.52, 5.32, 2.96, 0.42, "RAID log · planned source", "Today risks are typed by the reviewer.", false, true);
// cloud
box(9.92, 1.62, 2.89, 0.92, "Karta Assembly · Google Cloud Run", "The deck builder. Approved values in, PowerPoint out on the KCG template. Keeps nothing. Scales to zero. $0.36 spent to date.", true);
box(9.92, 2.64, 2.89, 0.5, "Secret Manager", "The service's sign-in secret. Never in code.");
box(9.92, 3.24, 2.89, 0.7, "GitHub · Karta organization", "Code, page sources, documentation, decisions. Private. No client data.");
// client
box(9.92, 4.54, 2.89, 1.18, "Client stakeholders", "Receive the weekly status deck from a Karta person in Teams or email, as today. Nothing connects to the client's systems. Software never sends.");
// arrows and numbers
arrow(2.68, 2.0, 3.1, 2.0, false, false); num(2.9, 1.86, 1);                       // 1 open
arrow(6.08, 3.6, 6.5, 3.5, false, false); arrow(6.08, 3.5, 6.5, 2.05, false, false); // 2 asana, sharepoint
arrow(6.08, 3.9, 6.5, 4.2, false, true); arrow(6.08, 4.0, 6.5, 4.9, false, true); arrow(6.08, 4.1, 6.5, 5.5, false, true); // planned reads
num(6.3, 3.25, 2);
arrow(4.6, 2.46, 4.6, 2.5, false, false); num(4.9, 2.45, 3);                        // 3 draft
arrow(6.08, 2.2, 6.2, 2.2, true, false); arrow(6.2, 2.2, 6.2, 4.9, true, false); arrow(6.2, 4.9, 6.1, 4.9, true, false); num(6.2, 4.6, 4); // 4 record
arrow(4.6, 5.72, 4.6, 6.02, true, false); arrow(4.6, 6.02, 9.7, 6.02, true, false); arrow(9.7, 6.02, 9.7, 2.1, true, false); arrow(9.7, 2.1, 9.9, 2.1, true, false); num(7.4, 6.02, 5); // 5 values -> deck
arrow(9.9, 1.92, 9.5, 1.85, true, false); num(9.7, 1.72, 6);                        // 6 save to SharePoint
arrow(2.68, 4.3, 2.68, 6.3, false, false); arrow(2.68, 6.3, 11.36, 6.3, false, false); arrow(11.36, 6.3, 11.36, 5.74, false, false); num(7.4, 6.3, 7); // 7 person sends
arrow(9.5, 2.35, 9.9, 2.35, false, false); num(9.7, 2.5, 8);                        // 8 sign-in
arrow(11.36, 3.22, 11.36, 2.56, false, false); num(11.55, 2.9, 9);                  // 9 deploy
// legend
const L = [
  ["1", "Open the workspace in claude.ai with your own seat."],
  ["2", "The page reads Asana and SharePoint as you. Granola, Harvest, Outlook and RAID reads come later."],
  ["3", "Claude drafts the words on a click. Code sets dates and colors."],
  ["4", "You correct and approve under your name. The record is saved with time and sources."],
  ["5", "Approved values go to Karta Assembly; a finished deck comes back. It keeps nothing."],
  ["6", "The deck is saved to the Status & Steer Co folder as you (after IT approves sign-in)."],
  ["7", "A person opens it in PowerPoint and sends it, by choice. Software never sends."],
  ["8", "Entra sign-in limits the deck builder to Karta identities. One IT approval pending."],
  ["9", "GitHub deploys the deck builder and publishes the pages. Karta-owned from September 14."],
];
L.forEach((it, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = 0.4 + col * 4.2, y = 6.5 + row * 0.24;
  num(x + 0.11, y + 0.12, it[0]);
  s.addText(it[1], { x: x + 0.3, y: y, w: 3.85, h: 0.23, fontFace: F, fontSize: 7.5, color: INK, isTextBox: true, margin: 0, valign: "middle" });
});
s.addText("Green arrows carry approved values or the finished deck and exist only after a named approval. Dashed lines are planned. September 9, 2026.", { x: 0.4, y: 7.27, w: 12.5, h: 0.2, fontFace: F, fontSize: 7, color: STONE, isTextBox: true, margin: 0 });
s.addNotes("Talk track: left to right. The consultant only touches the browser, Claude, PowerPoint and Teams. Karta hosts two new things: the pages in our Claude account and a small deck builder on Google Cloud, at effectively zero cost. Every read of Asana or SharePoint runs as the person looking, so nobody sees an engagement they are not on. The only thing that leaves is a deck a named person approved, and a person sends it.");
const out = "/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-delivery-workspace/docs/slides/engagement-workspace-architecture.pptx";
fs.mkdirSync(require("path").dirname(out), { recursive: true });
pres.writeFile({ fileName: out }).then(() => console.log("wrote", out));
