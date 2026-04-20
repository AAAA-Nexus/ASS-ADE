# Capability Registry

`registry.json` is the source of truth for ASS-ADE feature and capability
tracking. Docs can summarize it, but merge decisions should treat this file as
the measured capability ledger.

Status values:

- `complete`: implemented and covered by local evidence.
- `partial`: usable, but with known product or integration gaps.
- `planned`: accepted direction, not yet built.
- `missing`: known gap.
- `deprecated`: intentionally retired.

Every merge candidate should either leave this registry unchanged or update it
with matching evidence. A feature claim without an evidence path is not a
feature gain.
