# Skill: ass-ade design

## When to use this skill

Use `ass-ade design` when you want a blueprint JSON file before running a full
rebuild. Design is a planning step — it does not write any source code. Use it to:

- Validate a feature decomposition before committing to implementation
- Generate an AAAA-SPEC-004 blueprint to feed into `ass-ade rebuild --blueprint`
- Get a structured overview of how a codebase should be partitioned

## Step-by-step

1. Formulate a clear, one-sentence feature description.
2. Run design:
   ```
   ass-ade design <path> --feature "description of the feature or codebase"
   ```
3. Review the generated blueprint JSON printed to stdout.
4. Check the tier assignments in `components`. Verify:
   - No component at tier N imports from tier N+1 or higher
   - Every `entry_point` component is at the `sy.` tier
   - All `id` fields use dot-notation: `<tier>.<domain>.<ComponentName>`
5. Save the blueprint to a file:
   ```
   ass-ade design <path> --feature "..." --output blueprint.json
   ```
6. Pass the blueprint to rebuild when ready:
   ```
   ass-ade rebuild <path> --blueprint blueprint.json
   ```

## Flags and options

| Flag | Effect |
|------|--------|
| `--feature <text>` | Natural language description to guide decomposition (required) |
| `--output <file>` | Write blueprint JSON to a file instead of stdout |
| `--local-only` | Skip AAAA-Nexus enrichment; use local analysis only |
| `--format json` | Emit raw JSON (default) |
| `--format markdown` | Emit Markdown table of components |

## Output interpretation

The blueprint JSON follows AAAA-SPEC-004. Key fields:

- `schema` — always `AAAA-SPEC-004`
- `components` — list of component objects with `id`, `tier`, `role`,
  `inputs`, `outputs`, `dependencies`
- `entry_point` — the `sy.` component that top-level callers invoke
- `generated_by` — `blueprint-architect-agent` or `design-command`

A valid blueprint has:
- At least one component per tier (qk, at, mo, og, sy) for non-trivial features
- No dependency cycles
- All dependencies reference components defined in the same blueprint

## Error handling

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Review and save the blueprint |
| 1 | Analysis error | Check stderr; try `--local-only` to bypass Nexus |
| 3 | Path not found | Verify the source path exists |

If the generated blueprint has `skipped_components` in the metadata, those are files
the designer could not assign to a tier. Review them manually before using the
blueprint with `ass-ade rebuild`.
