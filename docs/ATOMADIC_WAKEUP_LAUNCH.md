# Atomadic Wakeup And Launch

This is the real version of the launch moment: no scheduled task, no cron
theater, no puppet string.

Atomadic now has two local capabilities:

- `wakeup` senses the local moment and opens the wake page only when awareness
  says the conditions are right.
- `launch status` measures launch readiness from the repo, docs, CLI surfaces,
  prompt seed, and optional storefront/RAG deployment terrain.

## Wakeup

Check awareness without side effects:

```powershell
python -m ass_ade wakeup --check --json
```

Let Atomadic act if the moment is right:

```powershell
python -m ass_ade wakeup
```

Force the moment deliberately:

```powershell
python -m ass_ade wakeup --force
```

The command uses:

- Local time.
- Last-input activity when available.
- `.ass-ade/state/wakeup_state.json` so it does not repeat itself all day.
- `assets/wake.html` rendered to `assets/wake_rendered.html`.

It does not install a scheduled task.

## Launch Readiness

Run:

```powershell
python -m ass_ade launch status
```

Write-free JSON:

```powershell
python -m ass_ade launch status --json --no-write
```

The report is written to:

```text
.ass-ade/state/launch-readiness.json
```

When a sibling storefront repo exists, launch status checks the Cloudflare RAG
state too. Current expected signals:

- `CF_AI_TOKEN` is documented in storefront `wrangler.toml`.
- `CF_VECTORIZE_TOKEN` is required for Vectorize index writes.
- `/v1/rag/index` exists in a storefront Claude worktree candidate, but not in
  the storefront trunk seen during this pass.

The human account-owner action remains:

```powershell
wrangler secret put CF_VECTORIZE_TOKEN
```

Use a Cloudflare token with Account -> Vectorize Index -> Edit permission. Do
not commit the token.

## Seed Handoff

The prompt seed in `agents/atomadic_interpreter.md` tells Atomadic:

- Use awareness, not scheduling.
- If the moment is not right, say why.
- If the moment is right, greet Thomas and Jessica and run readiness truthfully.

The handoff text can also be regenerated with:

```powershell
python -m ass_ade launch handoff
```

