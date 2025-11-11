#!/bin/bash
# Zero-Touch L1.2 — WIF Bootstrap Script
# Run locally with gcloud + gh CLI authenticated
# Idempotent: safe to run multiple times

set -euo pipefail

# ====== CONFIGURATION ======
export REPO="edri2or-commits/make-ops-clean"
export BRANCH="feature/pr-9-workspace-smoke"
export PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null)}"

if [ -z "$PROJECT_ID" ]; then
  echo "❌ ERROR: PROJECT_ID not set and no default gcloud project"
  echo "Set it with: export PROJECT_ID='your-project-id'"
  exit 1
fi

# ====== AUTO-DISCOVERY ======
echo "🔍 Discovering GCP environment..."
export PROJECT_NUM=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
export POOL_ID="github-pool"
export PROVIDER_ID="github-provider"
export SA_NAME="ops-mcp"
export SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "  Project: $PROJECT_ID (#$PROJECT_NUM)"
echo "  Service Account: $SA_EMAIL"
echo ""

# ====== CREATE WIF INFRASTRUCTURE ======
echo "📦 Creating Workload Identity Pool..."
if gcloud iam workload-identity-pools describe "$POOL_ID" --location=global --project="$PROJECT_ID" >/dev/null 2>&1; then
  echo "  ✅ Pool already exists"
else
  gcloud iam workload-identity-pools create "$POOL_ID" --location=global --project="$PROJECT_ID"
  echo "  ✅ Pool created"
fi

echo "🔐 Creating OIDC Provider..."
if gcloud iam workload-identity-pools providers describe "$PROVIDER_ID" \
  --location=global --workload-identity-pool="$POOL_ID" --project="$PROJECT_ID" >/dev/null 2>&1; then
  echo "  ✅ Provider already exists"
else
  gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID" \
    --location=global --workload-identity-pool="$POOL_ID" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
    --project="$PROJECT_ID"
  echo "  ✅ Provider created"
fi

echo "👤 Creating Service Account..."
if gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" >/dev/null 2>&1; then
  echo "  ✅ Service Account already exists"
else
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name="Ops MCP GitHub Actions" \
    --project="$PROJECT_ID"
  echo "  ✅ Service Account created"
fi

echo "🔗 Binding WIF to Service Account..."
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUM}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${REPO}" \
  --project="$PROJECT_ID" \
  --condition=None 2>/dev/null || echo "  ℹ️  Binding may already exist"
echo "  ✅ WIF binding configured"

echo "🔌 Enabling Google Workspace APIs..."
gcloud services enable \
  docs.googleapis.com \
  sheets.googleapis.com \
  drive.googleapis.com \
  --project="$PROJECT_ID"
echo "  ✅ APIs enabled"

echo "🎫 Granting Service Account permissions..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/editor" \
  --condition=None >/dev/null 2>&1 || echo "  ℹ️  Role may already be bound"
echo "  ✅ Permissions granted"

# ====== WRITE SECRETS TO GITHUB ======
echo "🔑 Writing secrets to GitHub..."
export WIF_PROVIDER="projects/${PROJECT_NUM}/locations/global/workloadIdentityPools/${POOL_ID}/providers/${PROVIDER_ID}"

echo -n "$WIF_PROVIDER" | gh secret set WIF_PROVIDER -R "$REPO" --app actions
echo -n "$SA_EMAIL" | gh secret set WIF_SERVICE_ACCOUNT -R "$REPO" --app actions
echo "  ✅ Secrets written"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ WIF Bootstrap Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Configuration:"
echo "  WIF_PROVIDER: $WIF_PROVIDER"
echo "  WIF_SERVICE_ACCOUNT: $SA_EMAIL"
echo ""

# ====== TRIGGER THE LOOP ======
echo "🚀 Triggering autonomous loop..."
gh api -X POST "/repos/${REPO}/dispatches" \
  -f event_type=run_dod \
  -f client_payload[target_ref]="$BRANCH"

echo ""
echo "✅ Loop triggered!"
echo ""
echo "Monitor progress:"
echo "  Actions: https://github.com/${REPO}/actions"
echo "  PR #88:  https://github.com/${REPO}/pull/88"
echo ""
echo "Expected outcome:"
echo "  1. eval-dod runs on branch: $BRANCH"
echo "  2. DoD operations: Docs replaceAllText, Sheets A1='שלום', Drive file create"
echo "  3. ops/ledger.json gets 5 entries"
echo "  4. PR #88 auto-merges"
echo ""
