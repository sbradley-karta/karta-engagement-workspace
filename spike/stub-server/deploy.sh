#!/usr/bin/env bash
# Deploys the stub to Cloud Run from source. Requires: gcloud auth login, billing linked.
set -euo pipefail
PROJECT="${PROJECT:-project-2c1b0888-6c19-4832-a90}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-karta-assembly-stub}"
gcloud config set project "$PROJECT" >/dev/null
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud run deploy "$SERVICE" --source . --region "$REGION" --allow-unauthenticated \
  --min-instances 0 --max-instances 2 --memory 512Mi --cpu 1 --timeout 60
echo "MCP endpoint: $(gcloud run services describe "$SERVICE" --region "$REGION" --format 'value(status.url)')/mcp"
