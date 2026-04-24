# Verified Gap Report

This report lists only gaps verified against the current codebase on 2026-04-16.

## High Confidence Gaps

### 1. Durable Agent Memory

**Severity**: High  
**Evidence**: `src/ass_ade/agent/conversation.py` stores per-run conversation state with token-aware trimming, but there is no durable memory store integrated into the agent loop.

**Impact**:

- resumed work loses context
- task continuity depends on the caller re-providing state
- coordination cannot build on persistent shared context

### 2. Agent Coordination Layer

**Severity**: High  
**Evidence**: coordination-related primitives exist in the client and CLI surface, but there is no first-class coordinator tying discovery, relay, inbox, consensus, and handoff together.

**Impact**:

- multi-agent flows are awkward to build
- orchestration lives outside the agent loop
- shared task progress is not formalized

### 3. VS Code Extension

**Severity**: Medium  
**Evidence**: no extension scaffold or editor-native package exists in the repo.

**Impact**:

- onboarding remains CLI-first
- existing MCP and agent capabilities are less accessible than they could be

### 4. x402 Payment UX

**Severity**: Medium  
**Evidence**: low-level x402 support exists, but user-facing cost estimation, consent, and budget controls are not yet first-class.

**Impact**:

- premium calls are less transparent than they should be
- cost predictability is weaker than the product needs

### 5. Richer Workflow Graphs

**Severity**: Medium  
**Evidence**: sequential pipelines with persistence and progress callbacks exist, but richer coordination-oriented graph workflows do not.

**Impact**:

- advanced scenarios still require custom orchestration
- coordination workflows are not yet packaged as reusable product features

## Not Gaps

The following are already present and should not be documented as missing:

- MCP protocol `2025-11-25`
- A2A validate, discover, negotiate, and local-card commands
- pipeline progress callbacks
- pipeline persistence
- typed error hierarchy
- retry and circuit-breaker transports
- CLI boundary validation
- hero workflows
- agent loop with streaming and tool execution
