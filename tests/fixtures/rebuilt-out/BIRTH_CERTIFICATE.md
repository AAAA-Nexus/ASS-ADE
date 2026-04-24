# BIRTH CERTIFICATE — minimal_pkg v0.0.1

> **This document is the permanent origin record.**
> It is preserved unchanged across all future rebuilds and evolutions.
> Compare against the current `CERTIFICATE.json` to measure how far this codebase has evolved.

---

## Identity

| Field | Value |
|---|---|
| Build name | **minimal_pkg v0.0.1 — Maiden Self-Rebuild** |
| Date/time of birth | `2026-04-22T23:26:14.515587+00:00` |
| Rebuild tag | `20260422_232614` |
| Parent (source path) | `C:\!atomadic\ass-ade-v1.1\tests\fixtures\minimal_pkg` |
| Builder | `ASS-ADE v0.0.1 (self-built)` |
| Schema | `ASSADE-SPEC-003` |
| Source plan digest | `369d769c80cbe38a` |

---

## Genesis Hash

SHA-256 of `MANIFEST.json` at birth:

```
9fd124a1f6974ed64dcf3541505d44594f02f5c0be1c95ddbd72d1ed6e745a1d
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
c91a0b81d455632a369bee334b42aecd21703fe22b0754ff4ebff8c068aefa21
```

---

## Initial Tier Distribution

| Tier | Components |
|---|---|
| `a0_qk_constants` | 0 |
| `a1_at_functions` | 4 |
| `a2_mo_composites` | 1 |
| `a3_og_features` | 0 |
| `a4_sy_orchestration` | 0 |
| **Total** | **5** |

---

## Initial Metrics

| Metric | Value |
|---|---|
| Components materialized | 5 |
| Audit pass rate | 40.0% |
| Audit findings | 3 (BODY_HASH_MISMATCH: 3) |
| Structural conformant | YES |
| Test count (source) | 0 |
| Doc coverage (source) | 60% |

---

## Initial VERSION.json Snapshot

| Tier | Module count | Version |
|---|---|---|
| `a0_qk_constants` | 0 | `0.1.0` |
| `a1_at_functions` | 4 | `0.1.0` |
| `a2_mo_composites` | 1 | `0.1.0` |
| `a3_og_features` | 0 | `0.1.0` |
| `a4_sy_orchestration` | 0 | `0.1.0` |

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
