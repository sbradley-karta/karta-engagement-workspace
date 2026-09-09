# Karta Engagement Delivery Workspace

Monorepo for the Karta Consulting Group engagement workspace pilot.

| Directory | Purpose |
|---|---|
| `spike/stub-server` | Gate 1 stub MCP server. Proves a published page can call an org custom connector and measures payload limits. No auth, no data. |
| `assembler` | Pure-function deck assembler: approved values in, optimized `.pptx` out. Gate 3. |
| `server` | MCP wrapper around the assembler with Microsoft Entra sign-in. Gate 3. |
| `page` | Engagement artifact site source. Gate 4 onward. |
| `docs` | Contracts, stand-up process, onboarding runbook, access test plan, Entra setup, spike notes. |
| `handover` | The governing product design and handover document, the only working copy, plus earlier handovers under `history/`. |
| `design` | Design canvas artboards and brand marks. |
| `reference` | Read-only references: the September 4 build plan page, the September 3 blueprint and mockups, design tokens, the original weekly status deck skill the assembler replaced, and the vision documents and workflow inventory. |

Governing document: `handover/karta-engagement-delivery-workspace-product-design.md` (Sean Bradley, September 2026). This repository is self-contained: nothing in it depends on a file outside it, and nothing outside it is updated from it.

Rules that do not bend: the approval gate is never skippable, nothing is sent automatically, read as the viewer, derive in code what can be derived, no local dependencies.

## Status, September 8, 2026

Gates 0 to 6 closed. The blank engagement workspace is `page/engagement-workspace.html`; stand it up with `docs/engagement-standup.md`. The doTERRA console in `page/engagement-console.html` is the earlier sample and is superseded. Gate 7, Stage 1 Prove, runs Weekly Status weekly on two engagements; its first week carries the Gate 6 exit tests (cross-engagement isolation, onboarding under an hour).

## Remote

This repository is the origin-in-waiting for the Karta GitHub organization approved on September 9, 2026. Until the organization exists, the personal GitHub repository `sbradley-karta/karta-engagement-workspace` is kept as the remote named `legacy` for backup only.

When the organization is ready, create an empty repository there named `karta-engagement-delivery-workspace` (no README, no license) and run:

```bash
git remote add origin https://github.com/<karta-org>/karta-engagement-delivery-workspace.git
git push -u origin main
```

Then move the CI secrets, if any, and retire the `legacy` remote with `git remote remove legacy`. The GitHub Actions workflow needs no change; it runs on push to any remote that hosts it.

## Publishing the pages

See `page/README.md`. Pages are published from `page/` with the target artifact's URL passed explicitly, and `page/artifacts.json` records which artifact each file feeds.
