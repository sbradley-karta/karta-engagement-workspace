# Karta Engagement Delivery Workspace

Monorepo for the Karta Consulting Group engagement workspace pilot.

| Directory | Purpose |
|---|---|
| `spike/stub-server` | Gate 1 stub MCP server. Proves a published page can call an org custom connector and measures payload limits. No auth, no data. |
| `assembler` | Pure-function deck assembler: approved values in, optimized `.pptx` out. Gate 3. |
| `server` | MCP wrapper around the assembler with Microsoft Entra sign-in. Gate 3. |
| `page` | Engagement artifact site source. Gate 4 onward. |
| `docs` | Contracts and decisions. The governing handover lives in the Claude working directory. |

Governing document: `karta-engagement-delivery-workspace-product-design.md` (Sean Bradley, September 2026).

Rules that do not bend: the approval gate is never skippable, nothing is sent automatically, read as the viewer, derive in code what can be derived, no local dependencies.

## Status, September 8, 2026

Gates 0 to 6 closed. The blank engagement workspace is `page/engagement-workspace.html`; stand it up with `docs/engagement-standup.md`. The doTERRA console in `page/engagement-console.html` is the earlier sample and is superseded. Gate 7, Stage 1 Prove, runs Weekly Status weekly on two engagements; its first week carries the Gate 6 exit tests (cross-engagement isolation, onboarding under an hour).
