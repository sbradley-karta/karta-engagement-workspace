# Karta Engagement Delivery Workspace

## Workflow Inventory and Automation Classification

**Status:** Strategic capability inventory  
**Date:** September 6, 2026  
**Strategy lead:** Sean Bradley  
**Scope:** North-star workflow model, not a first-release commitment

## Recommended Framing

The inventory contains 106 delivery workflow concepts. It should not be interpreted as a proposal to build 106 independent agents or product features. The workflows should be consolidated into a smaller number of end-to-end workflow families that reuse shared services, controls, records, and user experiences.

The classifications below describe the recommended primary operating model:

| Classification | Meaning |
| --- | --- |
| Agent-orchestrated | An agent may coordinate several bounded steps, sources, validations, and draft outputs. It must stop at defined human decisions. |
| AI-assisted | A person leads the workflow while AI retrieves, synthesizes, drafts, or recommends. |
| Deterministic system | Tested rules, calculations, validation, routing, state management, or artifact assembly should perform the work. |
| Human-controlled | The workflow represents an accountable review, acceptance, approval, or commercial decision. AI may prepare evidence but cannot decide. |

Product treatment is also important:

| Product treatment | Meaning |
| --- | --- |
| End-to-end workflow | A recognizable user journey with an outcome, owner, and review state. |
| Subworkflow | A reusable step within a broader end-to-end workflow. |
| Shared service | A capability used by several workflows, such as traceability, access validation, or artifact history. |
| Control gate | A required human decision or validation point. |
| Future intelligence | A later advisory capability that depends on sufficient standards, data, and evaluation. |

Roadmap posture references the horizons in the product vision. It indicates the earliest sensible product horizon, not a delivery commitment.

Plain-language definitions for every row are maintained in the companion [Workflow Descriptions](./karta-engagement-workspace-workflow-descriptions.md) reference and included directly in the spreadsheet inventory.

## Inventory Summary

| Lifecycle area | Workflow concepts |
| --- | ---: |
| Project Planning | 14 |
| Foundations | 15 |
| Build | 14 |
| Test | 16 |
| Train | 12 |
| Deploy | 12 |
| Continuous Support | 12 |
| Cross-phase | 11 |
| **Total** | **106** |

## Project Planning

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| Sales Handover | Sales-to-Delivery Continuity | Agent-orchestrated | Retrieve, synthesize, draft | Sales owner confirms accuracy; delivery owner accepts | End-to-end workflow | Horizon 3 |
| Delivery-Team Handover Acceptance | Sales-to-Delivery Continuity | Human-controlled | Prepare evidence | Delivery owner accepts or returns gaps | Control gate | Horizon 3 |
| Client and Company Brief | Sales-to-Delivery Continuity | AI-assisted | Retrieve, synthesize, draft | Engagement lead reviews sensitive and material claims | Subworkflow | Horizon 3 |
| Stakeholder Mapping | Sales-to-Delivery Continuity | AI-assisted | Retrieve, synthesize, recommend | Engagement lead confirms influence, roles, and sensitivities | Subworkflow | Horizon 3 |
| Commercial and Scope Baseline | Scope and Change Control | Deterministic system | Retrieve and structure | Commercial and delivery owners approve the baseline | Shared service | Horizon 2 |
| Use-Case Guidance | Team Enablement | AI-assisted | Retrieve, synthesize, recommend | Delivery lead selects relevant guidance | Subworkflow | Horizon 4 |
| Team Onboarding | Team Enablement | Agent-orchestrated | Retrieve, synthesize, draft | Engagement lead confirms role access and content | End-to-end workflow | Horizon 4 |
| Engagement Setup | Engagement Administration | Agent-orchestrated | Retrieve, validate, prepare action | Engagement owner approves configuration | End-to-end workflow | Horizon 2 |
| Source and Access Validation | Engagement Administration | Deterministic system | Retrieve and classify exceptions | Engagement owner resolves access gaps | Shared service | Horizon 1 to 2 |
| Kickoff Preparation | Project Mobilization | AI-assisted | Retrieve, synthesize, draft | Project manager approves client-facing material | End-to-end workflow | Horizon 3 |
| First-Two-Weeks Planning | Project Mobilization | AI-assisted | Retrieve, draft, recommend | Project manager confirms schedule and ownership | Subworkflow | Horizon 3 |
| Initial Delivery Plan | Project Mobilization | AI-assisted | Retrieve, analyze, recommend | Project manager owns commitments and sequencing | End-to-end workflow | Horizon 3 |
| Data Intake Coordination | Project Mobilization | Agent-orchestrated | Retrieve, classify, prepare action | Functional and data leads confirm requests and owners | End-to-end workflow | Horizon 3 |
| Initial RAID Assessment | Delivery Governance | AI-assisted | Retrieve, synthesize, recommend | Project manager accepts entries and ratings | Subworkflow | Horizon 3 |

## Foundations

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| Meeting Closeout | Evidence-to-Decision | Agent-orchestrated | Retrieve, synthesize, draft | Meeting owner confirms proposed records | End-to-end workflow | Horizon 3 |
| Business Requirements | Solution Definition | Agent-orchestrated | Retrieve, synthesize, draft | Functional lead and business reviewer approve | End-to-end workflow | Horizon 3 |
| Requirements Quality Review | Solution Definition | AI-assisted | Analyze and recommend | Functional lead resolves findings | Subworkflow | Horizon 3 |
| Design Document | Solution Definition | Agent-orchestrated | Retrieve, synthesize, draft | Solution owner and business reviewer approve | End-to-end workflow | Horizon 3 |
| Process Benchmark | Solution Definition | AI-assisted | Retrieve, compare, recommend | Functional lead determines relevance | Subworkflow | Horizon 3 to 4 |
| Business Process Flows | Solution Definition | Agent-orchestrated | Retrieve, structure, draft | Process owner reviews and approves | End-to-end workflow | Horizon 3 |
| Mockup Generator | Solution Definition | Agent-orchestrated | Retrieve, draft, revise | Named reviewer approves client use | End-to-end workflow | Horizon 1 to 3 |
| List and Data Matrix | Data and Architecture | AI-assisted | Retrieve, structure, draft | Data and solution leads validate | End-to-end workflow | Horizon 3 |
| Data Mapping and Gap Analysis | Data and Architecture | Agent-orchestrated | Retrieve, analyze, recommend | Data owners confirm mappings and gaps | End-to-end workflow | Horizon 3 |
| Solution Architecture | Data and Architecture | AI-assisted | Retrieve, synthesize, draft | Architect approves design and constraints | End-to-end workflow | Horizon 3 |
| Decision and Assumption Management | Evidence-to-Decision | Agent-orchestrated | Retrieve, synthesize, prepare record | Named owner confirms each retained record | Shared service | Horizon 3 to 4 |
| Design-to-Scope Reconciliation | Scope and Change Control | Agent-orchestrated | Compare, analyze, recommend | Delivery and commercial owners determine response | End-to-end workflow | Horizon 3 |
| Delivery Feasibility Review | Scope and Change Control | AI-assisted | Analyze and recommend | Project lead approves forecast and proposed response | Subworkflow | Horizon 3 |
| Scope Classification | Scope and Change Control | AI-assisted | Classify and recommend | Delivery owner confirms classification | Subworkflow | Horizon 3 |
| Change-Control Preparation | Scope and Change Control | Agent-orchestrated | Synthesize, model options, draft | Authorized commercial and client owners decide | End-to-end workflow | Horizon 3 |

## Build

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| Project Build Plan | Traceable Build | AI-assisted | Retrieve, structure, draft | Build lead approves sequencing and ownership | End-to-end workflow | Horizon 3 |
| Requirements-to-Build Traceability | Traceable Build | Deterministic system | Retrieve and identify gaps | Build and functional leads resolve gaps | Shared service | Horizon 3 |
| Data Hub Design and Validation | Data and Architecture | AI-assisted | Retrieve, analyze, recommend | Data architect approves design | End-to-end workflow | Horizon 3 |
| Model Configuration Documentation | Traceable Build | AI-assisted | Retrieve, synthesize, draft | Builder and reviewer confirm accuracy | Subworkflow | Horizon 3 |
| Dashboard and Report Specification | Traceable Build | AI-assisted | Retrieve, structure, draft | Functional lead and business reviewer approve | End-to-end workflow | Horizon 3 |
| Security Design Validation | Build Quality | AI-assisted | Compare, identify gaps, recommend | Security and solution owners approve | Control gate | Horizon 3 |
| Build Evidence Capture | Traceable Build | Agent-orchestrated | Retrieve, structure, prepare record | Builder confirms evidence and linkage | Subworkflow | Horizon 3 |
| Configuration Quality Review | Build Quality | AI-assisted | Analyze and recommend | Accountable peer reviewer decides disposition | End-to-end workflow | Horizon 5 |
| Design-Deviation Management | Scope and Change Control | Agent-orchestrated | Detect, analyze, recommend | Solution and delivery owners decide | End-to-end workflow | Horizon 3 |
| Sprint Review Preparation | Sprint Governance | Agent-orchestrated | Retrieve, synthesize, draft | Sprint owner approves agenda and evidence | Subworkflow | Horizon 3 |
| Sprint Review Record | Sprint Governance | Agent-orchestrated | Retrieve, synthesize, prepare record | Business and delivery owners confirm the record | End-to-end workflow | Horizon 3 |
| Initial Business Acceptance | Sprint Governance | Human-controlled | Prepare evidence | Authorized business reviewer records disposition | Control gate | Horizon 3 |
| Iteration and Change Monitoring | Sprint Governance | Deterministic system | Classify patterns and recommend | Delivery owner confirms intervention or change path | Future intelligence | Horizon 5 |
| AI-Assisted Development Review | Build Quality | AI-assisted | Analyze and recommend | Qualified builder or peer reviewer remains accountable | Future intelligence | Horizon 5 |

## Test

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| UAT Approach Design | Test Strategy | AI-assisted | Retrieve, analyze, recommend | Test and delivery leads select the approach | End-to-end workflow | Horizon 3 |
| UAT Readiness Planning | Test Strategy | Agent-orchestrated | Retrieve, validate, recommend | Test lead approves readiness plan | End-to-end workflow | Horizon 3 |
| Test Plan | Test Strategy | AI-assisted | Retrieve, synthesize, draft | Test lead and business owner approve | End-to-end workflow | Horizon 3 |
| UAT Test Script Generation | Test Design | Agent-orchestrated | Retrieve, draft, validate | Test and business reviewers approve scripts | End-to-end workflow | Horizon 3 |
| Coverage Analysis | Test Design | Deterministic system | Analyze and recommend | Test lead resolves accepted gaps | Shared service | Horizon 3 |
| Test Data Preparation | Test Execution | AI-assisted | Retrieve, structure, recommend | Data and test leads validate suitability | Subworkflow | Horizon 3 |
| Tester Guidance | Test Execution | AI-assisted | Draft and adapt | Test lead approves participant instructions | Subworkflow | Horizon 3 |
| Test Execution Tracking | Test Execution | Deterministic system | Retrieve, summarize, identify exceptions | Test lead manages intervention | Shared service | Horizon 3 |
| Defect Intake and Classification | Defect Management | Agent-orchestrated | Retrieve, classify, prepare record | Test or triage lead confirms classification | End-to-end workflow | Horizon 3 |
| Duplicate-Defect Detection | Defect Management | AI-assisted | Compare and recommend | Triage lead confirms merge or relationship | Subworkflow | Horizon 3 |
| Test and Enhancement Log | Defect Management | Deterministic system | Retrieve and summarize | Named owners maintain disposition | Shared service | Horizon 3 |
| Defect Triage and Summary | Defect Management | Agent-orchestrated | Analyze, synthesize, recommend | Triage group owns priority and action | End-to-end workflow | Horizon 3 |
| Retest and Regression Planning | Defect Management | AI-assisted | Analyze and recommend | Test lead approves regression scope | Subworkflow | Horizon 3 to 5 |
| UAT Measurement | Test Governance | Deterministic system | Summarize and recommend | Test lead interprets results by UAT model | Shared service | Horizon 3 to 5 |
| Test Exit Assessment | Test Governance | Agent-orchestrated | Retrieve, analyze, recommend | Test and business owners decide readiness | Control gate | Horizon 3 |
| Sign-Off Package | Test Governance | Agent-orchestrated | Retrieve, assemble, draft | Authorized business owner signs off | End-to-end workflow | Horizon 3 |

## Train

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| Training Scope and Audience Plan | Training Strategy | AI-assisted | Retrieve, structure, recommend | Training and delivery leads approve scope | End-to-end workflow | Horizon 3 |
| Administrator Training | Role-Based Training | AI-assisted | Retrieve, draft, adapt | Solution owner validates; trainer delivers | End-to-end workflow | Horizon 3 |
| Model Builder Training | Role-Based Training | AI-assisted | Retrieve, draft, adapt | Build lead validates; trainer delivers | End-to-end workflow | Horizon 3 |
| Train-the-Trainer | Role-Based Training | AI-assisted | Draft, adapt, recommend | Training lead approves; designated trainers participate | End-to-end workflow | Horizon 3 |
| End-User Training | Role-Based Training | AI-assisted | Retrieve, draft, adapt | Business and training owners approve | End-to-end workflow | Horizon 3 |
| Training Material Generation | Training Production | Agent-orchestrated | Retrieve, draft, validate | Subject-matter and training reviewers approve | End-to-end workflow | Horizon 3 |
| AI Training Video Production | Training Production | Agent-orchestrated | Draft script, narration, and scenes | Subject-matter and brand reviewers approve | Future capability | Horizon 5 |
| Administrative Runbooks | Operational Readiness | AI-assisted | Retrieve, synthesize, draft | Administrator and solution owner approve | End-to-end workflow | Horizon 3 |
| Content-to-Solution Validation | Training Quality | Deterministic system | Compare and identify gaps | Training and solution owners resolve conflicts | Shared service | Horizon 3 to 5 |
| Training Schedule and Dependency Management | Training Governance | Agent-orchestrated | Retrieve, analyze, recommend | Training and project managers approve changes | End-to-end workflow | Horizon 3 |
| Training Readiness Review | Training Governance | Agent-orchestrated | Retrieve, validate, recommend | Training and business owners decide readiness | Control gate | Horizon 3 |
| Learning Completion and Feedback | Training Governance | Deterministic system | Summarize and identify patterns | Training owner interprets results and acts | Shared service | Horizon 3 to 5 |

## Deploy

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| Deployment Planning | Release Management | Agent-orchestrated | Retrieve, structure, recommend | Deployment lead approves plan | End-to-end workflow | Horizon 3 |
| Cutover Readiness | Release Management | Agent-orchestrated | Retrieve, validate, recommend | Deployment and solution owners decide readiness | Control gate | Horizon 3 |
| Go-Live Decision Package | Release Management | Agent-orchestrated | Retrieve, synthesize, assemble | Authorized Karta and client owners approve go-live | Control gate | Horizon 3 |
| Release Communications | Release Management | AI-assisted | Draft and adapt | Named reviewer approves and person distributes | Subworkflow | Horizon 3 |
| Production Validation | Release Management | Deterministic system | Retrieve and identify exceptions | Technical and business owners confirm outcome | Control gate | Horizon 3 |
| Project Closeout | Project Closure | Agent-orchestrated | Retrieve, validate, recommend | Project and client owners approve closure | End-to-end workflow | Horizon 3 |
| Decision and RAID Closure | Project Closure | Agent-orchestrated | Retrieve, classify, prepare action | Named owners close, transfer, or defer items | Subworkflow | Horizon 3 |
| Lessons Learned | Project Closure | AI-assisted | Retrieve, synthesize, recommend | Delivery lead approves reusable conclusions | End-to-end workflow | Horizon 4 |
| Final Client Handoff | Project Closure | Agent-orchestrated | Retrieve, validate, assemble | Project and client owners accept package | End-to-end workflow | Horizon 3 |
| Hypercare Planning | Stabilization | AI-assisted | Retrieve, structure, recommend | Delivery and support leaders approve service model | End-to-end workflow | Horizon 3 |
| Hypercare Management | Stabilization | Agent-orchestrated | Retrieve, classify, summarize, recommend | Hypercare owner directs response and escalation | End-to-end workflow | Horizon 3 to 5 |
| Hypercare Exit Assessment | Stabilization | Agent-orchestrated | Retrieve, analyze, recommend | Delivery, client, and support owners decide exit | Control gate | Horizon 3 |

## Continuous Support

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| Support Handover | Support Transition | Agent-orchestrated | Retrieve, validate, assemble | Implementation and support owners approve | End-to-end workflow | Horizon 3 |
| Receiving-Team Acceptance | Support Transition | Human-controlled | Prepare evidence | Continuous Support owner accepts or returns gaps | Control gate | Horizon 3 |
| Open-Item Transition | Support Transition | Agent-orchestrated | Retrieve, classify, prepare action | Delivery and support owners confirm ownership | Subworkflow | Horizon 3 |
| Service Model Setup | Support Operations | AI-assisted | Retrieve, structure, draft | Support and client owners approve | End-to-end workflow | Horizon 3 to 6 |
| Request Classification | Support Operations | Agent-orchestrated | Classify and recommend | Support owner confirms routing and priority | Shared service | Horizon 5 |
| Issue Triage and Resolution | Support Operations | Agent-orchestrated | Retrieve, analyze, recommend, prepare action | Support owner authorizes action and closure | End-to-end workflow | Horizon 5 |
| Recurring-Issue Analysis | Support Intelligence | AI-assisted | Analyze and recommend | Support and solution leads confirm conclusions | Future intelligence | Horizon 5 |
| Solution-Health Monitoring | Support Intelligence | Deterministic system | Retrieve, detect, recommend | Support owner evaluates and acts on signals | Future intelligence | Horizon 5 |
| Enhancement Backlog | Enhancement Management | Agent-orchestrated | Retrieve, synthesize, recommend | Client and support owners prioritize | End-to-end workflow | Horizon 5 |
| Release and Regression Support | Enhancement Management | AI-assisted | Analyze, recommend, draft | Release and test leads approve | End-to-end workflow | Horizon 5 |
| Value and Roadmap Review | Enhancement Management | AI-assisted | Retrieve, synthesize, recommend | Client and account owners decide priorities | End-to-end workflow | Horizon 5 to 6 |
| Continuous-Improvement Feedback | Karta Knowledge Improvement | Agent-orchestrated | Aggregate, synthesize, recommend | Delivery Excellence approves reusable content | Future intelligence | Horizon 6 |

## Cross-Phase Workflows

| Workflow | Workflow family | Primary operating model | AI role | Required human control | Product treatment | Roadmap posture |
| --- | --- | --- | --- | --- | --- | --- |
| Engagement Home | Engagement Experience | Deterministic system | Retrieve, summarize, recommend | Engagement owner resolves configuration exceptions | Shared service | Horizon 1 |
| Project Chat | Engagement Memory | Agent-orchestrated | Retrieve, synthesize, draft | User validates answers; confirmation required before retention | End-to-end workflow | Horizon 4 |
| Weekly Status | Delivery Governance | Agent-orchestrated | Retrieve, synthesize, draft, recommend | Named reviewer approves; person distributes | End-to-end workflow | Horizon 1 |
| Decision Log | Engagement Memory | Agent-orchestrated | Retrieve, synthesize, prepare record | Named decision owner confirms record | Shared service | Horizon 3 to 4 |
| RAID Management | Delivery Governance | Agent-orchestrated | Retrieve, classify, summarize, recommend | Project manager owns ratings and actions | Shared service | Horizon 1 to 3 |
| Delivery Traceability | Delivery Control | Deterministic system | Retrieve, connect, identify gaps | Capability owners resolve or accept gaps | Shared service | Horizon 2 to 3 |
| Change Control | Scope and Change Control | Human-controlled | Retrieve, analyze, prepare options | Authorized commercial and client owners decide | End-to-end workflow | Horizon 3 |
| Artifact Library | Engagement Memory | Deterministic system | Retrieve and summarize | Named owners control approval and version state | Shared service | Horizon 1 to 2 |
| Delivery Insights | Delivery Intelligence | Agent-orchestrated | Retrieve, detect, analyze, recommend | Delivery lead assesses and owns intervention | Future intelligence | Horizon 5 |
| Team Onboarding and Development | Team Enablement | Agent-orchestrated | Retrieve, synthesize, adapt | Engagement lead confirms access and guidance | End-to-end workflow | Horizon 4 |
| Capability Catalog | Product Governance | Deterministic system | Retrieve and explain | Product and capability owners set availability | Shared service | Horizon 1 to 2 |

## Portfolio Interpretation

The 106 concepts currently consolidate into 36 workflow families. Those families, rather than the individual rows, should become the primary unit for product architecture, ownership, investment decisions, and roadmap sequencing. A later design pass may combine adjacent families further when the end-to-end user journeys and shared records are defined.

The current classification indicates four broad product patterns:

1. **End-to-end agent-orchestrated journeys** such as Sales Handover, Meeting Closeout, Business Requirements, Sprint Review, UAT Scripts, Deployment, and Support Handover.
2. **Human-led AI-assisted work** such as solution design, training development, quality review, and roadmap recommendations.
3. **Deterministic foundations and shared services** such as access validation, traceability, status logic, versioning, coverage calculations, and execution tracking.
4. **Human control gates** such as scope approval, business acceptance, test sign-off, go-live approval, hypercare exit, and support acceptance.

The next product-planning step should consolidate the workflow families into a smaller number of user journeys, define their shared records and control points, and identify which portions should be included in each release. No workflow should be labeled agentic solely because AI appears within it.
