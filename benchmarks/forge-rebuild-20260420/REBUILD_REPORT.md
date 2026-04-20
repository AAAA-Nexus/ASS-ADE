# Rebuild Report

**Rebuild tag**: `20260420_143836`
**Issued**: 2026-04-20T22:36:05.456096+00:00
**Issuer**: ass_ade.engine.schema_rebuilder
**Schema**: ASSADE-SPEC-003

## Source

| Field | Value |
|-------|-------|
| Input path | `C:\!aaaa-nexus\!ass-ade\src\ass_ade` |
| Plan digest | `b744bd93113c3e62` |
| Control root | `` |

## Output

| Field | Value |
|-------|-------|
| Components written | 1105 |
| Output folder | `C:\!aaaa-nexus\ass-ade-forge-rebuild` |

## Tier breakdown

| Tier | Count |
|------|-------|
| `a0_qk_constants` | 41 |
| `a1_at_functions` | 475 |
| `a2_mo_composites` | 495 |
| `a3_og_features` | 31 |
| `a4_sy_orchestration` | 63 |
| **Total** | **1105** |

## Public invariants

| Invariant | Observed | Limit | Pass |
|-----------|---------|-------|------|
| depth | ? | AN-TH-DEPTH-LIMIT | YES |
| dedup (dup fraction) | 0.00e+00 | 0.00e+00 | YES |
| trust | AN-TH-TRUST-NUM/AN-TH-TRUST-DEN | ≥ `AN-TH-TRUST-FLOOR` | YES |
| parity | ? mod AN-TH-STRUCT-MOD | — | — |

## Audit summary

- **Structural conformant**: YES
- **Pass rate**: 100.0%
- **Total findings**: 0
- **Valid components**: 1101 / 1101

## Certificate

- **Version**: ASSADE-SPEC-CERT-1
- **SHA-256**: `ecfe48be3685ce295b7a3aa1ef088df7aca3cc0e16216ca14359c6f746657b8b`

Verify:
```bash
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('VERIFIED' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```
