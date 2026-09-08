# Standing up an engagement workspace

**Status:** Gate 6 working process, September 8, 2026. Sean Bradley holds every role during the pilot and delegates later.
**Target:** a new engagement live in under one day, each member productive in under one hour.

## Roles and responsibilities

| Role | Holds during pilot | Responsible for |
|---|---|---|
| Engagement owner | Sean | Approves the engagement configuration: stage dates, control points, deliverables, sources, reviewers, capabilities. Confirms dates each week the plan changes. Resolves source gaps. |
| Product owner | Sean | Publishes and shares the engagement page, sets capability readiness, owns the catalog, decides when a capability may be client-facing. |
| Foundations owner | Sean | Runs the assembly service, the connector registration, the templates, and the contracts. Owns deploys and secrets. |
| Capability owner (Weekly Status) | Sean | Owns the drafting prompt, the status rules, corrections, and the readiness tier for Weekly Status. |
| Named reviewer | Any staffed member | Approves client-facing values under their own name. Accountable for what leaves the workspace. |
| Member | Staffed consultants | Uses the workspace with their own connector authorizations. Never shares credentials. |
| Tenant admin (Microsoft) | Outside the team | One-time consent for the Karta Assembly Service app. Nothing else. |

Rule that does not bend: every read runs as the viewer. A member who is not staffed on the engagement in Asana or SharePoint sees nothing from those sources, whatever the page says.

## The stand-up checklist

Do these in order. Steps 1 to 4 are the engagement owner. Steps 5 to 7 are the product owner. Step 8 is each member.

1. **Confirm the engagement identifier and names.** `engagement_id` in kebab case (for example `acme-fpa`), client name, project name. Nothing else about the client goes into configuration.
2. **Locate the sources.** Asana workspace and project gids; the milestone section name or the `milestone` subtype; the SharePoint drive id, the Status and Steer Co folder item id and its web link; the deck filename pattern the team already uses. Use the connector search tools from a Claude session to find the ids; never guess them.
3. **Write the seven stages.** Start and end dates for Project Planning, Foundations, Build, Test, Train, Deploy, and Continuous Support. Mark Train as parallel. Mark Continuous Support contracted or not. Record where the dates came from and the date you confirmed them.
4. **Write the current stage's control point and deliverables.** The next gate with its due date, a named owner, the decision it produces, and the evidence items with their state. The stage's deliverables with Approved, In progress, Draft, Missing, or Not started.
5. **Create the engagement page.** Copy the console source, change only the configuration block's engagement identifier and source pointers, publish it as a new artifact with the capability manifest (Asana, Microsoft 365, Karta Assembly, sample, db, downloads), and share it with the staffed members only. Never share publicly. Record the artifact URL in the handover.
6. **Seed the configuration document.** Open the new page's Config area and save the configuration, or write `engagements/<engagement_id>/config` with the Artifact tool. The page reads the document on load and falls back to its built-in block only when no document exists.
7. **Run the access test** (`docs/access-test-plan.md`) with one staffed member and one member who is not staffed. Record the result before anyone uses the page for client work.
8. **Onboard each member** using `docs/onboarding-runbook.md`.

## Weekly upkeep

- Engagement owner confirms stage dates and the next control point when the plan changes; the confirmation date shows on the page.
- Reviewer approves Weekly Status under their name; the deck is generated from the approved values.
- Product owner reviews correction rate and time to approval in the Config area's pilot measures once a week.

## What is deliberately not automated yet

Creating the page and seeding the configuration are manual, done by the product owner with a Claude session. An engagement setup assistant is a Horizon 2 item in the roadmap and is not needed for two engagements.
