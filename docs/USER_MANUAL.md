# User Manual

ASS-ADE is operated through one Python package and one CLI surface. Use
`python -m ass_ade` when developing from source, or `ass-ade` / `atomadic` after
the editable install is active.

If a term feels too technical, start with [GLOSSARY.md](GLOSSARY.md). It is
written for non-technical readers first.

## Operating Model

ASS-ADE grows deliberately:

1. Scout a repo and collect evidence.
2. Map each finding to `assimilate`, `rebuild`, `enhance`, or `skip`.
3. Cherry-pick exact symbols or features.
4. Rebuild or assimilate into monadic tiers.
5. Validate with tests, lint, docs coverage, and certificates.

The system should never copy a sibling tree blindly. Every imported capability
needs a target, a reason, and a reviewable artifact.

## CLI Basics

Show the command surface:

```powershell
python -m ass_ade --help
```

Start Atomadic interactive mode:

```powershell
python -m ass_ade
```

Start chat mode against a working directory:

```powershell
python -m ass_ade chat --dir .
```

Run local health checks:

```powershell
python -m ass_ade doctor
```

## Scouting

Use `scout` before assimilation. It inspects repo shape, metadata, symbols,
tests, CI, local enhancement findings, and benefit mapping.

```powershell
python -m ass_ade scout <repo> --benefit-root . --json-out .ass-ade\scout.json
```

Useful options:

| Option | Use |
|--------|-----|
| `--no-llm` | Keep the run deterministic and local-only. |
| `--no-nexus-guards` | Skip remote guard calls while keeping LLM synthesis. |
| `--model <id>` | Override the synthesis model. |
| `--json` | Print the full report to stdout. |

## Cherry Picking

Use `cherry-pick` to turn a scout report or source directory into a manifest.

```powershell
python -m ass_ade cherry-pick .ass-ade\scout.json --target .
```

Non-interactive examples:

```powershell
python -m ass_ade cherry-pick .ass-ade\scout.json --pick 1,3,5 --no-interactive
python -m ass_ade cherry-pick .ass-ade\scout.json --pick all --no-interactive
python -m ass_ade cherry-pick <repo> --target . --action assimilate --no-interactive
```

The default manifest path is `.ass-ade/cherry_pick.json` under the target.

## Assimilation

Assimilation copies only approved manifest entries into target monadic tier
directories. It is the final step after scout and cherry-pick review.

```powershell
python -m ass_ade assimilate .ass-ade\cherry_pick.json --target .
```

Prefer `rebuild` for risky, large, private, or undertested symbols. Prefer
`enhance` when ASS-ADE already has a related implementation and the sibling repo
is better used as evidence, tests, or hardening material.

## Rebuild and Enhancement

Rebuild any source project into a tiered output:

```powershell
python -m ass_ade rebuild <source> --output <output>
```

Ask for enhancement recommendations:

```powershell
python -m ass_ade enhance <path>
```

Run monadic lint and certification:

```powershell
python -m ass_ade lint <path>
python -m ass_ade certify <path>
```

## Documentation Generation

Generate a local documentation suite for a repository:

```powershell
python -m ass_ade docs . --output .ass-ade\generated-docs
```

Check source documentation coverage:

```powershell
python scripts\doc_coverage.py
```

The coverage script is intentionally local and deterministic. It reports missing
module, class, function, and method docstrings without fabricating content.

## Public and Private RAG

ASS-ADE has two RAG boundaries:

- Public/local RAG: `context pack`, `context store`, and `context query`.
- Private/owner RAG: `search` and `search --chat` through AAAA-Nexus internal
  search endpoints.

Local context memory is stored under `.ass-ade/vector-memory/vectors.jsonl` in
the target working directory:

```powershell
python -m ass_ade context store "trusted docs packet" --namespace demo --path .
python -m ass_ade context query "trusted docs" --namespace demo --path .
```

Private RAG requires an owner session token:

```powershell
$env:ATOMADIC_SESSION_TOKEN="<owner session token>"
python -m ass_ade search "Atomadic invariants" --chat
```

See [RAG_PUBLIC_PRIVATE.md](RAG_PUBLIC_PRIVATE.md) for the full setup,
worktree findings, and pending adapter status.

## Wakeup And Launch

Atomadic has local wakeup and launch readiness commands:

```powershell
python -m ass_ade wakeup --check
python -m ass_ade launch status
```

The wakeup command is awareness-gated. It reads local time, user activity, and
once-per-day state; it does not install a timer or scheduled task. See
[ATOMADIC_WAKEUP_LAUNCH.md](ATOMADIC_WAKEUP_LAUNCH.md).

## Agents and Hooks

Agent prompts live under `agents/`. Hooks live under `hooks/`. Treat both as
operator-facing behavior: when a prompt or hook changes, update the relevant
manual or status document and run the targeted tests for that surface.

Useful files:

- `agents/README.md`
- `agents/INDEX.md`
- `agents/LIVE_CAPABILITIES.md`
- `hooks/README.md`

## Dashboard and AG-UI

The CLI exposes a local UI command:

```powershell
python -m ass_ade ui
```

Dashboard work must stay real end-to-end. Disabled marketplace or sharing flows
should state the missing backend contract instead of simulating success.

## Validation Checklist

Use this before handing work to another agent:

```powershell
python -m ruff check src tests
python -m pytest
python scripts\doc_coverage.py
```

For a narrow pass, run only the tests related to the files you changed, then
name the unrun coverage in your handoff.

## No-Stub Documentation Rule

Documentation may describe future intent only under a gap or roadmap heading.
Any command shown in a quick start or workflow section should be runnable from
the repo root, or it should be explicitly marked as pending.
