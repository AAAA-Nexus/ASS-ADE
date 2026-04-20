# BIRTH CERTIFICATE — ass_ade v0.0.1

> **This document is the permanent origin record.**
> It is preserved unchanged across all future rebuilds and evolutions.
> Compare against the current `CERTIFICATE.json` to measure how far this codebase has evolved.

---

## Identity

| Field | Value |
|---|---|
| Build name | **ass_ade v0.0.1 — Maiden Self-Rebuild** |
| Date/time of birth | `2026-04-20T21:38:37.975032+00:00` |
| Rebuild tag | `20260420_143836` |
| Parent (source path) | `C:\!aaaa-nexus\!ass-ade\src\ass_ade` |
| Builder | `ASS-ADE v0.0.1 (self-built)` |
| Schema | `ASSADE-SPEC-003` |
| Source plan digest | `b744bd93113c3e62` |

---

## Genesis Hash

SHA-256 of `MANIFEST.json` at birth:

```
7067a5fa7b6e7a8bec5dd99446466e942dfe3533e29381a71d89771f8067732c
```

Verify at any time:
```bash
python -c "import hashlib; print(hashlib.sha256(open('MANIFEST.json','rb').read()).hexdigest())"
```

(If this matches, the manifest is untouched since birth. If it differs, the codebase has evolved — check `REBUILD_REPORT.md` for the delta.)

---

## Initial Certificate

SHA-256 from `CERTIFICATE.json` at birth (tracks quality, not identity):

```
ecfe48be3685ce295b7a3aa1ef088df7aca3cc0e16216ca14359c6f746657b8b
```

---

## Initial Tier Distribution

| Tier | Components |
|---|---|
| `a0_qk_constants` | 41 |
| `a1_at_functions` | 475 |
| `a2_mo_composites` | 495 |
| `a3_og_features` | 31 |
| `a4_sy_orchestration` | 63 |
| **Total** | **1105** |

---

## Initial Metrics

| Metric | Value |
|---|---|
| Components materialized | 1105 |
| Audit pass rate | 100.0% |
| Audit findings | 0 |
| Structural conformant | YES |
| Test count (source) | 0 |
| Doc coverage (source) | 63% |

---

## Initial VERSION.json Snapshot

| Tier | Module count | Version |
|---|---|---|
| `a0_qk_constants` | 41 | `0.1.0` |
| `a1_at_functions` | 475 | `0.1.0` |
| `a2_mo_composites` | 495 | `0.1.0` |
| `a3_og_features` | 31 | `0.1.0` |
| `a4_sy_orchestration` | 63 | `0.1.0` |

All change types: `new` (no prior version existed).

---

## Lineage Note

This is rebuild generation **1** — the first time this codebase built itself.

Every subsequent rebuild produces a new `CERTIFICATE.json` and `REBUILD_REPORT.md`
tracking the delta from the current state. This file never changes. Future
generations can diff:

```
BIRTH_CERTIFICATE.md  ← where it started (you are reading this)
CERTIFICATE.json      ← where it is now
REBUILD_REPORT.md     ← what changed in the most recent rebuild
```

The distance between genesis hash and current certificate hash is the measure of evolution.
