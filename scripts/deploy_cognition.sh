#!/usr/bin/env bash
# deploy_cognition.sh — one-shot deploy of Atomadic's full-stack cognition worker.
#
# Runs every Cloudflare-side resource provisioning step (idempotent — each
# `create` swallows the "already exists" case), then deploys.
#
# Prerequisites:
#   - cd scripts && npm install      (already in package.json)
#   - npx wrangler login             (interactive, one-time)
#
# Usage (from repo root or scripts/):
#   bash scripts/deploy_cognition.sh
#
set -u

cd "$(dirname "$0")"

WRANGLER="./node_modules/.bin/wrangler"
[ -x "$WRANGLER" ] || WRANGLER="npx wrangler"

CONFIG="wrangler.cognition.toml"

run() {
  echo ""
  echo "▸ $*"
  "$@" || echo "  (continuing — likely already exists)"
}

echo "━━━ Atomadic cognition worker — full Cloudflare stack deploy ━━━"

echo ""
echo "Step 1/6: Verify auth"
$WRANGLER whoami || { echo "ERROR: run 'npx wrangler login' first"; exit 1; }

echo ""
echo "Step 2/6: AI Gateway"
run $WRANGLER ai-gateway create atomadic-gateway

echo ""
echo "Step 3/6: Queues"
run $WRANGLER queues create atomadic-thoughts
run $WRANGLER queues create atomadic-actions
run $WRANGLER queues create atomadic-memory

echo ""
echo "Step 4/6: Pre-deploy validation"
$WRANGLER deploy --config "$CONFIG" --dry-run | tail -25

echo ""
echo "Step 5/6: Deploy"
$WRANGLER deploy --config "$CONFIG"

echo ""
echo "Step 6/6: Initialize D1 schema"
WORKER_URL="https://atomadic-cognition.$($WRANGLER whoami 2>/dev/null | grep -oE '[a-z0-9-]+\.workers\.dev' | head -1 || echo 'YOUR-SUBDOMAIN.workers.dev')"
echo "  Worker URL: $WORKER_URL"
echo "  curl -X POST \"$WORKER_URL/init-db\""
curl -sS -X POST "$WORKER_URL/init-db" || echo "  (init-db will succeed once worker is propagated; retry in ~30s)"

echo ""
echo "━━━ Done ━━━"
echo ""
echo "Manual follow-ups:"
echo "  • Email Routing — dashboard: route atomadic@atomadic.tech → atomadic-cognition worker"
echo "  • Verify destination address for send_email in dashboard (thomas.openminds.openmic@gmail.com)"
echo "  • Set secrets if not already:"
echo "      $WRANGLER secret put DISCORD_WEBHOOK_URL --config $CONFIG"
echo "      $WRANGLER secret put GITHUB_TOKEN        --config $CONFIG"
echo ""
echo "Test:"
echo "  curl $WORKER_URL/status"
echo "  curl -X POST $WORKER_URL/tick"
