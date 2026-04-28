# Documentation Status

This file records the current documentation policy and coverage checks so
Atomadic can personalize the public launch materials later without guessing at
the factual base.

## Current Spine

- Root README: public front door, quick start, repo map, and current gaps.
- `docs/README.md`: reading order and documentation rules.
- `docs/QUICKSTART.md`: install, verify, first scout, cherry-pick, assimilation.
- `docs/GLOSSARY.md`: plain-English definitions for non-technical readers.
- `WELCOME_ATOMADIC.md`: Atomadic orientation charter, axioms, trust wiring,
  and sovereignty rules.
- `docs/USER_MANUAL.md`: operator flows and validation checklist.
- `docs/RAG_PUBLIC_PRIVATE.md`: public/local RAG, private owner RAG, MCP
  exposure, and pending adapter status.
- `docs/ATOMADIC_WAKEUP_LAUNCH.md`: unscheduled wakeup capability, launch
  readiness command, and Cloudflare Vectorize handoff.
- `docs/SCOUT_COMMAND.md`: scout behavior and guard options.
- `docs/ASSIMILATION_TARGET_MAP.md`: selective growth policy.

## Coverage Command

Run:

```powershell
python scripts\doc_coverage.py
```

The checker scans production Python sources under `src/ass_ade`, plus repo
scripts and tools by default. It excludes caches, test fixtures, and generated
smoke artifacts. Use `--strict` when a handoff requires zero undocumented public
symbols.

Latest source-package scan from this pass:

- Command: `python scripts\doc_coverage.py --root src\ass_ade --json-out .ass-ade\state\doc-coverage.json --limit 3`
- Scanned files: 597
- Missing public doc entries: 677
- Module docstring gaps in parseable `src/ass_ade`, `scripts`, and `tools`
  files: 0

The remaining count is a real backlog of public class/function/method docstrings
and a small set of generated helper shards that need to be regenerated from real
source modules. It should be burned down in targeted slices so agents do not add
generic filler or fake imports.

Examples:

```powershell
python scripts\doc_coverage.py
python scripts\doc_coverage.py --root src\ass_ade --strict
python scripts\doc_coverage.py --json-out .ass-ade\state\doc-coverage.json
```

## Docstring Standard

- Every Python module should have a top-level docstring before
  `from __future__ import annotations`.
- Public functions, classes, and methods should have concise docstrings once
  they become part of a stable operator or integration surface.
- Private helpers may remain undocumented when their name and local context are
  clear.
- Generated fixture code is not part of the source documentation target.

## Known Gaps

- Some older markdown files still contain historical naming from sibling trees.
  Prefer the root README and this docs directory for current trunk truth.
- A few generated helper shards still fail parsing because their original
  source modules or private builder dependencies are absent in this trunk. Do
  not hide those with placeholder imports; regenerate or rebuild the helpers
  from real implementations.
- Launch copy, outreach content, and final brand voice are pending Atomadic’s
  own pass.
- Marketplace documentation stays gap-filed until the real auth, publishing, and
  blueprint registry contract exists.

## Handoff Rule

When an agent changes code behavior, it should update at least one of:

- A module/class/function docstring.
- A command doc in `docs/`.
- The user manual.
- A generated or explicit status file.

If that is not appropriate, the agent should say why in the handoff.
