# Standing up an engagement workspace

**Status:** Gate 6 working process, revised September 8, 2026 after Sean's direction: setup by links, owner named at stand-up. Sean Bradley holds every role during the pilot and delegates later.
**Target:** a new engagement live in under one day, each member productive in under one hour.

## Roles and responsibilities

| Role | Holds during pilot | Responsible for |
|---|---|---|
| Initial owner (usually the CSE) | Sean | Named by whoever stands the workspace up. Completes the setup screen, then sets reviewers and members with the team and confirms stage dates. Resolves source gaps. |
| Product owner | Sean | Publishes and shares the engagement page, sets capability readiness, owns the catalog, decides when a capability may be client-facing. |
| Foundations owner | Sean | Runs the assembly service, the connector registration, the templates, and the contracts. Owns deploys and secrets. |
| Capability owner (Weekly Status) | Sean | Owns the drafting prompt, the status rules, corrections, and the readiness tier for Weekly Status. |
| Named reviewer | Any staffed member | Approves client-facing values under their own name. Accountable for what leaves the workspace. |
| Member | Staffed consultants | Uses the workspace with their own connector authorizations. Never shares credentials. |
| Tenant admin (Microsoft) | Outside the team | One-time consent for the Karta Assembly Service app. Nothing else. |

Rule that does not bend: every read runs as the viewer. A member who is not staffed on the engagement in Asana or SharePoint sees nothing from those sources, whatever the page says.

## The stand-up checklist

Do these in order. Steps 1 to 2 and 6 are the initial owner. Steps 3 to 4 are the owner with the team, then or later. Steps 5 and 7 are the product owner. Step 8 is each member.

1. **Confirm the engagement identifier and names.** `engagement_id` in kebab case (for example `acme-fpa`), client name, project name. Nothing else about the client goes into configuration.
2. **Collect the links.** The Asana project link and the SharePoint engagement folder link (Copy link works). Granola and Harvest are picked from lists on the page. No identifiers are typed by hand; the page derives them from the links and verifies them through the owner's connectors.
3. **Write the seven stages.** Start and end dates for Project Planning, Foundations, Build, Test, Train, Deploy, and Continuous Support. Mark Train as parallel. Mark Continuous Support contracted or not. Record where the dates came from and the date you confirmed them.
4. **Write the current stage's control point and deliverables.** The next gate with its due date, a named owner, the decision it produces, and the evidence items with their state. The stage's deliverables with Approved, In progress, Draft, Missing, or Not started.
5. **Create the engagement page.** Publish a copy of the blank workspace (`page/engagement-workspace.html`) as a new artifact with the standard capability manifest (Asana, Microsoft 365, Granola, Harvest App, Karta Assembly, sample, db, downloads). Share it with the initial owner only. Never share publicly. Record the artifact URL in the handover.
6. **Hand the page to the initial owner.** The owner opens it and completes the setup screen: client and project names, their own name and email, and the links to the Asana project, the SharePoint engagement folder (Copy link or browser address; the page finds the Status and Steer Co folder inside it), and picks the Granola folder and Harvest project from lists. The page checks each through the owner's own connectors and records what it could verify. Stage dates can be entered then or later in Config. After setup the owner adds reviewers and members in Config and shares the page with them.
7. **Run the access test** (`docs/access-test-plan.md`) with one staffed member and one member who is not staffed. Record the result before anyone uses the page for client work.
8. **Onboard each member** using `docs/onboarding-runbook.md`.

## Weekly upkeep

- Engagement owner confirms stage dates and the next control point when the plan changes; the confirmation date shows on the page.
- Reviewer approves Weekly Status under their name; the deck is generated from the approved values.
- Product owner reviews correction rate and time to approval in the Config area's pilot measures once a week.

## What is deliberately not automated yet

Creating the page and seeding the configuration are manual, done by the product owner with a Claude session. An engagement setup assistant is a Horizon 2 item in the roadmap and is not needed for two engagements.
