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

## 4. Access token version

App registration, Manage, Manifest. Find `"requestedAccessTokenVersion"` and set it to `2`. Save. (If the manifest editor shows the newer format, the field sits under `api`.)

## 5. Client secret, straight into Secret Manager

App registration, Manage, Certificates & secrets, New client secret, description `Cloud Run`, expiry 12 months. Copy the **Value** once. Then in your terminal, paste it when prompted:

```bash
read -s -p "Entra client secret: " S && printf '%s' "$S" | /opt/homebrew/bin/gcloud secrets create entra-client-secret --data-file=- --project project-2c1b0888-6c19-4832-a90 --replication-policy automatic && unset S && echo && echo stored
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

Then confirm the printed URL matches the redirect URI in step 3, and confirm `https://<url>/healthz` returns ok.

## 7. Register the connector

Organization settings, Connectors, Add, Custom, Web. URL `https://karta-assembly-aa57tv4ota-uc.a.run.app/mcp`. Name exactly `Karta Assembly`. Leave the OAuth fields empty: the service handles registration itself. Then Connect it under Customize, Connectors. Sign in with your Karta Microsoft account and accept the permissions. Run the `whoami` tool from a Claude chat to confirm.

## Operating notes

- The pilot runs one always-on instance with in-memory sign-in state. A redeploy or restart signs everyone out of the connector; they sign in again on next use. A durable store is a later improvement.
- Rotate the client secret before it expires by creating a new secret version and redeploying.
- The service holds no client data at rest. Decks exist only in memory during a request.
