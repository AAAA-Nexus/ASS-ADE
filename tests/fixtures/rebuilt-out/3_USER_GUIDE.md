# User Guide

## Core commands

### ass-ade chat
Drop into an interactive session with Atomadic — the friendly front-door interpreter.
Speak casually or precisely; Atomadic derives the intent and dispatches the right command.

```bash
ass-ade chat
```

### ass-ade rebuild
Reorganize any codebase into the 5-tier monadic layout.

```bash
ass-ade rebuild ./source ./output          # full rebuild
ass-ade rebuild ./output                    # incremental update
ass-ade rebuild ./source ./output --premium # with Nexus enrichment
```

### ass-ade design
Produce a feature blueprint (AAAA-SPEC-004 JSON).

```bash
ass-ade design "Add JWT authentication" --output ./blueprints
```

### ass-ade docs
Generate or refresh documentation for any folder.

```bash
ass-ade docs ./my-project
```

### ass-ade lint
Run the CIE lint pipeline (AST + ruff + OWASP checks).

```bash
ass-ade lint ./my-project
ass-ade lint ./my-project --json
```

### ass-ade certify
Run the full certification pipeline and produce a signed CERTIFICATE.json.

```bash
ass-ade certify ./my-project
```

### ass-ade enhance
Proactively propose enhancements for any module or feature.

```bash
ass-ade enhance ./my-project
ass-ade enhance ./my-project --apply 1,3,5
```

### ass-ade eco-scan
Produce an onboarding pack for any codebase (architecture snapshot, gap report, next moves).

```bash
ass-ade eco-scan ./any-repo
```

### ass-ade doctor
Self-check: config, connectivity, test suite.

```bash
ass-ade doctor
```

## Configuration

Copy and edit the example config:

```bash
cp examples/ass-ade.config.json ~/.ass-ade.json
```

Key options:
- `profile`: `local` | `hybrid` | `premium`
- `nexus_api_key`: Your AAAA-Nexus API key (for hybrid/premium)
- `default_model`: Override the default LLM

## This rebuild

- Source: `C:\!atomadic\ass-ade-v1.1\tests\fixtures\minimal_pkg`
- Components: 5
- Rebuild tag: `20260422_232614`
- Structural conformant: YES
- CNA compatibility: compatible (0 finding(s) across 10 checked file(s))
- Generated tests: 2 (100% baseline coverage)
- Documentation coverage: 100% effective (8 inline docstrings / 8 public symbols)
- Coverage reports: `TEST_COVERAGE.md`, `DOC_COVERAGE.md`, `API_INVENTORY.md`
- Coverage manifests: `.ass-ade/coverage/test_coverage.json`, `.ass-ade/coverage/docs_coverage.json`
- Bridge languages: `typescript`, `rust`, `kotlin`, `swift`
- Bridge reports: `MULTILANG_BRIDGES.md`, `bridges/README.md`
- Bridge manifests: `.ass-ade/bridges/bridge_manifest.json`
- Output recon report: `RECON_REPORT.md`
