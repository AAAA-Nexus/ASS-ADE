# Pipeline Hooks

This directory contains pipeline hook scripts and the `pipeline_config.json` that
wires them into the `ass-ade` workflow pipeline.

## What pipeline hooks are

Hooks are Python scripts that run automatically at defined points in an `ass-ade`
pipeline. They let you attach pre- and post-processing logic without modifying the
core commands.

A hook script must:

1. Define a `run(path: str) -> dict` function.
2. Return a dict with at minimum `{"ok": bool}`.
3. Be importable as a Python module.
4. Be runnable as a standalone script (`python hooks/pre_rebuild.py <path>`).

When a hook returns `{"ok": False}`, the pipeline halts and reports the failure.
The only exception is warning-only hooks that explicitly set `{"ok": True}` even
on partial failure (e.g., `pre_rebuild.py` does not block on lint warnings).

## Hook execution points

| Event | Hook | Purpose |
|-------|------|---------|
| Before `ass-ade rebuild` | `pre_rebuild` | Lint check; catch issues early |
| Before prompt/agent rollout | `pre_prompt_governance` | Audit public prompt-like artifacts for secrets, unsafe bypass language, and governance drift |
| After `ass-ade rebuild` | `post_rebuild` | Auto-certify the rebuilt folder |
| After `ass-ade rebuild` | `post_rebuild_docs` | Auto-generate documentation |

Multiple hooks for the same event are run in the order listed in `pipeline_config.json`.
All post-rebuild hooks are run even if an earlier one reports a warning, unless a hook
returns `{"ok": False}`.

## Configuration

Hooks are wired up in `pipeline_config.json`:

```json
{
  "schema": "ass-ade-pipeline-v1",
  "hooks": {
    "pre_rebuild": "hooks/pre_rebuild.py",
    "post_rebuild": ["hooks/post_rebuild.py", "hooks/post_rebuild_docs.py"]
  },
  "default_profile": "hybrid"
}
```

Paths are relative to the repository root. Use forward slashes on all platforms.

## How to run a hook manually

```
python hooks/pre_rebuild.py /path/to/project
python hooks/pre_prompt_governance.py /path/to/project
python hooks/post_rebuild.py /path/to/rebuilt-output
python hooks/post_rebuild_docs.py /path/to/rebuilt-output
```

Each script prints a JSON result to stdout.

## Adding a new hook

1. Create `hooks/<name>.py` with a `run(path: str) -> dict` function.
2. Make it executable as a standalone script (add `if __name__ == "__main__":` block).
3. Register it in `pipeline_config.json` under the appropriate event key.
4. Test it manually: `python hooks/<name>.py <test-path>`

## Available hooks

| File | Event | Blocking? |
|------|-------|-----------|
| `pre_rebuild.py` | pre_rebuild | No (lint warnings do not block) |
| `pre_prompt_governance.py` | prompt/agent rollout | Yes for critical secret or bypass-language findings |
| `post_rebuild.py` | post_rebuild | Yes (certify failure stops further post-hooks) |
| `post_rebuild_docs.py` | post_rebuild | No (docs failure is a warning) |
