# Tool Wrappers

This directory contains thin Python wrappers around `ass-ade` CLI commands. Each
wrapper is a standalone module that agents and scripts can import or execute directly.

## What a tool wrapper is

A tool wrapper is a Python module that:

1. Calls a `ass-ade` sub-command via `subprocess`.
2. Returns a structured `dict` with at minimum: `ok`, `exit_code`, `stdout`, `stderr`.
3. Can be run as a script from the command line.
4. Is importable as a module by agent code.

Wrappers do not implement any logic themselves. They are thin shells that translate
Python function calls into CLI invocations and parse the results.

## Available wrappers

| File | Command wrapped | Key functions |
|------|-----------------|---------------|
| `rebuild_tool.py` | `ass-ade rebuild` | `rebuild(path, ...)` |
| `design_tool.py` | `ass-ade design` | `design(path, feature, ...)` |
| `enhance_tool.py` | `ass-ade enhance` | `scan(path, ...)`, `apply(path, finding_id, ...)` |
| `docs_tool.py` | `ass-ade docs` | `generate_docs(path, ...)` |
| `certify_tool.py` | `ass-ade certify` | `certify(path, ...)`, `verify(path, ...)` |
| `prompt_tool.py` | `ass-ade prompt` | `hash_prompt(path, ...)`, `validate(...)`, `diff(...)`, `propose(...)`, `sync_agent(...)` |

## Usage

### As a module

```python
from tools.rebuild_tool import rebuild

result = rebuild("/path/to/project")
if result["ok"]:
    print("Rebuild succeeded")
else:
    print("Rebuild failed:", result["stderr"])
```

### As a script

```
python tools/rebuild_tool.py /path/to/project
python tools/certify_tool.py /path/to/project
python tools/design_tool.py /path/to/project "add payment processing"
python tools/prompt_tool.py hash agents/prompt-governor.agent.md
```

Each script prints JSON to stdout on exit.

## Return value contract

All wrappers return a dict with:

```python
{
    "ok": bool,          # True if exit_code == 0
    "exit_code": int,    # Raw process exit code
    "stdout": str,       # Captured stdout
    "stderr": str,       # Captured stderr
    # Additional keys specific to each wrapper (e.g. "certificate" for certify_tool)
}
```

## Timeout defaults

| Wrapper | Default timeout |
|---------|----------------|
| `rebuild_tool.py` | 300 seconds |
| `design_tool.py` | 120 seconds |
| `enhance_tool.py` | 120 seconds |
| `docs_tool.py` | 120 seconds |
| `certify_tool.py` | 60 seconds |

Pass `timeout=<seconds>` to override.

## Environment variables

All wrappers inherit the calling process's environment. To pass an API key:

```python
import os
os.environ["AAAA_NEXUS_API_KEY"] = "your-key"
from tools.rebuild_tool import rebuild
result = rebuild("/path")
```

Or set `AAAA_NEXUS_API_KEY` in your shell before running.
