# Rebuild Report

**Rebuild tag**: `20260418_220755`
**Issued**: 2026-04-19T05:08:24.390977+00:00
**Issuer**: ass_ade.engine.schema_rebuilder
**Schema**: ASSADE-SPEC-003

## Source

| Field | Value |
|-------|-------|
| Input path | `C:\!ass-ade` |
| Plan digest | `d1040d1204548b71` |
| Control root | `` |

## Output

| Field | Value |
|-------|-------|
| Components written | 2589 |
| Output folder | `C:\!ass-ade-v0.0.1-final` |

## Tier breakdown

| Tier | Count |
|------|-------|
| `a0_qk_constants` | 106 |
| `a1_at_functions` | 1330 |
| `a2_mo_composites` | 855 |
| `a3_og_features` | 82 |
| `a4_sy_orchestration` | 216 |
| **Total** | **2589** |

## Public invariants

| Invariant | Observed | Limit | Pass |
|-----------|---------|-------|------|
| D_max (depth) | ? | 23 | YES |
| epsilon_KL (dup fraction) | 0.00e+00 | 0.00e+00 | YES |
| tau_trust | 1820/1823 | ≥1820/1823 | YES |
| G_18 parity | ? mod 324 | — | — |

## Audit summary

- **Structural conformant**: YES
- **Pass rate**: 100.0%
- **Total findings**: 0
- **Valid components**: 2532 / 2532

## Certificate

- **Version**: ASSADE-SPEC-CERT-1
- **SHA-256**: `ac51fb5864a1078ec1c0b813d4e82342bd0fe5c26d8501468d4a5684bcc7e493`

Verify:
```bash
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('VERIFIED' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```
