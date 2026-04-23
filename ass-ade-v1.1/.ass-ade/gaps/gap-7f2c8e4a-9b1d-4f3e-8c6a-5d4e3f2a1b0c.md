---
id: gap-7f2c8e4a-9b1d-4f3e-8c6a-5d4e3f2a1b0c
filed_by: ato-pilot-refine
parent_task: ass-ade-v1-1-greenfield-bootstrap
wave: v1.1-bootstrap
reason: Ingest currently Python-only; parity with ass-ade-v1 multi-language extractors is not implemented.
proposed_resolver: python-specialist-pure
severity: deferred
created_at: 2026-04-22T12:00:00Z
---

# Gap: Multi-language source ingest (TS/JS/RS)

## Observation

`ass_ade_v11.a0_qk_constants.exclude_dirs.SOURCE_SUFFIXES` is `{".py"}` only. `ass-ade-v1` `project_parser.py` supports `.ts`, `.tsx`, `.js`, `.jsx`, `.rs` via regex extractors.

## Required work

1. Port `TS_SYMBOL_PATTERNS`, `RS_SYMBOL_PATTERNS`, and `_extract_regex_symbols` into `ass_ade_v11.a1_at_functions` without importing `ass_ade`.
2. Extend `extract_symbols` and tests with a small fixture file per language.
3. Keep `MAX_FILE_BYTES` and exclusion rules aligned with v1.

## Blocker status

Not a blocker for phases 3–7 on **Python-only** golden fixtures; **must** resolve before claiming full v1 ingest parity.
