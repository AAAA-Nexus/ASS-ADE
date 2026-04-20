# Next Moves

ASS-ADE is already a credible public shell. The next work should stop treating shipped infrastructure as missing and move directly to the gaps that still matter.

## Immediate Priorities

These priorities are framed by the public release contract: ASS-ADE should
implement the public shell, memory, coordination, payment UX, and typed gate
adapters while leaving private orchestration and verification internals behind
AAAA-Nexus.

### 1. Durable Agent Memory

Add a local memory layer that survives process restarts and can be attached to task execution.

Target deliverables:

- per-task memory records
- summary snapshots for previous runs
- configurable pruning and retention
- memory read and write hooks in the agent loop

Why this matters:

- current conversation memory is per-run only
- long-running or resumed work loses useful context
- durable memory is the prerequisite for serious coordination

### 2. Agent Coordination Layer

Build a first-class coordinator over the primitives already exposed through A2A and Nexus.

Target deliverables:

- delegation and handoff state
- shared task context
- result collection and consolidation
- durable coordination audit trail

Why this matters:

- the repo already has discovery, relay, inbox, and consensus-related surfaces
- what is missing is orchestration, not raw protocol access

### 3. x402 Payment UX

Add explicit client-side cost and consent handling for billable calls.

Target deliverables:

- parse `402 Payment Required` metadata
- estimate cost before execution
- require explicit confirmation for paid calls
- track budget usage locally

### 4. VS Code Extension

Put the existing CLI and MCP server behind an editor-native UX.

Target deliverables:

- extension scaffold
- MCP onboarding and registration helpers
- workflow and memory views
- cost and status surfaces in-editor

### 5. Higher-Level Coordination Workflows

Ship workflows that prove the value of memory and coordination.

Candidates:

- `audit-full`
- `onboard-agent`
- `deploy-guard`
- multi-agent review and certification flows

## Constraint

Do not move private orchestration logic into ASS-ADE. When in doubt, expose a typed client, a public contract, or a degraded local fallback instead.
