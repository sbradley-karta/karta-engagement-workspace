# Pages

| File | What it is |
|---|---|
| `engagement-workspace.html` | The blank engagement workspace. One engagement per published copy. Setup screen on first open; Home, Weekly Status, area views and Config after. |
| `engagement-console.html` | The earlier doTERRA sample console. Superseded by the blank workspace; kept for reference. |
| `artifacts.json` | Registry of the live claude.ai artifacts fed from this directory, with their URLs and capability manifests. |
| `make-engagement-copy.py` | Produces a titled copy of the blank page for one engagement into `dist/` (not committed). |
| `make-sample-page.py` | Produces `dist/engagement-workspace-sample.html`: the workspace running on a mock runtime with fictional data (Northwind Foods · Anaplan FP&A), for screenshots and demos. Opens in any browser; reads nothing real. |

## Publishing

Pages are published with Claude's Artifact tool from a Claude Code session. Always pass the target artifact's `url` from `artifacts.json`; publishing without it creates a new artifact.

- **Blank template:** publish `page/engagement-workspace.html` to the blank template's URL, restating the capability manifest from `artifacts.json` when tools change.
- **An engagement's copy:** run `make-engagement-copy.py` with the engagement's title, publish the file in `dist/` to that engagement's URL, and pass `title` so the claude.ai name matches.
- **A new engagement:** publish `page/engagement-workspace.html` to a new URL (no `url`), share it with the initial owner, add it to `artifacts.json`, and follow `docs/engagement-standup.md`. After the owner saves setup, republish with the engagement's title (stand-up step 6a).

Before republishing an artifact that a page has republished itself (the self-rename after setup), read the live version first; the Artifact tool refuses a publish that is not built on it.

## Rules the pages follow

Every read runs as the viewer through their own connectors. Nothing is sent automatically. Missing evidence shows as Unknown or Not assessed, never Green. Configuration is identifiers, links, dates and people, never client facts. Connector calls are wired only after a real request and response have been observed.
