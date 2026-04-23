# End-to-End Workflow Gaps

This document maps the desired ASS-ADE user journey against the current implementation.

## Ideal Journey

1. Install ASS-ADE.
2. Configure a local or hybrid profile.
3. Inspect remote capabilities safely.
4. Run a task through the local agent shell.
5. Resume that task later with useful memory intact.
6. Delegate or coordinate parts of the task across agents.
7. Execute billable remote actions with clear cost and consent.
8. Use the same flows comfortably from VS Code.

## Current State By Journey Step

### 1. Install And Configure

Status: ✅ Strong

- package and CLI are already usable
- local, hybrid, and premium profile concepts exist

### 2. Capability Discovery

Status: ✅ Strong

- Nexus overview and public contract discovery exist
- MCP inspection and dry-run flows exist
- A2A discovery exists

### 3. A2A Validation And Negotiation

Status: ✅ Shipped

- validate, discover, negotiate, and local-card commands exist

### 4. Workflow Execution

Status: ✅ Strong

- hero workflows exist
- sequential pipelines exist
- progress callbacks and persistence exist

### 5. Task Resume With Memory

Status: ❌ Missing

- the agent loop does not yet have durable cross-session task memory

### 6. Multi-Agent Coordination

Status: ❌ Missing

- coordination primitives exist, but not a first-class coordination experience

### 7. Payment UX

Status: ❌ Missing

- cost visibility, consent, and budget UX remain incomplete

### 8. IDE Experience

Status: ❌ Missing

- no VS Code extension or editor-native shell exists yet

## Real Product Gap

The core journey is no longer blocked by missing A2A basics or missing pipeline persistence. The real gap is that ASS-ADE can start useful work, but it cannot yet remember or coordinate that work well enough across sessions and agents.
