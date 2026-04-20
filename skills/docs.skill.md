# Skill: ass-ade docs

## When to use this skill

Use `ass-ade docs` when you need to generate Markdown documentation from a codebase.
This command extracts Python docstrings (and JSDoc for TypeScript) and renders them
into browsable Markdown files.

Common triggers:
- After `ass-ade rebuild` to document the new tier structure
- After adding or updating docstrings and wanting to refresh the rendered output
- Before publishing or handing off a codebase

## Step-by-step

1. Ensure the source path has docstrings in public-facing modules. The docs pipeline
   only extracts documentation from files with module-level or function-level
   docstrings.
2. Run docs:
   ```
   ass-ade docs <path>
   ```
3. Read the summary from stdout: file count, output directory, any warnings.
4. Open `<output-dir>/index.md` to verify the table of contents.
5. Check `DOCS_REPORT.json` for modules with missing docstrings:
   ```json
   {"warnings": ["module_foo: no module docstring", ...]}
   ```
6. For each warning, open the flagged file and add a module-level docstring.
7. Re-run `ass-ade docs <path>` to refresh the output.

## Flags and options

| Flag | Effect |
|------|--------|
| `--output <dir>` | Write generated docs to a specific directory |
| `--serve` | Start a local HTTP server to browse the docs |
| `--format markdown` | Output Markdown (default) |
| `--format html` | Output HTML pages |
| `--local-only` | Skip AAAA-Nexus enrichment |

## Output interpretation

```
<output-dir>/
  index.md               # table of contents; start here
  api/
    <module_name>.md     # one file per public module
  DOCS_REPORT.json       # generation metadata and warnings
```

Fields in `DOCS_REPORT.json`:

- `file_count` — number of Markdown files written
- `generated_at` — ISO-8601 timestamp
- `source_path` — absolute path of the documented codebase
- `warnings` — list of modules with missing or malformed docstrings
- `errors` — list of files that could not be parsed

A docs run is considered clean when `errors` is empty. `warnings` are expected for
in-progress codebases and do not cause a non-zero exit.

## Error handling

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Review the output directory |
| 1 | Partial failure | Check `errors` in `DOCS_REPORT.json` |
| 3 | Path not found | Verify the source path exists |

If exit code is 1 and `errors` lists unparseable files, those files may have syntax
errors. Run `ass-ade lint <path>` first to catch syntax issues before running docs.
