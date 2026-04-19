# BIRTH CERTIFICATE — !ass-ade v0.0.1

> **This document is the permanent origin record.**
> It is preserved unchanged across all future rebuilds and evolutions.
> Compare against the current `CERTIFICATE.json` to measure how far this codebase has evolved.

---

## Identity

| Field | Value |
|---|---|
| Build name | **!ass-ade v0.0.1 — Maiden Self-Rebuild** |
| Date/time of birth | `2026-04-19T03:48:30.133973+00:00` |
| Rebuild tag | `20260418_204827` |
| Parent (source path) | `C:\!ass-ade` |
| Builder | `ASS-ADE v0.0.1 (self-built)` |
| Schema | `ASSADE-SPEC-003` |
| Source plan digest | `80f30e44aef7c7d0` |

---

## Genesis Hash

SHA-256 of `MANIFEST.json` at birth:

```
2ea0e6b0bed7e47ff3844bdd46145a4007fe79f045f2c30bd037fe6cdfcab85f
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
1a2190bb0733722d9c12b244e78854a92538dc8993bf8c529ced352914919093
```

---

## Initial Tier Distribution

| Tier | Components |
|---|---|
| `a0_qk_constants` | 86 |
| `a1_at_functions` | 1076 |
| `a2_mo_composites` | 780 |
| `a3_og_features` | 63 |
| `a4_sy_orchestration` | 190 |
| **Total** | **2195** |

---

## Initial Metrics

| Metric | Value |
|---|---|
| Components materialized | 2195 |
| Audit pass rate | 100.0% |
| Audit findings | 0 |
| Structural conformant | YES |
| Test count (source) | 3800 |
| Doc coverage (source) | 39% |

---

## Initial VERSION.json Snapshot

| Tier | Module count | Version |
|---|---|---|
| `a0_qk_constants` | 86 | `0.1.0` |
| `a1_at_functions` | 1076 | `0.1.0` |
| `a2_mo_composites` | 780 | `0.1.0` |
| `a3_og_features` | 63 | `0.1.0` |
| `a4_sy_orchestration` | 190 | `0.1.0` |

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
