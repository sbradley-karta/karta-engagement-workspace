# Handover — Karta project artifact site

**Written** 3 September 2026 · **For** the next session picking up development
**Read this whole file before touching anything.** Most of it is fact that cost real tool calls to establish, and re-deriving it wastes the session.

---

## 0. What this project is

One page per engagement — a "project artifact site" — that reads live project data with the *viewer's own* credentials, drafts work with Claude, holds it at a human review gate, and accumulates the engagement's record. Strategy and vision live in the blueprint; this file is the operational state.

**Read for context, in this order:**

| File | What it is |
|---|---|
| `project-artifact-sites.md` | The blueprint. Architecture, review contract, operating model, rollout, open decisions. |
| `artifact-site/engagement-console.html` | The working POC source. This is the thing to develop. |
| `artifact-site/weekly-status-deck-skill/` | Ethan's skill, unmodified. Content rules are good; mechanics have confirmed bugs (§5). |
| `artifact-site/blueprint.html` | Source of the published blueprint artifact. |
| `artifact-site/karta-tokens.css` | Karta brand tokens, extracted. Paste into any new page. |

---

## 1. Live artifacts — do not create new ones

Both were published from this working directory. To update either, republish **the same file path**, or pass the URL as `url`. Publishing without `url` from a fresh conversation creates a *duplicate* — don't.

| Artifact | URL | Source file |
|---|---|---|
| doTERRA Delivery Console (the POC) | `https://claude.ai/code/artifact/cd830c0e-10da-466c-86b5-e4f249c16520` | `artifact-site/engagement-console.html` |
| Project Artifact Sites (blueprint) | `https://claude.ai/code/artifact/70179aca-a7bb-43f3-a6be-e3838b8883f1` | `artifact-site/blueprint.html` |

Console was published with:

```
capabilities: {
  mcp: { servers: [
    { server: "Asana",         tools: ["asana_search_tasks"] },
    { server: "Microsoft 365", tools: ["sharepoint_search"] }
  ]},
  sample: {},
  db: {}
}
favicon: 🧭   (never change it — omit favicon on redeploy)
```

**Capabilities is a full-set declaration.** On redeploy, omitting `capabilities` carries the stored set forward. Passing a non-empty object *replaces* it — anything not restated is revoked. So when adding a connector tool, restate the whole manifest.

---

## 2. Verified platform facts

Established this session by direct call or header check. Trust these; don't re-research.

### Runtime capabilities available to this account
Contract **0.2.41**. Roster: `artifact`, `db`, `downloads`, `mcp`, `room`, `sample`, `self` (deprecated alias of `artifact`).

**There is no `user` capability.** So `data/users/me` per-viewer-private `db` subtrees are *not available*. Everything in `db` is shared with everyone who can open the page. Design accordingly — do not assume per-viewer privacy.

Reach anything via `await claude.use(name)`; it resolves `null` when unavailable and **never during the script's first synchronous run**. Render the page without it and light features up on resolve. Framed by a host that never answers, it resolves `null` after 10s.

### Connector display names — exact strings
`mcp` addresses connectors by **display name**, never by id:

`Asana` · `Microsoft 365` · `Granola` · `Harvest App` · `visualize`

Only claude.ai connectors are valid. The Claude app's own servers (`cowork`, `workspace`, `scheduled-tasks`) are **not** addressable from a page.

### Karta Asana identifiers
- Workspace: `1207382895863198` (kartacg.com)
- doTERRA Raw Materials & Production Planning: **`1215722811960554`**
- doTERRA `Project Milestones` section: `1215723128499322`
- Firm template "Asana Project Template (WIP)": `1216318202838093`

doTERRA sections: Project Milestones · Data & Integrations · Sourcing · Raw Materials Planning · Production Planning · Promotional Planning · Purchasing Budget · Active Build · Admin

Firm template sections: Project Management · Foundations · Data Hub · Spoke Model · User Acceptance Testing Preparations · Go-Live Preparations

### SharePoint
Status decks live at:
`.../Firmwide - General & Delivery/Delivery/_Client Projects/doTERRA/03_Raw Materials Planning/00 - Project Management/Status & Steer Co/`

Most recent at time of writing: `KCG_Status DoTERRA 8-26-2026.pptx`. 89 results total for the query `KCG_Status doTERRA`.

### Teams
**Claude cannot act in Teams.** The Microsoft 365 connector is read-only for Teams — `teams_list_teams`, `teams_list_channels`, `teams_list_chats`, `teams_list_channel_messages` exist; there is no send/post tool. July 2026 write tools covered Outlook mail, calendar and OneDrive/SharePoint only. No @mention, no event triggers.

**Artifacts cannot be embedded in Teams.** Verified by header check:
```
GET https://claude.ai/code/artifact/<id>
content-security-policy: frame-ancestors 'self'
```
Page content runs in a nested frame on `<uuid>.frame.claudeusercontent.com`; pointing a tab at that inner frame strips the capability bridge and every `claude.use()` returns null. A Teams tab must link out.

---

## 3. Observed connector shapes

**Rule: never publish a page calling a connector tool without having observed one real request/response pair.** These were observed. Anything new must be observed first.

Also: **never embed observed values in the page as sample data.** The console fetches everything live; config pointers (project gid, client name) are fine, real task names are not.

### `Asana` → `asana_search_tasks`

Request used:
```json
{ "projects_any": "1215722811960554", "limit": 60,
  "sort_by": "due_date", "sort_ascending": true,
  "opt_fields": "name,start_on,due_on,completed,completed_at,assignee.name,memberships.section.name" }
```

Response:
```json
{ "data": [ {
  "gid": "…", "name": "…",
  "completed": false, "completed_at": null,
  "due_on": "2026-08-14", "start_on": null,
  "assignee": { "gid": "…", "name": "…" } | null,
  "memberships": [ { "section": { "gid": "…", "name": "Project Milestones" } } ]
} ] }
```

**`sections_any` does not reliably filter** — it returned tasks from other sections. Filter client-side on `memberships[].section.name`. The console already does this.

### `Microsoft 365` → `sharepoint_search`

Request used: `{ "query": "KCG_Status doTERRA", "limit": 5 }`

Response is **concatenated JSON objects, not an array**, each:
```json
{ "uri":"file:///…", "driveId":"…", "id":"…", "name":"KCG_Status DoTERRA 8-26-2026.pptx",
  "content":"…", "summary":"…", "isPartialContent":true,
  "webUrl":"https://kartaconsultinggroup.sharepoint.com/…",
  "downloadUrl":null, "size":null,
  "lastModifiedDateTime":"2026-09-03T14:42:33.000Z", "offset":0 }
```
followed by a final `{ "moreResults":true, "nextOffset":5, "totalResultCount":89 }`.

> ### ⚠ THE FIRST THING TO VERIFY
> The shapes above are what the **tool** returns to a session. What a **page** receives via
> `mcp.callTool(...)` / `watchTool(...)` is `result.payload` — documented as "`structuredContent`
> when present, else the first text block's text parsed as JSON when it parses, else that text
> verbatim." **I could not confirm how the concatenated-object SharePoint response lands in
> `payload`.** The console parses defensively (`Array.isArray(p) ? p : p.value || p.results || []`)
> but that is a guess and may return nothing. Open the console in the viewer, check whether the
> "last deck" chip populates, and fix the parse against what actually arrives. Asana's clean
> `{data:[…]}` is far more likely to work first try.

---

## 4. POC state — `artifact-site/engagement-console.html`

Vanilla HTML/CSS/JS, no build step, no dependencies. ~28KB. Publishes as-is.

### Layout — engagement landing page

Follows Sean's reference mockups (two screenshots, light and dark, provided in-session). Structure:

- **Top bar** — light in light mode, charcoal in dark. KARTA CONSULTING GROUP | ENGAGEMENT DELIVERY
  on the left; Project chat, Help, **theme toggle**, avatar on the right.
- **Engagement header** — "doTERRA" at 35px Manrope 800, subtitle, then meta chips (period,
  sources-synced state, Pilot pill).
- **Hero** — "Here's where the project stands." with a live one-line summary naming the current
  phase and the count of items past due.
- **Ask this project** — full-width card, wired to `sample` over the live task data with an
  instruction to say so plainly rather than guess.
- **Project journey** — 5-step stepper: solid green connectors and check bubbles for complete,
  filled numbered bubble for the current phase, dashed connectors and outline bubbles ahead.
- **Recommended now** — 4 capability cards. Only "Create weekly status" is live (Start → review
  gate); the rest carry Available / Coming soon / Planned tags.
- **Project insights** — right rail: needs attention (with a red dot when non-zero), upcoming
  milestone, team assigned, next client update. All derived from live Asana.
- **Recent project activity** — the latest SharePoint status deck plus the four most recent Asana
  completions.
- **Review gate** — second view, reached from Start, returned from by the back link.

**Theme toggle.** Three-state by design: with no manual choice the page follows the viewer
(`data-theme` stamp, else `prefers-color-scheme`). Clicking the toggle sets `data-mode="light"` or
`"dark"` on the root, declared last so it wins, and persists to `localStorage["kcg-mode"]` inside
try/catch. Dark mode is **charcoal** (`--ground #111213`, `--surface #191B1C`) with a lifted Salem
accent — deliberately not green-on-green, per Sean.

**Type and palette are the Karta design system** — Manrope only, no serif; San Felix, Salem and
Stone Wall. The first pass at this used a serif display face read off the mockup screenshots and
Sean corrected it: *stick with our design system but use the visual layout and concepts.* Layout
comes from the mockups; every colour and typeface comes from the design system.

### Phase dates are the one thing not read live

`CFG.phases` at the top of the script holds the five phases with start and end dates, seeded from
the mockup. Everything else on the page is read live or derived in code. Those dates need
confirming against doTERRA's actual plan — the current-phase highlight and the hero line both key
off them. Edit them in that one place.

### Known soft spots
- The `sample` drafting prompt (in `draftPrompt()`) is a first draft. Correction rate will tell us how good it is.
- `db` write failure is surfaced but the page keeps local state — acceptable, worth revisiting.
- Engagement config is a hardcoded `CFG` object. Generalizing this is step 4 below.
- No `room` presence, so two people reviewing simultaneously can clobber each other's finalize. Low risk at current scale.

---

## 5. The skill's bugs — confirmed by running the code

`artifact-site/weekly-status-deck-skill/scripts/pptx_helpers.py`. I installed python-pptx 1.0.2 in a throwaway venv and executed these. **The content rules in SKILL.md are sound and worth preserving; the mechanics are not.**

**Crash 1 — `add_position_marker`, first line of the body.**
`connector.line.color.rgb.__class__` — a deliberate no-op "to document the import path". Reading `.rgb` before a color is set raises `AttributeError: no .rgb property on color type '_NoneColor'`. **Fix: delete the line.** Verified.

**Crash 2 — `copy_slide_from_external`, any slide with a picture.**
Passes `image_part.blob` (raw bytes) to `get_or_add_image_part()`, which expects a path or file-like → `AttributeError: 'bytes' object has no attribute 'seek'`. **Fix: `io.BytesIO(sh.image.blob)`.** Verified — the copy then produces a valid slide whose picture blob resolves after a fresh reopen. This bug hits the *primary* path: slides 2 and 3 carry the client logo.

**Wrong constants — the "Yellow" is a teal.**
COM ints are OLE colors (`&HBBGGRR`, low byte = red):

| | COM int | Correct RGB | Skill's tuple |
|---|---|---|---|
| Green | `6786602` = `0x678E2A` | `(0x2A, 0x8E, 0x67)` | `(0x67, 0x99, 0x22)` ✗ |
| Yellow | `2204889` = `0x21A4D9` | `(0xD9, 0xA4, 0x21)` gold | `(0x21, 0xA1, 0x99)` ✗ teal |
| Red | `4871627` = `0x4A55CB` | `(0xCB, 0x55, 0x4A)` | — |

Byte-reversed *and* mistranscribed. One wrong value propagates to the slide-3 marker plus four status ovals. **Eyedropper the real template before trusting either column.**

**Also broken / missing:**
- `try_export_slide_png` — LibreOffice `--convert-to png` renders only slide 1 and names output from the input basename, so `slide_1indexed` is ignored and the `os.path.exists(out_path)` check fails even on success. Moot here anyway: **no LibreOffice on this Mac**, so it always returns `False` and no visual QA is possible.
- `find_table_by_name` is used in SKILL.md's example but never written.
- No slide-reordering helper — `copy_slide_from_external` appends at the end, but the deck needs slides 1–4 in order.
- Copying onto layout index 6 ("Blank" in the stock template, unverified for `KCG_Status Template.pptx`) loses source-layout-inherited formatting.
- `rewrite_bulleted_cell` raises `IndexError` on an empty `items` list — reachable, since the skill says risks are often empty.
- Dead code: `_shape_contains_text`, and `template_pPr` computed but never used.

**Environment:** `python3` 3.9.6 at `/usr/bin/python3`. **python-pptx is not installed** system-wide. No LibreOffice, no `pdftoppm`.

---

## 6. Data-convention mismatches (found in live Karta data)

The skill assumes conventions Karta doesn't actually follow. These break it silently.

| Skill assumes | Reality |
|---|---|
| Sections `Kickoff / Foundations / Build / UAT / Deploy` | doTERRA uses `Project Milestones` + workstream sections; firm template uses a third set. Neither matches. |
| Milestone date from `start_on` | Milestones have `due_on` populated, `start_on` null. Reading `start_on` yields nothing. |
| `<YYYYMMDD> KCG_<Client> Status Report.pptx` | Actual: `KCG_Status DoTERRA 8-26-2026.pptx`. Previous-deck lookup fails. |
| `sections_any` filters the task search | It doesn't. Filter on `memberships[].section.name`. |

Still correct and worth keeping: **New Date governs, never Orig. Date**; drop the `Build:` prefix from milestone names; ~14 wrapped lines at ~48 chars; empty-risks phrasing is "No open risks or issues outstanding."

---

## 7. Design system — Karta, not my choices

**Source of truth:** the Karta Consulting Group Design System —
`https://claude.ai/design/p/e094fba9-877c-4944-8768-6c6463c0690e`
Both pages were rebuilt onto it. Tokens are extracted to `artifact-site/karta-tokens.css`;
paste that block into any new page. **Read the design system itself before making brand
judgement calls** — it carries logo lockups, exclusion zones, voice guidance and UI kits this
file only summarises.

### Brand palette

| Name | Hex | Role |
|---|---|---|
| San Felix | `#113A2A` | Primary / body text. Near-black forest green. |
| Salem | `#2A654E` | Accent — links, CTAs, highlights. |
| Stone Wall | `#979187` | Neutral — borders, labels, muted surfaces. |
| White | `#FFFFFF` | Dominant background. |

### Type

Brand specifies **Visby CF** (commercial, not redistributable). The design system substitutes
**Manrope** from Google Fonts and flags it — if a licensed Visby CF webfont ever arrives, swap it.
One family throughout, contrast carried by **weight, not by pairing**: 800 for display/headlines
with tight tracking, 600 for labels and panel heads, 400–500 for body. No serif. Load
`Manrope:wght@400;500;600;800`.

There is no brand mono. A system mono stack is used **only** for genuinely tabular or technical
strings — dates, gids, filenames, code. Everything label-shaped (eyebrows, table headers, badges,
step numbers) is Manrope 600 uppercase with tracking, per the brand's "ALL CAPS for nav labels and
section numbers" rule.

### Hard brand rules

- **No gradients.** The brand book prohibits them outright.
- **No colored accent borders on cards.** Both pages originally had accent left-rails; they were
  removed and replaced with tinted surfaces. Do not reintroduce them.
- Borders: 1px, Stone Wall at low opacity. Structural, never decorative.
- Shadows: soft, shallow, tinted with the primary green rather than pure black. Used sparingly.
  A card gets a border **or** a shadow, not both heavily.
- Radii 4–14px (`--r-control: 6px`, `--r-card: 12px`). The logo mark is hard-edged geometry —
  don't over-round brand-adjacent shapes.
- Hover **darkens** (Salem → San Felix); it never lightens. Press = slightly darker fill,
  no shrink or scale.
- Motion: fades and short slides, standard easing, ~200ms. No bounce or spring.
- Transparency/blur: only as a translucent dark-green scrim over photography. No glassmorphism.
- Layout: centered column, max ~1200px, generous section padding.
- **Numbered section markers** (`1.0`, `2.0`…) are a brand-book motif the design system explicitly
  recommends for internal documents and decks. The blueprint uses them via a CSS counter.
- Icons: Heroicons outline, 1.5px stroke, via CDN — a flagged substitution, since Karta's real icon
  set wasn't in the provided assets. **No emoji, no unicode characters as icons**, anywhere.

### Voice

Confident, plain, outcome-first. "We" for Karta, "your/you" for the client. Sentence case
everywhere except nav labels and section numbers. No emoji, no exclamation points, no hype
adjectives. CTAs are calm and directive — verb plus short object ("Draft this week's status"),
never urgency language.

### Deliberate extensions — flagged, and worth a review

Three additions were made that the brand system does not itself define. Check them against the
design system owner:

1. **Stone Wall darkened to `#6E6961` for secondary *text* only.** `#979187` on white is roughly
   3.1:1 and fails small-text contrast. Stone Wall proper is retained for borders, labels and muted
   surfaces.
2. **Semantic warn `#9A6B1F` and risk `#A63D30` added.** A status console needs amber and red; the
   brand defines neither. Both are muted to sit beside the greens rather than fight them. Status
   "Green" reuses Salem, which is on-brand.
3. **A dark theme was derived from San Felix.** The brand system is light-only, but artifacts render
   in the viewer's theme and a transparent page borrows the host's ground. Ground `#0A1D15`, surface
   San Felix, accent lifted to `#6FB08D` for contrast. This keeps the brand identity in dark mode
   rather than inventing a second palette.

Three-state theming is still required: full palette on bare `:root`; `@media (prefers-color-scheme:
dark)` guarded as `:root:not([data-theme="light"])`; then `:root[data-theme="dark"]` again. `body`
must set an explicit `background` token.

**CDN allowlist (CSP-enforced):** scripts only from cdnjs / jsdelivr / `cdn.tailwindcss.com` /
code.jquery.com; stylesheets only from fonts.googleapis.com. Everything else is silently blocked.
The console needs no library — keep it that way if you can.

## 8. Non-negotiable design rules

Carry these into every capability. They came out of real reasoning, not preference.

1. **The review gate is never skippable.** No capability writes to a client deliverable without a human correcting the draft first. No auto-send, ever.
2. **Draft once, persist, everyone else reads.** A page that redrafts on load multiplies cost across viewers *and* shows each of them different numbers than the reviewer approved. The inconsistency is the real bug.
3. **Model calls fire on an explicit click**, never on load. First `sample` call prompts the viewer for consent; handle `not_granted` (hide the affordance) and `rate_limited` (back off, never loop).
4. **Derive in code what can be derived.** Status inference, date arithmetic, rollups, budgets, file assembly. Send the model only genuine judgment.
5. **Read as the viewer.** Never introduce a service account or shared credential — the whole security posture rests on connector calls using the viewer's own identity.
6. **Never embed observed data as placeholder content.** Fetch live.

---

## 9. Development plan

### Step 1 — Verify the POC live *(blocks everything else)*
Open the console in the viewer and walk it: does the Asana chip populate? Does the deck chip populate (see §3 warning)? Does Draft prompt for consent and return usable JSON? Does Finalize persist, and does a second open read it back without calling anything? Fix what breaks. **Do not build anything new until this passes.**

### Step 2 — Judge the draft quality
Run it against a real week. The metric is **correction rate** — how much of the draft a human has to fix. Tune `draftPrompt()` against that, not against taste. This decides whether the status deck moves Piloted → Standard.

### Step 3 — Add the missing reads
RAID log, Granola transcripts (`Granola` connector), the Design Document. Observe each tool's real shape before wiring it. Each meaningfully improves accomplishments and risks.

### Step 4 — Generalize beyond doTERRA
Move `CFG` into a `db` doc so the page is engagement-driven, or settle on cloning a template page per engagement. **Leaning per-engagement pages** for client isolation — one page switching clients puts every engagement's config in one shared store, and there is no `user` capability to partition it.

### Step 5 — Close the assembly loop
Either the hand-off block is good enough in practice, or fix `pptx_helpers.py` (§5) and drive the skill from a session. Only after that has proved annoying enough to price should the Karta MCP server be considered — and then as a **pure function**: reviewed values in, `.pptx` out, no data access, no per-user OAuth, template bundled and validated at startup. Days of work in that shape; a different project in any other.

### Step 6 — Second capability
BRD generator. Inputs are Granola transcripts (reachable today), output feeds the existing UAT scripts skill. First real chain and the best proof the architecture holds.

---

## 10. Open questions for Sean

- **Who owns Foundations?** Unresolved and blocking at the architecture level.
- **Fix the skill upstream?** It's Ethan Sweeney's, and its own header asks that corrections go back into the file rather than being patched around. The three bugs and the color constants should go to him, not into a Mac-only fork.
- **Standardize Asana sections and folder naming, or make them per-engagement config?** Recommendation is both — standard by default, config as the escape hatch.
- **Plan and seats:** everyone who *uses* a site needs a Claude seat with usage headroom, not just builders. Team seats are $25/member/month; project sharing needs Team or Enterprise.
- **Who should the console be shared with?** It's private to Sean right now. Sharing is per-artifact from the page's share menu. Note that declaring `mcp` bars public sharing — which is correct for client confidentiality.
- **Which second engagement pilots this?** doTERRA plus one more, for three or four weeks, before anything reaches a catalog.

---

## 11. Session-start checklist

```
1. Read project-artifact-sites.md and this file.
2. Read artifact-site/engagement-console.html end to end before editing it.
3. Do NOT publish a new artifact — republish artifact-site/engagement-console.html,
   or pass url=https://claude.ai/code/artifact/cd830c0e-10da-466c-86b5-e4f249c16520
4. Load the artifact-capabilities skill before touching any claude.use() code.
5. Load artifact-design before writing any new page, and use `artifact-site/karta-tokens.css`
   — the Karta design system (§7) overrides any palette you would otherwise choose.
6. Observe any new connector tool's real request/response before wiring it into a page.
7. Start at §9 Step 1. Verify before building.
```
