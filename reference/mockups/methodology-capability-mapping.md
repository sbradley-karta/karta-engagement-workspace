# Project Artifact Site: Methodology and Capability Mapping

Updated: 2026-09-04

## Design direction

Use Karta's implementation methodology as the primary navigation and orientation model for the engagement landing page:

1. Project Planning
2. Foundations
3. Build
4. Test
5. Train & Deploy

The landing page should show where the project is in this lifecycle, what is coming next, what needs attention, and which AI-supported actions are most relevant now. It should not reproduce the full methodology slide or become a dense project plan.

Weekly status remains a persistent cross-phase capability because it supports the engagement throughout delivery.

General Project Chat is also a persistent cross-phase capability. It should be available from every page and answer questions using the engagement's authorized sources and retained project record.

## Candidate AI-supported capabilities by phase

| Phase | Deliverable or activity | Potential AI support |
|---|---|---|
| Project Planning | First two weeks meetings | Agenda preparation, meeting synthesis, action and decision capture |
| Project Planning | Data first drafts | Source intake, profiling summaries, first-draft mappings |
| Project Planning | Project logistics and documentation | Kickoff packs, workplan summaries, role and dependency checks |
| Foundations | Business requirements | Workshop evidence to traceable requirements and review workflow |
| Foundations | Design document | Requirements to first-draft solution design with source traceability |
| Foundations | Process benchmark | Current-state synthesis and comparison prompts |
| Foundations | Business process flows | Requirements and workshop notes to editable process-flow drafts |
| Foundations | Mockups and wireframes | Requirements or working ideas to editable visual concepts for human review |
| Foundations | List and data matrix | Structured extraction, completeness checks, and validation |
| Foundations | Solution architecture | Draft architecture narrative, decisions, assumptions, and open questions |
| Build | Project build plan | Requirements and design outputs to sequenced build activities |
| Build | Data Hub | Mapping validation, exception summaries, and documentation |
| Build | Configured dashboards | Requirements coverage checks and review preparation |
| Build | Build documentation | Model documentation, runbooks, and configuration summaries |
| Test | Test plan | Scope and requirements to test strategy and coverage plan |
| Test | UAT test scripts | Approved requirements to traceable, review-gated test cases |
| Test | Test and enhancement log | Defect classification, duplicate detection, prioritization support |
| Test | User sign-off | Readiness summary, evidence package, and approval record |
| Train & Deploy | Model Builder training | Training plans, exercises, facilitator notes, and reference material |
| Train & Deploy | Administrative workflow | Role-based operating procedures and runbooks |
| Train & Deploy | End-user training | Audience-specific guides, decks, scripts, and knowledge checks |
| Train & Deploy | Cutover and deployed solution | Cutover checklists, readiness summaries, and release communication drafts |
| Train & Deploy | Anaplan roadmap | Enhancement themes, sequencing options, and executive roadmap narrative |

## Landing-page implications

- Replace the generic phase names with the five Karta methodology phases.
- Expand the current phase and keep completed and future phases visually compact.
- Populate **Recommended now** from the current phase, readiness tier, open work, and user role.
- Keep **Project Chat** persistently available in the global navigation and expose an approachable **Ask this project** entry point on the landing page.
- Surface the **Mockup Generator** during Foundations and Build, while retaining it in the complete capability catalog.
- Add a **Project insights** panel for upcoming milestones, deliverables due, PTO and capacity, unresolved decisions, risks, and readiness signals.
- Provide a secondary **View all capabilities** path for discovery without making the landing page a catalog.
- Show capability readiness consistently: Available, Pilot, Planned, or Coming soon.
- Keep deliverables connected so outputs can flow forward, for example workshops to requirements to design to UAT scripts to training.

## Product principle

Organize the experience around the work the team is doing, not around AI tools. The user should see the project phase, the next delivery obligation, and the most relevant action. AI should appear as embedded assistance inside that workflow.

The current visual reference uses illustrative phase ranges: Project Planning, Jun 1 to Jun 12; Foundations, Jun 15 to Jul 3; Build, Jul 6 to Sep 18; Test, Sep 21 to Oct 2; and Train & Deploy, Oct 5 to Oct 16. Production dates must come from the engagement plan rather than static configuration.

## Source reference

Implementation methodology image supplied by Sean Bradley on 2026-09-04. Treat the image as reference material. Confirm exact terminology and deliverable ownership before implementation.
