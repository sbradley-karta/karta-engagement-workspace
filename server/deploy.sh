#!/usr/bin/env bash
# Run by Sean from his terminal, from the repository root. Requires the two secrets to exist (see docs/entra-setup.md).
set -euo pipefail
PROJECT="${PROJECT:-project-2c1b0888-6c19-4832-a90}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-karta-assembly}"
BASE_URL="${BASE_URL:-https://karta-assembly-aa57tv4ota-uc.a.run.app}"
gcloud run deploy "$SERVICE" --source . --region "$REGION" --project "$PROJECT" --allow-unauthenticated \
  --min-instances 1 --max-instances 1 --memory 1Gi --cpu 1 --timeout 300 --concurrency 20 \
  --set-env-vars "AZURE_CLIENT_ID=9056b184-4a0f-4f44-9b5f-77d52124fb0b,AZURE_TENANT_ID=e079c544-3de0-440a-a999-7f424555afff,BASE_URL=${BASE_URL},REQUIRED_SCOPE=assemble,GRAPH_SCOPES=User.Read Files.ReadWrite.All,OAUTH_STORAGE=memory" \
  --set-secrets "AZURE_CLIENT_SECRET=entra-client-secret:latest,JWT_SIGNING_KEY=jwt-signing-key:latest"
echo "MCP endpoint: $(gcloud run services describe "$SERVICE" --region "$REGION" --project "$PROJECT" --format 'value(status.url)')/mcp"
