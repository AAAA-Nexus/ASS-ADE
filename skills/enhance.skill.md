# Skill: ass-ade enhance

## When to use this skill

Use `ass-ade enhance` when you want to surface and apply ranked code improvements
beyond what a linter catches. The enhance pipeline combines local static analysis
with optional AAAA-Nexus semantic enrichment to find:

- Simplification opportunities (dead code, redundant branches)
- Type annotation gaps
- Performance improvements (O(n^2) -> O(n) patterns)
- Security hardening opportunities
- Documentation coverage gaps

Use `ass-ade lint` first. Enhance works best on code that is already lint-clean.

## Step-by-step

1. Run lint to establish a clean baseline:
   ```
   ass-ade lint <path>
   ```
2. Scan for enhancement opportunities:
   ```
   ass-ade enhance scan <path>
   ```
3. Review the findings table in stdout. Findings are grouped by severity.
4. For each finding you want to apply, preview the change first:
   ```
   ass-ade enhance preview <path> --finding <finding-id>
   ```
5. Review the diff shown by preview.
6. Apply the finding if the diff looks correct:
   ```
   ass-ade enhance apply <path> --finding <finding-id>
   ```
7. Re-run lint to confirm no regressions:
   ```
   ass-ade lint <path>
   ```
8. Repeat from step 4 for the next finding.

## Flags and options

### scan
| Flag | Effect |
|------|--------|
| `--local-only` | Skip Nexus enrichment; local analysis only (free) |
| `--json` | Emit findings as structured JSON |
| `--min-severity <level>` | Only show findings at this severity or higher |

### preview
| Flag | Effect |
|------|--------|
| `--finding <id>` | Show diff for a specific finding ID |

### apply
| Flag | Effect |
|------|--------|
| `--finding <id>` | Apply a specific finding |
| `--min-severity <level>` | Apply all findings at this severity or higher |
| `--dry-run` | Print what would change without writing |

## Output interpretation

Findings JSON schema:

```json
{
  "id": "enh-0042",
  "severity": "medium",
  "file": "src/foo.py",
  "line": 88,
  "title": "Replace O(n^2) dedup with set",
  "detail": "The dedup loop on lines 88-94 runs O(n^2). Replace with set(items).",
  "local": true,
  "estimated_cost": 0
}
```

- `local: true` means the finding was detected locally (no API cost).
- `estimated_cost > 0` means AAAA-Nexus enrichment was used; surface this to the user
  before applying.

## Severity reference

| Level | Policy |
|-------|--------|
| `critical` | Apply immediately; security or correctness impact |
| `high` | Apply with user confirmation |
| `medium` | Apply only after explicit user approval |
| `low` | Suggest only; do not apply without clear request |
| `info` | Informational; no action |

## Error handling

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Proceed with findings |
| 1 | Apply failed | Report stderr; do not retry the same finding |
| 2 | Auth error | Check API key; use `--local-only` for free scan |
| 3 | Path not found | Verify the source path |
