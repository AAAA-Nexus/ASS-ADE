# Skill: ass-ade rebuild

## When to use this skill

Use `ass-ade rebuild` when you need to restructure an existing codebase into a
tier-partitioned layout (`qk/`, `at/`, `mo/`, `og/`, `sy/`). This command dispatches
to the AAAA-Nexus ecosystem rebuilder and requires an active API connection.

Use `ass-ade eco-scan` first if you want a read-only inventory before committing to a
full rebuild.

## Pre-flight checklist

Before running rebuild:

- [ ] Confirm the source path exists: `ls <path>`
- [ ] Run eco-scan: `ass-ade eco-scan <path>`
- [ ] Review the eco-scan tier distribution summary
- [ ] Confirm the user has a backup or the source is in version control

## Step-by-step

1. Run the eco-scan to map what exists:
   ```
   ass-ade eco-scan <path>
   ```
2. Review the output. Look for:
   - Number of files per existing tier
   - Import graph warnings (circular imports block clean partitioning)
   - Any files already in `qk/`, `at/`, `mo/`, `og/`, `sy/` folders
3. Run the rebuild:
   ```
   ass-ade rebuild <path>
   ```
4. Wait for completion. Rebuild can take 30-300 seconds depending on codebase size.
   The command streams progress to stdout.
5. After completion, check the output folder (printed in the final line of stdout).
6. Read `BUILD_REPORT.json` in the output folder to review tier assignments.
7. Run certify on the output:
   ```
   ass-ade certify <output-folder>
   ```

## Flags and options

| Flag | Effect |
|------|--------|
| `--only-path` | Local-only mode; skips AAAA-Nexus enrichment |
| `--blueprint <file.json>` | Use a specific AAAA-SPEC-004 blueprint to guide partitioning |
| `--output <dir>` | Write output to a specific directory instead of auto-named |
| `--dry-run` | Show what would be moved without writing any files |
| `--verbose` | Emit per-file placement logs |

## Output interpretation

After a successful rebuild, the output folder contains:

```
qk/    - pure, side-effect-free primitives
at/    - stateless atoms
mo/    - stateful molecules
og/    - domain organism services
sy/    - system-level orchestrators
CERTIFICATE.json   - local tamper-evident digest (not yet signed)
BUILD_REPORT.json  - per-component placement summary
```

Key fields in `BUILD_REPORT.json`:

- `placed_count` — total files placed into tiers
- `skipped_count` — files that could not be assigned a tier (review manually)
- `tier_distribution` — map of tier name to file count
- `warnings` — files with ambiguous tier placement

## Error handling

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Proceed to certify |
| 1 | Partial failure | Check `BUILD_REPORT.json` for skipped files |
| 2 | Auth error | Check `AAAA_NEXUS_API_KEY` is set; try `--only-path` for local mode |
| 3 | Source path not found | Verify the path exists |
| 124 | Timeout | Increase timeout or use `--only-path` for large codebases |

If rebuild exits non-zero, do not run certify. Report the error from `stderr` and
stop.
