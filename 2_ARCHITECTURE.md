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
| `a0_qk_constants` | 123 |
| `a1_at_functions` | 1582 |
| `a2_mo_composites` | 855 |
| `a3_og_features` | 82 |
| `a4_sy_orchestration` | 218 |
| **Total** | **2860** |

## Dependency graph

- Cycles: **? parity** (G_18 modulus 324)
- Max chain depth: **?** (limit: 23)
- Cycle violations: **0**

## Public invariants

| Invariant | Value | Conformant |
|-----------|-------|-----------|
| D_max (max depth) | ? / 23 | YES |
| epsilon_KL (dup fraction) | 0.00e+00 | YES |
| tau_trust (pass rate) | 1820/1823 | YES |
| G_18 (structural parity) | 2860 components | — |

## Schema

- Component schema: AAAA-SPEC-003
- Certificate schema: AAAA-SPEC-006/CERT-1
- Issuer: `ass_ade.engine.schema_rebuilder`
