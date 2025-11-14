#!/bin/bash
set -e

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "Starting Google APIs enablement at $TIMESTAMP"

APIS=(
  "gmail.googleapis.com"
  "drive.googleapis.com"
  "calendar-json.googleapis.com"
  "sheets.googleapis.com"
  "docs.googleapis.com"
  "iap.googleapis.com"
)

VERIFIED=()
FAILED=()

for api in "${APIS[@]}"; do
  echo "Enabling $api..."
  if gcloud services enable "$api" --project=edri2or-mcp 2>&1; then
    echo "✅ Enabled $api"
  else
    echo "⚠️ Issue with $api"
  fi
done

echo ""
echo "=== Verification ==="
for api in "${APIS[@]}"; do
  if gcloud services list --enabled --project=edri2or-mcp --filter="name:$api" --format="value(name)" | grep -q "$api"; then
    VERIFIED+=("$api")
    echo "✅ $api: VERIFIED ENABLED"
  else
    FAILED+=("$api")
    echo "❌ $api: NOT ENABLED"
  fi
done

echo ""
echo "=== Summary ==="
echo "Verified: ${#VERIFIED[@]}/${#APIS[@]}"
echo "Failed: ${#FAILED[@]}"

# Create result JSON
mkdir -p .ops/results
cat > .ops/results/google-apis-phase1.json <<EOF
{
  "timestamp": "$TIMESTAMP",
  "status": "success",
  "phase": "1-enable-apis",
  "method": "gcloud-direct",
  "project": "edri2or-mcp",
  "verified_count": ${#VERIFIED[@]},
  "total_count": ${#APIS[@]},
  "apis_verified": [$(printf '"%s",' "${VERIFIED[@]}" | sed 's/,$//')],
  "apis_failed": [$(printf '"%s",' "${FAILED[@]}" | sed 's/,$//')]  
}
EOF

cat .ops/results/google-apis-phase1.json

if [ ${#VERIFIED[@]} -eq ${#APIS[@]} ]; then
  echo ""
  echo "✅ ALL APIS ENABLED SUCCESSFULLY"
  exit 0
else
  echo ""
  echo "⚠️ SOME APIS FAILED"
  exit 1
fi
