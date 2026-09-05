# Entra app and deployment setup for the Karta assembly service

Owner: Sean Bradley. Everything here is a one-time action in the Azure portal, the Google Cloud console, or Sean's terminal. Nothing needs the Microsoft tenant admin unless the tenant blocks user consent for `Files.ReadWrite.All`.

App registration: **Karta Assembly Service**, client ID `9056b184-4a0f-4f44-9b5f-77d52124fb0b`, tenant `e079c544-3de0-440a-a999-7f424555afff`.

Predicted service URL (Cloud Run URLs in this project share the `aa57tv4ota-uc` suffix): `https://karta-assembly-aa57tv4ota-uc.a.run.app`. Verify after the first deploy and fix the redirect URI if it differs.

## 1. Expose an API

App registration, Manage, Expose an API.

1. Application ID URI: click Add, accept the default `api://9056b184-4a0f-4f44-9b5f-77d52124fb0b`, Save.
2. Add a scope: name `assemble`, who can consent `Admins and users`, admin display name `Assemble Karta decks`, admin description `Build status decks from approved values on the member's behalf`, user display name and description the same, state Enabled. Add scope.

## 2. API permissions

App registration, Manage, API permissions, Add a permission, Microsoft Graph, Delegated permissions. Add: `User.Read`, `Files.ReadWrite.All`, `offline_access`, `openid`, `profile`, `email`. Do not click Grant admin consent; members consent at first sign-in.

## 3. Redirect URI

App registration, Manage, Authentication, Add a platform, Web. Redirect URI: `https://karta-assembly-aa57tv4ota-uc.a.run.app/auth/callback`. Leave implicit grant unchecked. Save.

Cloud Run also serves every service on a second, newer URL of the form `https://<service>-926268554033.us-central1.run.app`. Add `https://karta-assembly-926268554033.us-central1.run.app/auth/callback` as a second redirect URI so either form works. The service's `BASE_URL` decides which one the connector uses; the deploy script sets the first.

## 4. Access token version

App registration, Manage, Manifest. Find `"requestedAccessTokenVersion"` and set it to `2`. Save. (If the manifest editor shows the newer format, the field sits under `api`.)

## 5. Client secret, straight into Secret Manager

Prerequisite, done once: the Secret Manager API must be enabled on the project (`gcloud services enable secretmanager.googleapis.com`). Enabled September 5, 2026.

App registration, Manage, Certificates & secrets, New client secret, description `Cloud Run`, expiry 12 months. Copy the **Value** once. Then in your terminal (zsh), run this, paste the value at the prompt (it will not echo), and press Return:

```bash
read -s "S?Entra client secret: " && printf '%s' "$S" | /opt/homebrew/bin/gcloud secrets create entra-client-secret --data-file=- --project project-2c1b0888-6c19-4832-a90 --replication-policy automatic && unset S && echo && echo stored
```

Also create the signing key for the service's own session tokens:

```bash
openssl rand -base64 48 | /opt/homebrew/bin/gcloud secrets create jwt-signing-key --data-file=- --project project-2c1b0888-6c19-4832-a90 --replication-policy automatic
```

Let the service read both secrets:

```bash
for s in entra-client-secret jwt-signing-key; do /opt/homebrew/bin/gcloud secrets add-iam-policy-binding "$s" --member=serviceAccount:926268554033-compute@developer.gserviceaccount.com --role=roles/secretmanager.secretAccessor --project project-2c1b0888-6c19-4832-a90; done
```

## 6. Deploy

From the repository root:

```bash
cd "/Users/seanbradley/Documents/Claude/Claude Various/karta-engagement-workspace" && ./server/deploy.sh
```

Then confirm the printed URL matches the redirect URI in step 3, and confirm `https://<url>/status` returns ok (from the second deploy onward; the first deploy used `/healthz`, which the Google front end answered with a 404).

## 7. Register the connector

Organization settings, Connectors, Add, Custom, Web. URL `https://karta-assembly-aa57tv4ota-uc.a.run.app/mcp`. Name exactly `Karta Assembly`. Leave the OAuth fields empty: the service handles registration itself. Then Connect it under Customize, Connectors. Sign in with your Karta Microsoft account and accept the permissions. Run the `whoami` tool from a Claude chat to confirm.

## Deployed, September 5, 2026

- Service `karta-assembly` revision 1 is serving at `https://karta-assembly-aa57tv4ota-uc.a.run.app` and `https://karta-assembly-926268554033.us-central1.run.app`.
- `/mcp` without a token returns 401 with `resource_metadata` pointing at `/.well-known/oauth-protected-resource/mcp`, which advertises the `assemble` scope and the service as its own authorization server. `/.well-known/oauth-authorization-server` exposes authorize, token, and registration endpoints. Log line confirms the Azure provider initialized for the client and tenant.
- Secrets `entra-client-secret` and `jwt-signing-key` exist and are readable by the service account.

## Tenant admin consent, required once

The Karta tenant does not allow users to consent to applications. The first sign-in shows Microsoft's Approval required screen. Two ways to clear it:

1. **Through the request.** Sean enters a justification and clicks Request approval. The tenant admin approves it in the Entra admin center under Enterprise applications, Admin consent requests.
2. **Directly.** The tenant admin opens Entra admin center, Enterprise applications, Karta Assembly Service, Permissions, and clicks Grant admin consent for Karta Consulting Group. This consents to the six delegated Graph permissions for all users.

After either, every member can connect without seeing a consent screen. The permissions are delegated only: the service can never act outside the signed-in member's own access.

## Interim mode while tenant consent is pending (September 5, 2026)

Sean's decision: run without sign-in until the admin approves, with members saving the deck to SharePoint themselves.

- `server/deploy-interim.sh` deploys with `AUTH_MODE=none`, the endpoint on an unguessable path, minimum instances zero, and the bundled optimized KCG template as the base deck. The tool returns the deck as base64; the page hands it to the member through the viewer's save dialog and points at the Status and Steer Co folder.
- Update the `Karta Assembly` connector in Organization settings: URL to the printed interim endpoint, Authentication to None. Members click Connect; no sign-in appears.
- What the open endpoint exposes: compute on one instance and the ability to render a Karta-branded deck from caller-supplied content. It stores nothing and reaches no Karta data, because the Graph path needs a member token that does not exist in this mode.
- To return to the target design after consent: run `server/deploy.sh`, set the connector URL back to `/mcp` with Authentication Always required. The page needs no change; it follows the `delivery` field the service returns.

## Interim deployment, September 5, 2026

Revision `karta-assembly-00002-svl` deployed by Sean with `AUTH_MODE=none`, `MCP_PATH=/mcp-7f3c9a2e51b84d6f`, minimum instances zero. The interim endpoint answers MCP initialize without a token; `/mcp` returns 404. Connector `Karta Assembly` re-created by Sean with the interim URL and Authentication None.

## Operating notes

- The pilot runs one always-on instance with in-memory sign-in state. A redeploy or restart signs everyone out of the connector; they sign in again on next use. A durable store is a later improvement.
- Rotate the client secret before it expires by creating a new secret version and redeploying.
- The service holds no client data at rest. Decks exist only in memory during a request.
