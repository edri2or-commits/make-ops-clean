#!/bin/bash
set -euo pipefail

# ========================================
# MCP Remote Setup Script
# ========================================
# This script automates the full setup of:
# 1. Cloudflare Worker deployment
# 2. Secrets configuration
# 3. Connection testing
# 4. Custom connector instructions
# ========================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
WORKER_DIR="$REPO_ROOT/mcp/server/worker"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# GitHub App Configuration
APP_ID="2251005"
INSTALLATION_ID="93530674"

echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   MCP Remote Setup - Automated           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
echo ""

# ========================================
# Step 1: Check Prerequisites
# ========================================
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo -e "${RED}✗ wrangler not found. Installing...${NC}"
    npm install -g wrangler@3
else
    echo -e "${GREEN}✓ wrangler found${NC}"
fi

# Check for Cloudflare credentials
if [ -z "${CLOUDFLARE_API_TOKEN:-}" ]; then
    echo -e "${RED}✗ CLOUDFLARE_API_TOKEN not set${NC}"
    echo "Please set it: export CLOUDFLARE_API_TOKEN=your_token"
    exit 1
fi
echo -e "${GREEN}✓ Cloudflare credentials found${NC}"

# ========================================
# Step 2: Setup Secrets
# ========================================
echo ""
echo -e "${YELLOW}[2/6] Setting up Cloudflare secrets...${NC}"

cd "$WORKER_DIR"

# Check if secrets already exist
EXISTING_SECRETS=$(wrangler secret list 2>/dev/null | grep -E "APP_ID|INSTALLATION_ID" || true)

if [ -z "$EXISTING_SECRETS" ]; then
    echo -e "${BLUE}Setting APP_ID...${NC}"
    echo "$APP_ID" | wrangler secret put APP_ID
    
    echo -e "${BLUE}Setting INSTALLATION_ID...${NC}"
    echo "$INSTALLATION_ID" | wrangler secret put INSTALLATION_ID
    
    echo -e "${BLUE}Setting PRIVATE_KEY...${NC}"
    echo "⚠️  You need to paste your private key from Windows Credential Manager"
    echo "Key name: github-app-2251005-privatekey"
    echo ""
    wrangler secret put PRIVATE_KEY
    
    echo -e "${GREEN}✓ Secrets configured${NC}"
else
    echo -e "${GREEN}✓ Secrets already exist${NC}"
fi

# ========================================
# Step 3: Deploy Worker
# ========================================
echo ""
echo -e "${YELLOW}[3/6] Deploying MCP worker to Cloudflare...${NC}"

wrangler deploy

echo -e "${GREEN}✓ Worker deployed${NC}"

# ========================================
# Step 4: Get Worker URL
# ========================================
echo ""
echo -e "${YELLOW}[4/6] Fetching worker URL...${NC}"

# Get subdomain
SUBDOMAIN=$(curl -sS -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/workers/subdomain" \
    | jq -r '.result.subdomain')

# Get worker name from wrangler.toml
WORKER_NAME=$(grep -E '^name\s*=\s*"' wrangler.toml | sed -E 's/.*"([^"]+)".*/\1/')

WORKER_URL="https://${WORKER_NAME}.${SUBDOMAIN}.workers.dev"

echo -e "${GREEN}✓ Worker URL: ${WORKER_URL}${NC}"

# Save to file
echo "$WORKER_URL" > "$REPO_ROOT/mcp/server/WORKER_URL.txt"

# ========================================
# Step 5: Test Endpoints
# ========================================
echo ""
echo -e "${YELLOW}[5/6] Testing worker endpoints...${NC}"

# Test health endpoint
echo -e "${BLUE}Testing /health...${NC}"
HEALTH_RESPONSE=$(curl -s "${WORKER_URL}/health")
if echo "$HEALTH_RESPONSE" | jq -e '.ok == true' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed: $HEALTH_RESPONSE${NC}"
fi

# Test tools list
echo -e "${BLUE}Testing /tools/list...${NC}"
TOOLS_RESPONSE=$(curl -s "${WORKER_URL}/tools/list")
if echo "$TOOLS_RESPONSE" | jq -e '.ready == true' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Tools endpoint ready${NC}"
    echo "$TOOLS_RESPONSE" | jq '.tools[] | .name'
else
    echo -e "${YELLOW}⚠ Tools endpoint not fully configured${NC}"
    echo "$TOOLS_RESPONSE" | jq '.'
fi

# ========================================
# Step 6: Generate Connection Instructions
# ========================================
echo ""
echo -e "${YELLOW}[6/6] Generating connection instructions...${NC}"

cat > "$REPO_ROOT/mcp/server/CONNECTION_INSTRUCTIONS.md" << EOF
# MCP Remote Connection Instructions

## 🎯 Worker Information

**Worker URL**: \`${WORKER_URL}\`
**Deployed**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Status**: ✅ Active

## 🔗 Connect to Claude Web

### Step 1: Open Claude Settings
1. Go to [claude.ai](https://claude.ai)
2. Click on your profile
3. Navigate to **Settings** → **Integrations**

### Step 2: Add Custom Connector
1. Click **"Add custom connector"**
2. Fill in the details:
   - **Name**: \`GitHub MCP\`
   - **Type**: \`Custom MCP Server\`
   - **URL**: \`${WORKER_URL}\`
   - **Authentication**: None (handled by GitHub App)

### Step 3: Test Connection
After adding, you should see:
- ✅ Connection status: Active
- ✅ Available tools: 5

## 🛠️ Available Tools

The following tools are now available in Claude Web:

1. **github.create_ref** - Create a branch (ref) in a repo
2. **github.create_or_update_file** - Create or update a file in a repo
3. **github.create_pr** - Create a pull request
4. **github.merge_pr** - Merge a pull request
5. **github.delete_branch** - Delete a branch

## 🔍 Verification

Test the connection by asking Claude Web:
\`\`\`
Can you list the tools available through the GitHub MCP?
\`\`\`

Expected response should include the 5 tools listed above.

## 🔄 Sync with Desktop

Your Claude Desktop already has full GitHub MCP access through Docker.
This remote worker provides the same capabilities when using Claude through the web browser.

## 📊 Status Monitoring

Check worker status:
\`\`\`bash
curl ${WORKER_URL}/health
\`\`\`

Check available tools:
\`\`\`bash
curl ${WORKER_URL}/tools/list
\`\`\`

## 🆘 Troubleshooting

If the connection fails:

1. **Verify worker is running**:
   \`\`\`bash
   curl ${WORKER_URL}/health
   \`\`\`

2. **Check secrets are configured**:
   \`\`\`bash
   cd mcp/server/worker
   wrangler secret list
   \`\`\`

3. **Redeploy if needed**:
   \`\`\`bash
   cd mcp/server/worker
   wrangler deploy
   \`\`\`

4. **View worker logs**:
   \`\`\`bash
   wrangler tail
   \`\`\`

---

Generated by: \`scripts/setup-mcp-remote.sh\`
Last updated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
EOF

echo -e "${GREEN}✓ Instructions saved to: mcp/server/CONNECTION_INSTRUCTIONS.md${NC}"

# ========================================
# Final Summary
# ========================================
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Setup Complete! ✅                     ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Worker URL:${NC} ${WORKER_URL}"
echo -e "${BLUE}Instructions:${NC} mcp/server/CONNECTION_INSTRUCTIONS.md"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Open https://claude.ai"
echo "2. Go to Settings → Integrations"
echo "3. Add custom connector with URL: ${WORKER_URL}"
echo ""
echo -e "${GREEN}You're all set! 🚀${NC}"
