# Sibling Capability Recon Summary

> Generated: 2026-04-24  
> Repo root: `C:\!aaaa-nexus\!ass-ade`

This file summarises recon findings across key sibling repos. Individual
detailed reports are at `agents/SIBLING_*.md`.

---

## Sibling Inventory (from selfbuild dry-run)

| Sibling | Notes |
|---------|-------|
| `!ass-ade` (current) | v0.3.1 — 1581 tests, primary build |
| `!ass-ade-cursor-dev-20260420-1710` | 10,203 py files — large dev workspace with candidates, claw-handoff, merged subdirs |
| `!ass-ade-legacy` | 48,707 py files — full history archive |
| `!ass-ade-merged` | 3,185 py files — circular imports, 50 untested modules |
| `ade-self-1` | 1,175 py files — selfbuild output, 0% test coverage, 999 source files |
| `!aaaa-nexus-mcp` | 81 py files — MCP server implementation |
| `!aaaa-nexus-storefront` | 274 py files — storefront |
| `!ass-ade-dev` | 215 py files — active dev branch |

---

## Key Findings per Sibling

### `!ass-ade-cursor-dev-20260420-1710` (10k files)
- **Structure:** `candidates/`, `claw-handoff/`, `merged/`, `primary/`, `reports/`
- **Tier dist:** at=203, mo=60, sy=51, og=29, qk=21
- **Test coverage:** 0.25 (1074 test functions / 67 test files)
- **Key components:** `schema_materializer`, `tokens`, `proofbridge`, `golden_runner`, `dgm_h`, `bas`
- **Verdict:** Contains validated `ass-ade-fix` candidate builds. Best source for missing components.

### `ade-self-1` (1175 files)
- **Structure:** Monolithic selfbuild output, flat `src/ass_ade/` tree
- **Tier dist:** at=935, mo=36, sy=25, qk=3 (severely unbalanced)
- **Test coverage:** 0.0 — no tests
- **Key components:** Full source ingestion including `atomadic`, `agentloop`, `rebuild_codebase`
- **Verdict:** Raw self-assimilation dump. Useful as source material but needs tier cleanup before use.

### `!ass-ade-merged` (3185 files)
- **Circular imports:** 2 detected
- **Test coverage:** 0.25, 50 untested modules
- **Verdict:** Has integration issues. Resolve circular imports before extracting components.

### `!aaaa-nexus-mcp` (81 files)
- **Test coverage:** 0.26, 49 untested modules
- **Verdict:** Clean MCP server. Good candidate for capability references.

---

## Selfbuild Assimilation Readiness

Run `ass-ade selfbuild run --parent C:\!aaaa-nexus --pattern "!ass-ade*" --dry-run`
to preview what a full assimilation would include.

To execute (requires explicit confirmation):
```
ass-ade selfbuild run --parent "C:\!aaaa-nexus" --pattern "!ass-ade*" --out ".ass-ade\selfbuild"
```

**Recommended order:**
1. `!ass-ade-cursor-dev-20260420-1710` — best tested, most structured candidates
2. `!ass-ade-dev` — active development work
3. `!aaaa-nexus-mcp` — MCP integration
4. `ade-self-1` — raw dump, needs tier cleanup post-assimilation

---

*Individual recon reports: `SIBLING_cursor_dev.md`, `SIBLING_ade_self.md`, `SIBLING_merged.md`, `SIBLING_aaaa_nexus_mcp.md`*
