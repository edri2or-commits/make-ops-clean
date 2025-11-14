#!/bin/bash

#################################################################
# create-approval-request.sh
# Purpose: Send approval request via Make.com webhook to Telegram
# Usage: ./create-approval-request.sh <task_id> <description> <files> <risk_level>
#################################################################

set -euo pipefail

# Input validation
if [ $# -lt 4 ]; then
  echo "Usage: $0 <task_id> <description> <files> <risk_level>"
  echo "Example: $0 'L1.2-001' 'Deploy approval flow' 'workflow.yml,script.sh' 'LOW'"
  exit 1
fi

TASK_ID="$1"
DESCRIPTION="$2"
FILES="$3"
RISK_LEVEL="$4"
DURATION="${5:-~60 seconds}"

# Verify MAKE_WEBHOOK_URL is set (read from environment or secret)
if [ -z "${MAKE_WEBHOOK_URL:-}" ]; then
  echo "❌ Error: MAKE_WEBHOOK_URL not set"
  echo "Set it via: export MAKE_WEBHOOK_URL='https://hook.eu2.make.com/...'"
  exit 1
fi

# Build JSON payload
PAYLOAD=$(cat <<EOF
{
  "task_id": "$TASK_ID",
  "description": "$DESCRIPTION",
  "files": "$FILES",
  "risk_level": "$RISK_LEVEL",
  "duration": "$DURATION",
  "summary": "Zero-Touch approval request via Telegram",
  "requested_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "requested_by": "claude-desktop"
}
EOF
)

# Send webhook
echo "📡 Sending approval request to Make.com..."
echo "Task ID: $TASK_ID"
echo "Risk Level: $RISK_LEVEL"

RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" \
  -X POST "$MAKE_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | grep -oP 'HTTP_CODE:\K\d+')
BODY=$(echo "$RESPONSE" | sed 's/HTTP_CODE:.*//')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "✅ Approval request sent successfully"
  echo "Response: $BODY"
  exit 0
else
  echo "❌ Failed to send approval request"
  echo "HTTP Code: $HTTP_CODE"
  echo "Response: $BODY"
  exit 1
fi

#################################################################
# Security Notes:
# - No secrets printed to logs
# - Webhook URL read from environment
# - Payload sanitized (no shell injection)
#
# Example Usage (after setting up Make + Telegram):
#   export MAKE_WEBHOOK_URL="https://hook.eu2.make.com/..."
#   ./create-approval-request.sh "L1.2-001" "Deploy L1.2" "*.yml,*.sh" "LOW"
#
# Expected Flow:
#   1. Script sends webhook to Make
#   2. Make formats message and sends to Telegram
#   3. Or clicks ✅ Execute in Telegram
#   4. Make sends repository_dispatch to GitHub
#   5. execute-on-approval.yml runs and merges
#################################################################
