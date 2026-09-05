# Gate 1 spike observations

## Stub deployment

- Service: `karta-assembly-stub`, Cloud Run, us-central1, project `project-2c1b0888-6c19-4832-a90`.
- Deployed September 4, 2026 by Sean Bradley from his terminal after granting `roles/cloudbuild.builds.builder` to the default compute service account, which a new project no longer receives automatically.
- MCP endpoint: `https://karta-assembly-stub-aa57tv4ota-uc.a.run.app/mcp`
- Probe: JSON-RPC `initialize` over streamable HTTP returned HTTP 200, `text/event-stream`, server name `Karta Assembly Test`, FastMCP 2.14.7, protocol 2025-06-18.
- No authentication by design. Delete the service after Gate 1.

## Connector registration

- Org custom connector display name: `Karta Assembly Test` (the page addresses connectors by display name).
- Registered by Sean Bradley on September 4, 2026 as an org custom connector, no auth. Connected for his account. Visible to the test page as `Karta Assembly Test`, authStatus `connected`, tools `hello`, `blob`, `echo_size`.

## Observations from the test page

Test page: `https://claude.ai/code/artifact/962bcabf-db9b-4c45-b967-d74d548cb268` (source `spike/test-page/gate1-test.template.html`). Results persisted in the page database at `gate1/observations`; the page resets the document on each load, so earlier runs are recorded here.

### Run 1, September 4, 2026 22:38 to 22:41 UTC (Sean)

| Test | Result |
|---|---|
| Runtime | `claude.use("mcp")` and `claude.use("db")` both resolved. Both connectors `connected`. |
| hello | Passed. `result.payload` is the tool's structured object; `structuredContent` present; one text block of 78 chars. 1,345 ms. |
| Connector to page ladder | Passed at 256 KB, 512 KB, 1 MiB, 2 MiB, 4 MiB. Every payload arrived intact by SHA-256. 0.8 to 3.0 s each. Cloud Run logs show each request reaching the stub and returning HTTP 200 with response bodies up to 11.2 MB. |
| Page to connector, 1 MiB argument | Failed with `server_unavailable`, message `request failed`, `retryable: true`. No corresponding request in Cloud Run logs. The connector layer refused the call before it left Claude. Ceiling is below 1.4 MB of JSON argument; exact value not yet measured (argument ladder added to the page, not yet run). |

### Run 2, September 4, 2026 22:47 UTC (Sean, reload only)

Microsoft 365 tool visibility to a published page, from `listTools()` intersected with a six-tool manifest:

| Declared | Visible to the page |
|---|---|
| `sharepoint_folder_search` | yes |
| `sharepoint_search` | yes |
| `outlook_create_draft` | yes |
| `sharepoint_upload_file` | **no** |
| `sharepoint_update_file` | **no** |
| `sharepoint_create_folder` | **no** |

The SharePoint write tools that a Claude session can use are not exposed to artifact pages. This is not a blanket write filter, since the Outlook draft tool is visible. **A page cannot upload a deck to SharePoint through the viewer's Microsoft 365 connector.** Steps 5 and 6 of the test page cannot pass and were not run.

### Consequences for the design

1. Decision 17 holds. A page can call a Karta custom connector and receive multi-megabyte results.
2. Decision 18 (page uploads the deck through the viewer's Microsoft 365 connector) is not implementable. Proposed replacement, pending Sean: the assembly service writes the deck to the engagement's SharePoint folder itself, through Microsoft Graph with delegated permission obtained during the same Microsoft sign-in the connector already requires. The write still happens as the signed-in member. Fallback: the service returns the deck and the page offers it to the viewer through `downloads`, and the member saves it to SharePoint by hand.
3. The 1 MiB connector cap on deck size no longer applies if Graph does the write. Deck optimization remains worthwhile for the connector-to-page return path and for email, but is no longer a hard gate.
4. Approved values sent from the page to the service are a few kilobytes and are unaffected by the argument ceiling. Measure the ceiling anyway (step 3 ladder) so the contract has a documented bound.

### Run 3, September 5, 2026 00:53 to 00:56 UTC (Sean)

| Test | Result |
|---|---|
| hello | Passed again, 1,264 ms. |
| Connector to page ladder | Passed again to 4 MiB. |
| Page to connector argument ladder | Accepted 64, 128, 256, 384, and 512 KB of binary (699,052 base64 chars). Refused at 768 KB (1,048,576 base64 chars) with `upstream_error`, message `request failed (400)`, not retryable. **Ceiling is a request body of about 1 MiB**; the 768 KB payload's base64 alone reaches that figure before the JSON envelope. Approved values are a few kilobytes and unaffected. |
| Folder search | Passed. `payload` was the first result object only. The connector returned eleven text blocks, one per folder plus a paging trailer, with no `structuredContent`. **Page code must iterate `result.content` text blocks, not just `payload`, for Microsoft 365 list results.** The test page's parser stopped at `payload` and saw one folder; corrected in the note here, not in the throwaway page. 2,342 ms. |
| Upload tiny deck | Failed with `approval_required`, message `this tool requires per-call approval, which is not yet supported in artifacts`. Nothing was written. This is the precise reason SharePoint write tools are hidden from pages: org policy marks them as requiring per-call approval, and artifacts cannot present that approval today. The wording `not yet` suggests a platform capability that may arrive later. |

### Gate 1 verdict

**Passed for the assembly-service path.** A published page calls a Team custom connector by display name, sends arguments up to about 1 MiB, and receives results intact to at least 4 MiB.

**Failed for page-side SharePoint writes.** The Microsoft 365 connector's write tools require per-call approval, which artifact pages cannot provide. The deck cannot be uploaded from the page.

### Decisions affected

- Decision 17 confirmed by evidence.
- Decision 18 mechanism must change. Recommendation: the assembly service writes the deck to SharePoint through Microsoft Graph with delegated permission granted at the member's Microsoft sign-in. Fallback: `downloads` hand-off to the member.
- Contract bound for the page-to-service request: keep the approved-values document under 512 KB of JSON, with a hard check in the page.

### Cleanup once Sean closes the gate

- Delete Cloud Run service `karta-assembly-stub` (Sean, from his terminal): `gcloud run services delete karta-assembly-stub --region us-central1 --project project-2c1b0888-6c19-4832-a90`
- Remove the `Karta Assembly Test` connector from Organization settings, Connectors.
- Republish the test page with `capabilities: {}` or delete the artifact.
