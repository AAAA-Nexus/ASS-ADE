# RECON_REPORT

**Path:** `C:\!aaaa-nexus\!aaaa-nexus-mcp`  
**Duration:** 656 ms

## Summary

Repo at `C:\!aaaa-nexus\!aaaa-nexus-mcp` contains 195 files (73 source, 18 test-related) across 7 directory levels (632.3 KB total). Test coverage: 209 test functions across 14 test files (ratio 0.26). Documentation coverage is low (47%). Dominant tier: `at`.

## Scout

- Files: 195 (632.3 KB)
- Source files: 73
- Max depth: 7
- Top-level: .claude, .cursor, .gitattributes, .github, .gitignore, .hive, .mcp.json, .opencode, .vscode, AGENTS.md

**By extension:**
  - `.md`: 77
  - `.py`: 73
  - `.json`: 20
  - `[no_ext]`: 14
  - `.sh`: 4
  - `.toml`: 2
  - `.yaml`: 2
  - `.typed`: 2

## Dependencies

- Python files: 73
- Unique external deps: 23
- Max import depth: 0
- Circular deps: none

## Tier Distribution

- `qk`: 2 — e.g. .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/__init__.py, src/aaaa_nexus_mcp/__init__.py
- `at`: 64 — e.g. .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/codex.py, .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/config.py
- `mo`: 1 — e.g. .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/count_tools.py
- `og`: 2 — e.g. .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/errors.py, src/aaaa_nexus_mcp/errors.py
- `sy`: 4 — e.g. .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/client.py, .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/tools/orchestration.py

**Violations:**
  - .hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/tools/codex_local.py (at, 25KB — may span tiers)
  - src/aaaa_nexus_mcp/tools/codex_local.py (at, 26KB — may span tiers)

## Tests

- Test files: 14
- Test functions: 209
- Coverage ratio: 0.26
- Frameworks: pytest, unittest
- Untested modules: 49

**Untested (sample):**
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/count_tools.py`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/client.py`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/config.py`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/errors.py`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/server.py`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/__main__.py`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/tools/aegis.py`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/tools/codex_local.py`

## Documentation

- README: yes
- Doc files: 77
- Public callables: 662
- Documented: 308 (47%)

**Missing docstrings (sample):**
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/count_tools.py:FakeCollector`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/count_tools.py:tool`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/count_tools.py:decorator`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/client.py:get`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/client.py:post`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/client.py:close`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/config.py:NexusConfig`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/config.py:get_config`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/errors.py:NexusError`
  - `.hive/.worktrees/public-release-cleanup/01-normalize-public-metadata/src/aaaa_nexus_mcp/errors.py:raise_for_status`

## Recommendations

1. Test coverage is low (0.26). Add tests for the 49 untested modules.
2. 2 file(s) may span tier boundaries. Split into smaller, single-purpose modules.
3. Directory depth is 7. Consider flattening the structure to reduce navigation friction.

**Next action:** Run `ass-ade lint` for detailed style and security findings.
