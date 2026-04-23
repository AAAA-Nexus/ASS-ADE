# Architecture

## 5-tier composition law (AAAA-SPEC-003)

```
a0_qk_constants      ← stateless invariants: constants, axioms, public rules
a1_at_functions      ← pure functions operating on qk
a2_mo_composites     ← stateful compositions of at
a3_og_features       ← feature modules composed of mo
a4_sy_orchestration  ← top-level orchestration and system entry points
```

Dependencies flow strictly upward: `qk → at → mo → og → sy`.
No tier may import from a tier above it.

## Component distribution

| Tier | Count |
|------|-------|
| `a1_at_functions` | 4 |
| `a2_mo_composites` | 1 |
| **Total** | **5** |

## Dependency graph

- Cycles: **? parity** (structural-parity invariant `AN-TH-STRUCT-PARITY`, modulus AN-TH-STRUCT-MOD)
- Max chain depth: **?** (limit: AN-TH-DEPTH-LIMIT)
- Cycle violations: **0**

## Public invariants

| Invariant | Value | Conformant |
|-----------|-------|-----------|
| depth (max chain) | ? / AN-TH-DEPTH-LIMIT | YES |
| dedup (dup fraction) | 0.00e+00 | YES |
| trust (pass rate) | AN-TH-TRUST-NUM/AN-TH-TRUST-DEN | YES |
| parity (structural) | 5 components | — |

## Schema

- Component schema: AAAA-SPEC-003
- Certificate schema: AAAA-SPEC-006/CERT-1
- Issuer: `ass_ade.engine.schema_rebuilder`
