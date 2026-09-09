# Project Artifact Sites

**Karta Consulting Group · Internal AI capability**

One page per engagement that reads live project data with the viewer's own credentials, drafts the work, holds it at a human review gate, and accumulates what the project knows. The door a project team walks through — not a tool they have to learn.

`draft blueprint` · `first POC live on doTERRA RMPP` · `owner: unassigned`

---

## The idea

Every engagement gets its own page. It knows which client it belongs to, reads that project's live state from Asana, SharePoint, Outlook and Granola, and presents the firm's AI capability as a small set of things you can actually click. A PM never types a prompt, never names a skill, and never explains which project they're on.

Two properties do the heavy lifting. First, **the page carries context** — arriving from the engagement's own site means the client, the config and the source systems are already resolved, which is the tax that makes generic AI tooling go unused. Second, **it reads as the viewer** — every connector call uses that person's own credentials, so a consultant can only ever reach engagements they're actually staffed on. There is no service account and no cross-client blast radius.

> **Live proof of concept**
> [doTERRA Delivery Console](https://claude.ai/code/artifact/cd830c0e-10da-466c-86b5-e4f249c16520) — live Asana milestones, a drafted weekly status narrative, an editable review surface, and a hand-off block for deck assembly. Built against the real engagement, not a mock.

---

## One stop shop

Generating deliverables is the visible part and the smallest part. The full site is where a project team goes for anything the engagement knows.

The organising idea is that **the site accumulates the engagement's record**. Every capability both reads from it and writes back to it — a workshop becomes requirements, requirements become test scripts, decisions become the answer to "why did we build it this way?" three months later. Deliverables are outputs; the record is the asset. That is what makes a site a destination rather than a launcher: you go there because it is where the project's memory lives.

Today an engagement's memory is scattered across 89 status decks, a year of meeting transcripts, Teams threads, and whatever four people happen to remember. Nothing about that is searchable, and all of it walks out the door when someone rolls off.

### The components

**Produce** — deliverables, drafted and gated

| Component | Source |
|---|---|
| Weekly status deck | Asana · RAID |
| Business requirements | Granola · workshops |
| UAT scripts | BRD requirements |
| Mockups & wireframes | requirements |
| Estimates & change orders | scope · rate card |
| Runbooks & training | build state |

**Know** — the engagement's memory, made answerable

| Component | What it does |
|---|---|
| Ask the engagement | one question, every source |
| Decision log | what, when, by whom |
| Onboarding brief | an analyst's first hour |
| Meeting close-out | transcript → actions |

**Watch** — signals surfaced without being asked

| Component | Trigger |
|---|---|
| Slipping milestones | Asana dates |
| Stalled workstreams | no movement, N weeks |
| Aging RAID items | open, untouched |
| Scope drift | built vs. BRD |

**Run** — the commercial and delivery picture

| Component | Source |
|---|---|
| Burn against plan | Harvest · SOW |
| Resourcing & capacity | allocations |
| Margin health | hours vs. fee |
| Portfolio roll-up | leadership view |

None of these need a data source we don't already have connected. Asana, SharePoint, Outlook, Granola and Harvest cover every item above — what's missing is the surface that puts them in one place and the record that ties them together.

### How a site matures

Each stage is a real increase in value and a real increase in what has to exist first. They arrive in this order whether we plan for it or not.

| Stage | | What it means |
|---|---|---|
| One | **Produces** | Generates deliverables on request. Where the doTERRA console is now. |
| Two | **Remembers** | Holds the engagement record and answers questions about the project. |
| Three | **Watches** | Surfaces what needs attention before someone thinks to look. |
| Four | **Connects** | Capabilities chain, and patterns carry across engagements. |

Stage two is the one that changes the economics. A site that only produces is competing with the hour it saves; a site that remembers is competing with the week a new analyst spends getting up to speed, and with the decisions we re-litigate because nobody can find the first one.

### What constrains the vision

- **The record is earned, not designed.** Let two or three capabilities run first and extract the shared structure from what they actually have in common. A schema guessed up front is how platforms die.
- **Cross-engagement reuse carries patterns, never client data.** "How do we usually model raw materials planning" is firm IP worth compounding. Any mechanism that could surface one client's figures inside another client's engagement fails, regardless of how useful it is.
- **Watching surfaces, it never acts.** A signal raises something for a human; it does not send the email, update the client, or change the plan. The gate applies to proactive work exactly as it applies to requested work.
- **Client-facing access is a trust decision, not a technical one.** A read-only client view of a project site is entirely buildable and should not be built until someone senior decides it should exist.

---

## Architecture

Three layers, funded very unevenly. The bottom one is the asset; the top one is disposable.

### Foundations — build once

House standards as code — brand templates, Karta voice, document conventions, rate card, methodology. Shared Office-file plumbing. Template validation. The review-gate skeleton every capability inherits.

**This is where the leverage is.** Five Karta capabilities already exist and were likely each built standalone, which means each carries its own copy of the same plumbing and its own copy of the same bugs.

### Capabilities — thin, one per deliverable

Content rules plus a review surface, sitting on Foundations. A capability should be mostly judgment rules a delivery lead can read and approve, not mechanics.

### Surfaces — swappable

The artifact site per engagement. A Teams tab for discovery. Scheduled runs for anything recurring. These will change; treat them as cheap and never let a surface constraint reshape the layers below it.

---

## What a site can do

Grounded in the runtime capabilities actually available to us today, not a wish list.

| Ability | Mechanism | What it means in practice |
|---|---|---|
| Read live project data | `mcp` | Asana, SharePoint, Outlook, Granola, Harvest — called with the viewer's credentials, tokens never exposed to the page. |
| Draft content | `sample` | The page asks Claude directly, with streaming and structured JSON back. Drafting happens inside the GUI, not in a chat. |
| Remember decisions | `db` | Shared state across everyone who opens the page — finalized status, run history, engagement config. |
| Update itself | `artifact` | The page can publish new versions of itself, so the site evolves without a redeploy cycle. |
| Hand over a file | `downloads` | Offer a generated file to the viewer, who confirms the save. |
| Live co-review | `room` | Presence and ephemeral events when two people review the same draft together. |
| Assemble branded Office files | *not in the page* | A page cannot build a `.pptx` from the KCG template. That runs in a Claude session today, or behind a Karta MCP server later. |

> **Constraint worth knowing up front**
> These sites cannot be embedded inside Teams — the viewer serves `frame-ancestors 'self'`, so a Teams tab must open out to the browser. That costs one click and buys a purpose-built interface instead of a chat box. It is the right trade, but plan for the click rather than discovering it.

---

## The review contract

Every capability follows the same five steps. Learn it once, and every tool in the firm works the same way.

| Step | | What happens |
|---|---|---|
| Pull | Systems of record | Asana, SharePoint, RAID, transcripts — as the viewer. |
| Draft | Claude proposes | Fields, prose, ratings. Never written straight to a deliverable. |
| **Gate** | **A human corrects** | Editable surface with provenance. Non-skippable, always. |
| Emit | Branded artifact | Deterministic assembly from the reviewed values. |
| Send | A person decides | Distribution is never automatic. |

The gate is the entire defence against a hallucinated milestone or a fabricated requirement reaching a steering committee. There is no fully automatic mode, on any capability, ever — and one such incident would cost more trust than the whole programme buys.

One honest exception on shape: wireframes and mockups don't fit a confirm button. Their gate is a canvas you tweak rather than a draft you approve. Same contract, different surface.

---

## Deterministic vs judgment

The single most useful design rule we found. Send the model only what actually requires judgment.

**Derived in code** — milestone status from completion and dates. Status-period arithmetic. The worst-of rollup for Overall. Wrapped-line budgets. File assembly from reviewed values. All testable, all repeatable, all free.

**Drafted by Claude** — which completions are genuine milestones rather than routine chatter. How to phrase an accomplishment for a client audience. Whether the evidence reads Green or Yellow. Real judgment, and exactly what the human reviews.

Pushing assembly out of the model means the file a client opens is produced by plain, tested code. Nondeterminism sits upstream of a human check, never downstream of it.

---

## Who pays

There is no backend accruing a bill. Model calls run on the seat of whoever is looking at the page.

| Action | Charged to | Cost |
|---|---|---|
| Publishing and hosting the site | Publisher, once | Nothing ongoing |
| Reading Asana / SharePoint | Viewer's connectors | Data access, no model spend |
| Drafting content | Viewer's Claude seat | Their usage allowance |
| Editing, cycling, deleting | Nobody | Free — runs in the page |
| Reading a stored draft | Nobody | Free |
| Assembling the deliverable | Karta, if we build the server | No model cost |

> **The rule this produces**
> Draft once, on an explicit click, and persist the result. Everyone who opens the page afterwards reads what was stored. A page that redrafts on load multiplies cost across every viewer *and* shows each of them different numbers than the PM signed off on — the inconsistency is the real bug, not the spend.

---

## Operating model

How a site comes into existence, who owns it, and what governs it.

### At kickoff

Standing up an engagement's site should be one step, not a wiki page with eleven. A setup capability finds the Asana project, locates the SharePoint folder, writes the engagement config, validates the template, publishes the site, and does one dry run so the team sees the review surface before it matters.

### Weekly rhythm

Recurring work arrives on a schedule — the status draft is ready before the Thursday review. Ad hoc work starts from the site whenever someone needs it. Same capabilities, same gate, different trigger.

### Ownership

Foundations needs a named owner; a shared foundation with no owner degrades faster than independent tools do. Each capability needs an owner who takes field bugs back into the capability rather than patching around them locally.

### Readiness, shown at the point of use

| Tier | Means | Client-facing output |
|---|---|---|
| Experimental | Built, not yet run on a real engagement | No |
| Piloted | Working on one or two engagements, correction rate still high | Only with a named reviewer |
| Standard | Proven across engagements, correction rate low and stable | Yes, through the normal gate |

### Two risk classes

**Client-facing** — status decks, BRDs, UAT scripts, proposals. Full gate, named owner, readiness tier enforced.

**Internal thinking** — a quick wireframe to argue about in a workshop, a scratch estimate. Near-zero ceremony. Applying steering-committee governance here kills the everyday value.

### Conventions we depend on but don't control

Capabilities read engagement folders and Asana projects by convention, and that convention is effectively their interface. Standardise it at kickoff as the default, and allow a per-engagement config override as the escape hatch for projects that can't conform. What the doTERRA build surfaced:

- Asana section names vary by engagement — `Project Milestones` on doTERRA, a different set on the firm template, and neither matches what the original status skill assumed.
- Milestones carry `due_on` with `start_on` empty, so anything reading start dates returns nothing.
- Deck filenames run `KCG_Status DoTERRA 8-26-2026.pptx`, not the dated pattern the skill searches for.
- Where a slipped-milestone table carries both, the New Date governs — never Orig. Date.

---

## Capability catalog

The Produce column, tracked. What exists, what's in flight, and what the sites should carry next. Know, Watch and Run capabilities enter this table as they're built.

| Capability | Readiness | Note |
|---|---|---|
| Estimator / pricing workbook | Standard | Shipped. Candidate to fold onto Foundations. |
| Industry one-pager | Standard | Shipped. |
| Win story | Standard | Shipped. |
| RFP clarifying questions | Standard | Shipped. |
| UAT scripts | Standard | Shipped. Natural downstream of the BRD. |
| Weekly status deck | Piloted | Console live on doTERRA. Assembly bugs found and fixable; hand-off still manual. |
| Mockups / wireframes | Piloted | Already exists as an artifact. Canvas-style gate rather than a confirm button. |
| BRD generator | Experimental | Not built. Should be next — input is Granola transcripts, output feeds UAT scripts. First real chain. |

The compounding value is that these chain: discovery feeds the BRD, the BRD's requirements become the UAT scripts' traceability source, the estimator's phases become the status deck's milestones. Design for that composition — but extract a shared engagement record only once two or three capabilities show what they actually have in common. Guessing the schema first is how platforms die.

---

## What we measure

Capability count rewards sprawl. These three don't.

| Metric | Why it earns its place |
|---|---|
| Adoption per engagement | Whether project teams actually use it, not whether individuals tried it once. |
| **Review-gate correction rate** | How much of each draft a human has to fix. The honest quality signal, nearly free to collect if the review surface captures edits, and the number that decides when something moves from Piloted to Standard. |
| Time from source data to reviewed artifact | The hours actually saved, which is the case this programme has to make. |

---

## Rollout

Sequenced so each step produces the requirements for the next, rather than guessing them.

1. **Harden the status deck end to end.** Two engagements, three or four weeks. Fix the assembly bugs, resolve the data-convention mismatches, run the console weekly. It is the most complete capability, so it will surface real Foundations requirements rather than imagined ones.
2. **Extract Foundations.** Pull shared Office plumbing, template validation and the review-gate skeleton out of the status deck and the five shipped capabilities. Consolidation, not greenfield.
3. **Publish the catalog into Teams.** A SharePoint page per engagement site, surfaced as a Teams tab, listing capabilities with readiness tiers. No custom code, no app upload.
4. **Build the BRD generator.** Second, not first. Its inputs are reachable today and its output feeds UAT scripts — the first real chain, and the best proof the architecture holds.
5. **Decide on the Karta MCP server.** Only once the manual hand-off has proved annoying enough to price. A pure-function assembly server is days of work; one with its own data access and per-user OAuth is a different project entirely.

---

## Open decisions

Things this blueprint deliberately does not settle, because they aren't ours to settle alone.

| Decision | What turns on it |
|---|---|
| Who owns Foundations | Everything. An unowned shared layer degrades faster than independent tools. |
| Standardise Asana and folder conventions, or make them config | Two-week rollout versus two-quarter. Recommendation is both — standard by default, config as the escape hatch. |
| One site per engagement, or one site switching clients | Client isolation versus maintenance. Leaning per-engagement from a shared template. |
| Plan and seat coverage | Everyone using a site needs a seat with usage headroom, not just the builders. |
| Whether one click out of Teams is acceptable friction | If it's a hard no, a Copilot Studio agent published into Teams becomes worth a narrow pilot despite the duplication it implies. |

---

*Blueprint drafted 3 September 2026 from the doTERRA proof of concept and the research behind it. Findings about Asana structure, milestone dates and deck naming come from the live Karta workspace; the runtime capabilities described are the ones available to this account today. Readiness tiers for shipped capabilities are provisional and need confirming with their owners.*
