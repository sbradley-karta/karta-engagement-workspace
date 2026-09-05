#!/usr/bin/env bash
# INTERIM MODE: no sign-in, download delivery, bundled template as base. Run from the repository root.
# Use until the Microsoft tenant admin approves the Karta Assembly Service app; then run deploy.sh instead.
set -euo pipefail
PROJECT="${PROJECT:-project-2c1b0888-6c19-4832-a90}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-karta-assembly}"
# Unguessable endpoint path. Fixed here so redeploys keep the same connector URL. Rotate by changing it and updating the connector.
MCP_PATH="${MCP_PATH:-/mcp-7f3c9a2e51b84d6f}"
gcloud run deploy "$SERVICE" --source . --region "$REGION" --project "$PROJECT" --allow-unauthenticated \
  --min-instances 0 --max-instances 1 --memory 1Gi --cpu 1 --timeout 300 --concurrency 10 \
  --set-env-vars "AUTH_MODE=none,MCP_PATH=${MCP_PATH},AZURE_CLIENT_ID=9056b184-4a0f-4f44-9b5f-77d52124fb0b,AZURE_TENANT_ID=e079c544-3de0-440a-a999-7f424555afff,BASE_URL=https://karta-assembly-aa57tv4ota-uc.a.run.app,REQUIRED_SCOPE=assemble,GRAPH_SCOPES=User.Read Files.ReadWrite.All,OAUTH_STORAGE=memory" \
  --set-secrets "AZURE_CLIENT_SECRET=entra-client-secret:latest,JWT_SIGNING_KEY=jwt-signing-key:latest"
URL=$(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format 'value(status.url)')
echo "Interim MCP endpoint (register this, authentication None): ${URL}${MCP_PATH}"
