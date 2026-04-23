# Perfect Workflow Derivation

This document defines the ASS-ADE operating loop for the sovereign axiom:

> If the technology for the job does not exist, invent it.

The workflow begins with **Never Code Blind** Phase 0 recon, then reaches
`MAP = TERRAIN`: before execution, the system maps the task to the current
terrain of agents, hooks, skills, tools, harnesses, prompts, and instructions.
If the terrain cannot support the task, the task halts and a capability
development packet is produced.

## Verdicts

| Verdict | Meaning |
| --- | --- |
| `PROCEED` | All required capabilities exist. Continue to synthesis/execution. |
| `HALT_AND_INVENT` | At least one required capability is missing. Do not execute the original task. Build and verify the missing asset first. |

## Capability Types

| Type | Examples | Creation Lane |
| --- | --- | --- |
| Agent | `security_scanner`, `release_marshal` | `nexus_spawn_agent`, human approval required |
| Hook | `pre_merge`, `trust_gate` | verified code synthesis |
| Skill | `python_ast_analysis`, `trusted_rag_design` | skill distillation or verified code synthesis |
| Tool | `nexus_semgrep_scan`, `map_terrain` | verified code synthesis |
| Harness | `gvisor_sandbox`, `redacted_admin_probe` | secure handoff and sandbox template |
| Prompt | `router_pack`, `blueprint_architect` | prompt optimization plus rebuild-backed packet generation |
| Instruction | `router_rules`, `repo_policy_pack` | verified code synthesis plus rebuild-backed packet generation |

## Current Implementation

ASS-ADE has a local Phase 0 recon and context-memory layer:

- module: `src/ass_ade/recon.py`
- module: `src/ass_ade/context_memory.py`
- CLI: `ass-ade workflow phase0-recon`
- CLI: `ass-ade context pack`
- CLI: `ass-ade context store`
- CLI: `ass-ade context query`
- local MCP tools: `phase0_recon`, `context_pack`,
  `context_memory_store`, `context_memory_query`

ASS-ADE now has a local `map_terrain` engine and MCP tool:

- module: `src/ass_ade/map_terrain.py`
- CLI: `ass-ade workflow map-terrain`
- local MCP tool: `map_terrain`

The direct AAAA-Nexus MCP source now has the matching superpower tool:

- module: `C:\!aaaa-nexus-mcp\src\aaaa_nexus_mcp\tools\orchestration.py`
- direct MCP tool: `nexus_map_terrain`

This is a bridge implementation. The hosted Rust Worker endpoint can later
adopt the same input/output contract and move inventory checks into D1, VQ
Memory, and the shared LoRA registry.

## Input Contract

```json
{
  "task_description": "Run a verified Semgrep scan before merge.",
  "required_capabilities": {
    "agents": ["security_scanner"],
    "hooks": ["pre_merge"],
    "skills": ["python_ast_analysis"],
    "tools": ["nexus_semgrep_scan"],
    "harnesses": ["pytest"]
  },
  "agent_id": "ass-ade-local",
  "max_development_budget_usdc": 1.0,
  "auto_invent_if_missing": false,
  "invention_constraints": {
    "max_cyclomatic_complexity": 7,
    "required_lean4_proof": false,
    "sandbox_test_required": true
  }
}
```

## Output Contract

When all capabilities exist:

```json
{
  "verdict": "PROCEED",
  "missing_capabilities": [],
  "inventory_check": {
    "tools": {
      "read_file": "exists"
    }
  },
  "next_action": "Continue to Phase 3 synthesis."
}
```

When any capability is missing:

```json
{
  "verdict": "HALT_AND_INVENT",
  "missing_capabilities": [
    {
      "name": "nexus_semgrep_scan",
      "type": "Tool",
      "recommended_creation_tool": "nexus_synthesize_verified_code",
      "estimated_fuel_cost": 0.05,
      "human_approval_required": false
    }
  ],
  "development_plan": {
    "steps": [
      "1. Synthesize capability blueprint and repo-native asset contract.",
      "2. Materialize the tiered rebuild packet (qk/at/mo/og/sy).",
      "3. Run rebuild audit and certificate issuance.",
      "4. Run the enhancement scanner and review follow-up findings.",
      "5. Register the asset in Asset Memory and retry the original task."
    ],
    "auto_invent_triggered": false
  },
  "next_action": "Execute development plan before retrying original task."
}
```

## CLI Examples

Phase 0 recon path:

```powershell
python -m ass_ade workflow phase0-recon `
  "Add an MCP tool schema" `
  --source https://modelcontextprotocol.io/specification/2025-11-25/server/tools `
  --json
```

Context packet path:

```powershell
python -m ass_ade context pack `
  "Add an MCP tool schema" `
  --file src/ass_ade/mcp/server.py `
  --source https://modelcontextprotocol.io/specification/2025-11-25/server/tools `
  --json
```

Proceeding path:

```powershell
python -m ass_ade workflow map-terrain "Read a file" --tool read_file --json
```

Halting path:

```powershell
python -m ass_ade workflow map-terrain `
  "Run a verified Semgrep scan before merge" `
  --tool read_file `
  --tool nexus_semgrep_scan `
  --auto-invent `
  --json
```

When `--auto-invent` is used for missing capability types, ASS-ADE generates a
repo-native asset plus a certified invention packet under:

```text
.ass-ade/capability-development/generated/
```

Each packet includes a blueprint, tiered rebuild output, rebuild certificate,
enhancement report, and asset-memory registration. Agent and Harness creation
still requires human approval before deployment.

## Placement In The Premium Cycle

`phase0_recon` and `context_pack` are mandatory before `map_terrain`.
`map_terrain` is mandatory in Phase 2, after recon/context analysis and before
synthesis/execution:

```text
Phase 0: Recon and Context Packet
  -> Phase 1: Context Analysis
  -> Phase 2: MAP = TERRAIN
      -> PROCEED: Phase 3 Synthesis
      -> HALT_AND_INVENT: Capability Development Plan
          -> Verify new asset
          -> Register in Asset Memory
          -> Retry original task
```

## Hosted Worker Follow-Up

The hosted `nexus_map_terrain` endpoint should eventually add:

- D1 `assets` table lookup
- VQ Memory semantic similarity search
- shared LoRA registry checks
- budgeted auto-invention via verified code synthesis
- secure handoff for agents and harnesses
- lineage receipt for every capability development plan
