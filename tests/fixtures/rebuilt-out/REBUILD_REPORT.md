# Rebuild Report

**Rebuild tag**: `20260422_232614`
**Issued**: 2026-04-22T23:26:31.929238+00:00
**Issuer**: ass_ade.engine.schema_rebuilder
**Schema**: ASSADE-SPEC-003

## Source

| Field | Value |
|-------|-------|
| Input path | `C:\!atomadic\ass-ade-v1.1\tests\fixtures\minimal_pkg` |
| Plan digest | `369d769c80cbe38a` |
| Control root | `` |

## Output

| Field | Value |
|-------|-------|
| Components written | 5 |
| Output folder | `C:\!atomadic\ass-ade-v1.1\tests\fixtures\rebuilt-out` |

## Output verification

| Check | Value |
|-------|-------|
| Recon report | `RECON_REPORT.md` |
| CNA status | compatible |
| Files checked | 10 |
| Findings | 0 |
| Filename issues | 0 |
| Id/stem mismatches | 0 |
| Paired file mismatches | 0 |
| Tier mismatches | 0 |
| Generated tests | 2 |
| Test coverage baseline | 100% |
| Doc coverage baseline | 100% |
| Public symbols indexed | 8 |
| Bridge languages | typescript, rust, kotlin, swift |

## Coverage artifacts

| Artifact | Value |
|----------|-------|
| Coverage reports | `TEST_COVERAGE.md`, `DOC_COVERAGE.md`, `API_INVENTORY.md` |
| Coverage manifests | `.ass-ade/coverage/test_coverage.json`, `.ass-ade/coverage/docs_coverage.json` |
| Generated tests | `tests/test_generated_multilang_bridges.py`, `tests/test_generated_rebuild_integrity.py` |

## Bridge artifacts

| Artifact | Value |
|----------|-------|
| Bridge reports | `MULTILANG_BRIDGES.md`, `bridges/README.md` |
| Bridge manifests | `.ass-ade/bridges/bridge_manifest.json` |
| Bridge languages | `typescript`, `rust`, `kotlin`, `swift` |
| Bridge ready | NO |



## Tier breakdown

| Tier | Count |
|------|-------|
| `a1_at_functions` | 4 |
| `a2_mo_composites` | 1 |
| **Total** | **5** |

## Public invariants

| Invariant | Observed | Limit | Pass |
|-----------|---------|-------|------|
| depth | ? | AN-TH-DEPTH-LIMIT | YES |
| dedup (dup fraction) | 0.00e+00 | 0.00e+00 | YES |
| trust | AN-TH-TRUST-NUM/AN-TH-TRUST-DEN | ≥ `AN-TH-TRUST-FLOOR` | YES |
| parity | ? mod AN-TH-STRUCT-MOD | — | — |

## Audit summary

- **Structural conformant**: YES
- **Pass rate**: 40.0%
- **Total findings**: 3
- **Valid components**: 2 / 5

## Certificate

- **Version**: ASSADE-SPEC-CERT-1
- **SHA-256**: `c91a0b81d455632a369bee334b42aecd21703fe22b0754ff4ebff8c068aefa21`

Verify:
```bash
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('VERIFIED' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```
