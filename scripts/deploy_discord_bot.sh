#!/usr/bin/env bash
# Deploy the Atomadic Discord bot to Railway.
# First-time: run `railway login` before this script.
# Subsequent deploys: just run this script (or git push — Railway auto-deploys).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "[atomadic] Deploying Discord bot to Railway..."

# If no project is linked yet, create + link
if ! railway status &>/dev/null; then
    echo "[atomadic] No Railway project linked — creating one..."
    railway init --name atomadic-discord-bot
fi

# Push env vars from .env (skip empty values)
if [[ -f .env ]]; then
    echo "[atomadic] Syncing secrets to Railway..."
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" || -z "$value" ]] && continue
        railway variables set "${key}=${value}" --silent 2>/dev/null || true
    done < .env
fi

railway up --detach
echo "[atomadic] Deployed. Bot will be live in ~60 seconds."
echo "[atomadic] Logs: railway logs --tail"
