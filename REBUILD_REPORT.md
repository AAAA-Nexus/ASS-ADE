# Rebuild Report

**Rebuild tag**: `20260419_005513`
**Issued**: 2026-04-19T07:55:48.280808+00:00
**Issuer**: ass_ade.engine.schema_rebuilder
**Schema**: ASSADE-SPEC-003

## Source

| Field | Value |
|-------|-------|
| Input path | `C:\!ass-ade` |
| Plan digest | `ea55c602acdeff07` |
| Control root | `` |

## Output

| Field | Value |
|-------|-------|
| Components written | 2860 |
| Output folder | `C:\!ass-ade-v0.1.0-evolved-20260419-005502` |

## Tier breakdown

| Tier | Count |
|------|-------|
| `a0_qk_constants` | 123 |
| `a1_at_functions` | 1582 |
| `a2_mo_composites` | 855 |
| `a3_og_features` | 82 |
| `a4_sy_orchestration` | 218 |
| **Total** | **2860** |

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
- **Valid components**: 2758 / 2758

## Certificate

- **Version**: ASSADE-SPEC-CERT-1
- **SHA-256**: `b4936fecb3a0a81ab436946288675fb60cf9a35e3534bf50b082da348d21496f`

Verify:
```bash
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('VERIFIED' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```
