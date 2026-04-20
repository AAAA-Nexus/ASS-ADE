# UEP v17.5 Lite Contract For ASS-ADE

ASS-ADE consumes UEP v17.5 as a public-safe operating contract, not as a
checked-in private system prompt.

The full private prompt, theorem corpus, scoring internals, and backend
orchestration logic remain outside this repository. This document captures the
lite contract ASS-ADE may implement locally while delegating sensitive gates and
premium orchestration to AAAA-Nexus.

## Boundary

ASS-ADE may expose:

- local developer utility
- public-safe protocol phases
- typed AAAA-Nexus contract calls
- local fallback checks for syntax, lint, planning, and audit artifacts
- certificates, receipts, and verdicts returned by remote services

ASS-ADE must not expose:

- the full private UEP system prompt body
- unpublished theorem bodies or proof corpora
- private scoring formulas beyond public contract names
- backend routing, policy, payment, or self-modification internals

## Lite Runtime Shape

The ASS-ADE lite runtime should follow this shape:

```text
intent
  -> local assess and plan
  -> optional Nexus preflight
  -> trusted context refresh
  -> local synthesis or tool execution
  -> AST, lint, security, and payment consent gates
  -> remote certification where enabled
  -> local audit artifact and next-step recommendation
```

Local mode stays useful without remote dependencies. Hybrid and premium modes
opt into AAAA-Nexus for stronger proof, trust, economic, and coordination
surfaces.

## Public Phase Mapping

| UEP v17.5 concept | ASS-ADE lite behavior |
| --- | --- |
| Bootstrap | Load config, profile, tool status, public contracts, and local project state. |
| Epistemic classification | Keep private classification remote; locally enforce no private prompt or theorem leakage. |
| Structural assessment | Use repo summary, plan drafting, and optional `nexus_uep_preflight` verdicts. |
| Trusted context augmentation | Use docs freshness, local project context, and optional `nexus_trusted_rag_augment`. |
| Code integrity synthesis | Use local AST/lint/security checks and optional `nexus_synthesis_guard`. |
| Wisdom audit | Emit local cycle reports and optionally submit trace to `nexus_uep_trace_certify`. |
| Autopoietic recursion | Keep self-modification planning side-effect-free locally; delegate premium planning to `nexus_autopoiesis_plan`. |

## Hook Mapping

ASS-ADE implements only the public-safe portion of each hook.

| Hook family | Local ASS-ADE responsibility | Remote or private responsibility |
| --- | --- | --- |
| Classification | Prevent private prompt, proof, and internal-constant leakage. | Full epistemic classification and theorem enforcement. |
| Never Code Blind | Track docs freshness and surface context gaps. | Trusted RAG and provenance receipts. |
| Axiom / safety | Require explicit consent for risky or billable operations. | High-confidence alignment and trust scoring. |
| AST verify | Parse, lint, type-check where available, and report failures. | Formal proof or premium synthesis certification. |
| Sandbox | Use bounded local command and file tools. | Hardened execution service where needed. |
| Audit | Write local cycle reports and recommendations. | Tamper-evident trace certification and ledger storage. |
| Trust verification | Use typed Nexus trust endpoints when remote mode is enabled. | Backend trust policy and reputation scoring. |
| Economic gate | Parse payment requirements and require explicit user consent. | x402 settlement, treasury validation, and ledger receipts. |
| PCI / formal refinement | Enforce public checks and surface missing proof status. | Private proof synthesis, FormalGrad, and security-critical proof gates. |
| Self-modification | Produce side-effect-free proposals only. | DGM, SEVerA, GVU, and auto-apply policy. |

## Engine Mapping

| UEP engine | ASS-ADE lite surface |
| --- | --- |
| SAM | `ass-ade protocol`, repo summary, local planner, optional Nexus preflight. |
| TCA | docs/context checks, remote hybrid guide, optional trusted RAG. |
| CIE | agent loop, local tools, AST/lint gate, synthesis guard contract. |
| IDE | next-move recommendations and future higher-level workflows. |
| BAS / Wisdom | cycle reports, audit reports, trace artifacts. |
| LSE | provider router, epistemic routing, model fallback. |
| x402 | payment requirement parsing, consent, and budget UX. |
| EDEE / memory | durable local task memory, planned as the next core feature. |
| CORAL / coordination | first-class coordinator over A2A, MCP, and Nexus primitives. |
| ProofBridge / FormalGrad / DGM / SEVerA / GVU | premium remote contracts or side-effect-free local planning stubs. |

## AAAA-Nexus MCP Role

The local AAAA-Nexus MCP server currently exposes a tool surface, not a resource
surface. ASS-ADE should treat it as a remote capability bridge:

- discover and inspect `nexus_*` tools
- call free and paid tools only with explicit profile and consent rules
- preserve MCP responses as public certificates or receipts
- avoid copying private backend behavior into ASS-ADE

The source server currently registers 134 unique tools across 18 modules. ASS-ADE
should consume that catalogue as a contract and not infer hidden resources when
none are advertised.

## Build Slices

### Slice 1: Durable Memory

Add local task memory with summaries, retention policy, and agent-loop hooks.
This implements the public portion of EDEE without private memory internals.

### Slice 2: Coordination

Create a coordinator over A2A discovery, Nexus discovery, swarm relay, inbox, and
consensus primitives. The coordinator should persist handoff state and audit
trails locally.

### Slice 3: Payment UX

Make billable calls explicit:

- parse 402 responses
- display cost and treasury metadata
- require consent before payment proof flow
- track local spend budget

### Slice 4: Hybrid UEP Gates

Add typed wrappers and CLI/MCP surfaces for:

- `nexus_uep_preflight`
- `nexus_trusted_rag_augment`
- `nexus_synthesis_guard`
- `nexus_aha_detect`
- `nexus_autopoiesis_plan`
- `nexus_uep_trace_certify`

### Slice 5: Editor UX

Expose the memory, coordination, payment, and gate surfaces through MCP and a VS
Code extension without expanding the private boundary.

## Acceptance Criteria

ASS-ADE's UEP v17.5 lite integration is acceptable when:

- local mode remains useful and default
- remote calls are explicit and profile-gated
- billable actions require clear user consent
- no private prompt body or theorem corpus is checked into the repo
- local checks fail closed where safety or payment is involved
- premium behavior is represented as typed contracts and certificates
- docs state the limits of the lite implementation plainly
