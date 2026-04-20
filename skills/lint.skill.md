# Skill: ass-ade lint

## When to use this skill

Use `ass-ade lint` before any write operation on a codebase. Linting is the fastest
way to catch issues before they propagate to rebuild, certify, or docs.

Required before:
- `ass-ade rebuild` (pre-rebuild hook runs this automatically if configured)
- Committing code changes
- Submitting a codebase for certification

## Step-by-step

1. Run lint with JSON output for machine-readable findings:
   ```
   ass-ade lint <path> --json
   ```
2. Review the findings grouped by file and severity.
3. Count errors vs warnings. The target is zero errors.
4. For fixable findings, run auto-fix:
   ```
   ass-ade lint <path> --fix
   ```
5. Re-run lint to confirm the fix resolved the findings:
   ```
   ass-ade lint <path> --json
   ```
6. For unfixable errors, read the relevant code and write the corrected version.
7. Repeat until lint exits 0 with zero errors.

## Flags and options

| Flag | Effect |
|------|--------|
| `--json` | Emit findings as structured JSON to stdout |
| `--fix` | Apply safe auto-fixes in place |
| `--local-only` | Skip AAAA-Nexus CIE enrichment; run local linters only |
| `--min-severity <level>` | Only report findings at this level or higher |
| `--file <path>` | Lint a single file instead of an entire directory |

## Output interpretation

Each finding in `--json` output:

```json
{
  "tool": "ruff",
  "path": "src/foo.py",
  "line": 42,
  "col": 10,
  "code": "F401",
  "message": "'os' imported but unused",
  "severity": "error",
  "fixable": true,
  "source": "local"
}
```

- `source: "local"` — detected by a local linter (ruff, mypy, pyright)
- `source: "nexus"` — detected by the AAAA-Nexus CIE gate (OWASP, semantic)
- `fixable: true` — `--fix` can resolve this automatically

## Linter auto-detection

`ass-ade lint` detects which tools are available based on project config:

| Config present | Tool used |
|---------------|-----------|
| `[tool.ruff]` in `pyproject.toml` | ruff |
| `mypy.ini` or `[tool.mypy]` | mypy |
| `pyrightconfig.json` | pyright |
| API key present and `--local-only` not set | Nexus CIE gate |

If no local linter is detected and `--local-only` is set, lint will report a
configuration warning and exit 0 with no findings.

## Error handling

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 0 | No errors found | Proceed |
| 1 | Errors found | Fix errors before proceeding |
| 2 | Linter tool not found | Install the required linter |
| 3 | Path not found | Verify the path exists |

A lint exit code of 1 blocks the pre-rebuild hook. Fix all errors before
running `ass-ade rebuild`.
