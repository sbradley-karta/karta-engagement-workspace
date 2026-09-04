# Gate 1 spike observations

## Stub deployment

- Service: `karta-assembly-stub`, Cloud Run, us-central1, project `project-2c1b0888-6c19-4832-a90`.
- Deployed September 4, 2026 by Sean Bradley from his terminal after granting `roles/cloudbuild.builds.builder` to the default compute service account, which a new project no longer receives automatically.
- MCP endpoint: `https://karta-assembly-stub-aa57tv4ota-uc.a.run.app/mcp`
- Probe: JSON-RPC `initialize` over streamable HTTP returned HTTP 200, `text/event-stream`, server name `Karta Assembly Test`, FastMCP 2.14.7, protocol 2025-06-18.
- No authentication by design. Delete the service after Gate 1.

## Connector registration

- Org custom connector display name: `Karta Assembly Test` (the page addresses connectors by display name).
- Registered by: pending.

## Observations from the test page

Pending. Record here: whether `claude.use("mcp")` resolves the connector, the `result.payload` shape for each tool, the largest `blob` size that arrives intact, the largest `echo_size` argument accepted, and the Microsoft 365 `sharepoint_upload_file` request and response for a small real deck into a test folder.
