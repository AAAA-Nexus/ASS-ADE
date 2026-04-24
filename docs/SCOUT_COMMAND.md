# Scout Command

`ass-ade scout` surveys a repository before ASS-ADE absorbs anything from it.
It gathers static intel, compares the repo against a benefit root, and then
optionally asks the configured LLM provider for a grounded synthesis.

## Examples

Scout a sibling and compare it to the current seed:

```powershell
python -m ass_ade scout ..\!aaaa-nexus-mcp --benefit-root . --json-out .ass-ade\scout-mcp.json
```

Run deterministic local-only scouting without an LLM call:

```powershell
python -m ass_ade scout ..\!aaaa-nexus-mcp --benefit-root . --no-llm
```

Run LLM synthesis but skip paid/remote Nexus guard calls:

```powershell
python -m ass_ade scout ..\!aaaa-nexus-mcp --benefit-root . --no-nexus-guards
```

Force a model for synthesis:

```powershell
python -m ass_ade scout ..\!ass-ade-dev --benefit-root . --model "llama-3.3-70b-versatile"
```

## What It Collects

- Repo shape: files, directories, file types, top-level entries.
- Traits: package files, docs, entrypoints, tests, and CI files.
- Dependency hints from `pyproject.toml`, `requirements.txt`, and `package.json`.
- Python symbol inventory and sample modules.
- Enhancement findings from the local scanner.
- Benefit mapping via the assimilation target map: `assimilate`, `rebuild`,
  `enhance`, and `skip`.
- LLM scout synthesis when `--llm` is enabled and a provider responds.
- Local grounding checks on LLM opportunities.
- Optional AAAA-Nexus guards for hallucination, output certification, trust
  score, and drift between static evidence and LLM recommendations.

The LLM is intentionally fed evidence JSON instead of raw freedom. If provider
access fails, the command still returns the static scout report with
`llm.status = "unavailable"`.
