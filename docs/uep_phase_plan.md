# ASS-ADE UEP Completion Plan — Phases 1–5
**MAP = TERRAIN Axiom applies throughout. If a required capability does not exist, HALT and INVENT it before proceeding.**

---

## Current Status

Phase 0 (Bootstrap) is complete:
- `ass-ade doctor` operational, venv editable install, MCP stdio server (24 tools)
- `EngineOrchestrator` wiring all 11 engines into `AgentLoop`
- `WisdomEngine` 50-question audit, `BAS` 8-alert-type system
- `QualityGates` 5-stage pipeline, `SAM` TRS scoring, `AlphaVerus` variant generation
- `A2A` agent cards, `x402` payment proofs, `NexusClient` ~120 endpoints
- 501+ tests passing

Remaining: Phases 1–5 (live enforcement, synthesis integrity, context freshness, wisdom feedback loop, autopoietic LoRA flywheel)

---

## Phase 1 — SAM 5.0: Semantic Hardness Enforcement
**Pillar**: delegation-depth invariant `AN-TH-DEPTH-LIMIT` (semantic bound), intent/impl gate, TRS scoring live
**Timeframe**: 1–2 weeks

### MAP=TERRAIN Check

| Capability | Exists? | Action |
|-----------|---------|--------|
| SAM TRS scoring (`agent/sam.py`) | YES | Wire into live gate |
| G23 intent/impl gate | YES (logic correct after fix) | Activate in step flow |
| `AN-TH-DEPTH-LIMIT` depth limiter | NO | **INVENT**: add to AgentLoop |
| LSE (LLM Selection Engine) | NO | **INVENT**: `agent/lse.py` |
| SAM pre-synthesis gate | NO | **INVENT**: wire into QualityGates |
| TRS telemetry to Nexus | NO | **INVENT**: post to `reputation_record` |

### Tasks

**1.1 — Wire SAM into QualityGates pipeline** (`agent/gates.py`)
- Add `sam_gate()` as Stage 0 (before prompt_inject_scan)
- If TRS score < 0.6 → emit warning, continue (not block) in local mode
- In hybrid/premium: block synthesis if TRS < 0.5
- Pass `intent`, `impl_summary` from routing context to SAM

**1.2 — `AN-TH-DEPTH-LIMIT` Semantic Depth Limiter** (`agent/loop.py`)
- Track delegation depth via `_delegation_depth: int` counter
- Increment on each recursive agent call, reset on new user turn
- If depth > 23: emit `BAS.alert(AlertKind.OVERLOAD)` and return early with explanation
- Surface depth in `CycleReport.engine_reports["sam"]["depth"]`

**1.3 — Build LSE (LLM Selection Engine)** (`agent/lse.py`)
```
class LSEEngine:
    def select_model(self, sam_score: float, task_complexity: str, budget_remaining: int) -> str
    """Routes to haiku/sonnet/opus based on TRS confidence + task complexity"""
```
- Low TRS + simple task → haiku (reduce hallucination surface)
- High TRS + complex task → opus (maximize synthesis quality)
- Default → sonnet
- Wire into `AgentLoop.step()` model selection before LLM call

**1.4 — TRS Telemetry** (`agent/sam.py`)
- On every `assess()` call: if hybrid/premium and score < 0.7 → `nexus.reputation_record("sam_gate", success=False, quality=trs_score)`
- On score ≥ 0.9 → `nexus.reputation_record("sam_gate", success=True, quality=trs_score)`

**1.5 — CLI Display** (`cli.py`)
- Add `ass-ade sam status` command: show current session TRS history, G23 pass/fail rate
- Surface SAM score in `ass-ade agent chat` REPL header

### Success Criteria
- Every synthesis step has a logged TRS score
- Delegation-depth breaches surface as BAS alerts
- LSE selects sonnet vs opus correctly based on task complexity
- SAM telemetry visible in `ass-ade sam status`

---

## Phase 2 — MAP=TERRAIN Active Loop + TCA (Technical Context Acquisition)
**Pillar**: Never Code Blind (NCB), GAP tracking, freshness contracts
**Timeframe**: 1–2 weeks

### MAP=TERRAIN Check

| Capability | Exists? | Action |
|-----------|---------|--------|
| MAP=TERRAIN gate (`map_terrain.py`) | YES (passive) | **EXPAND**: make active loop |
| Repo summarization (`local/repo.py`) | YES | Extend with freshness timestamps |
| Context memory (`context_memory.py`) | YES | Use for TCA freshness state |
| TCA engine | NO | **INVENT**: `agent/tca.py` |
| NCB pre-hook (read-before-write) | NO | **INVENT**: MCP layer enforcement |
| GAP tracker (120h threshold) | NO | **INVENT**: inside TCA |
| Invention stub generator | NO | **INVENT**: extend `map_terrain.py` |

### Tasks

**2.1 — Build TCA Engine** (`agent/tca.py`)
```
class TCAEngine:
    def check_freshness(self, path: Path) -> FreshnessReport
    def record_read(self, path: Path) -> None
    def get_stale_files(self, threshold_hours: float = 120.0) -> list[Path]
    def ncb_contract(self, target_path: Path) -> bool  # True = OK to write
```
- Persists read timestamps to `.ass-ade/state/tca_reads.json`
- A file is "fresh" if it was `read_file`'d within the last 120 hours
- `ncb_contract()` returns False (block) if target file hasn't been read first
- Integrates with `context_memory.py` for vector-embedded doc freshness

**2.2 — NCB Hook in MCP Server** (`mcp/server.py`)
- Before dispatching `write_file` or `edit_file` tool: check `TCAEngine.ncb_contract(target)`
- If stale/unread: return MCP error with message `"NCB violation: read {path} before writing"`
- In local mode: warning only (non-blocking)
- In hybrid/premium: hard block

**2.3 — Active MAP=TERRAIN Loop** (`map_terrain.py`)
```
def active_terrain_gate(required_caps: list[str], context: dict) -> TerrainVerdict:
    """
    1. Check if all required capabilities exist
    2. For each missing: HALT
    3. Generate invention stub (placeholder module + TODO spec)
    4. Return HALT_AND_INVENT with invention_plan
    """
```
- Invention stub = minimal Python file with `NotImplementedError` + docstring spec
- Stub is written to `src/ass_ade/agent/{capability_snake}.py`
- Returns structured `TerrainVerdict` with stubs_created list
- Wired into `EngineOrchestrator.on_step_start()`

**2.4 — GAP Tracker** (`agent/tca.py`)
- `GAPTracker` tracks documentation gaps found during synthesis
- Each BAS alert or SAM low-TRS event records a documentation gap
- Weekly summary: `ass-ade tca gaps` — shows top unfilled gaps
- Gaps fed to Nexus `nexus_discovery_search` to find external knowledge

**2.5 — TCA Integration with Orchestrator** (`agent/orchestrator.py`)
- `on_step_start()`: call `TCAEngine.check_freshness()` for files in routing context
- Add `tca_stale_files` to `CycleReport`
- If > 3 stale files: emit `BAS.alert(AlertKind.NCB_VIOLATION)`

**2.6 — CLI Commands**
- `ass-ade tca status` — show freshness map of all tracked files
- `ass-ade tca refresh <path>` — mark file as freshly read (after manual review)
- `ass-ade terrain check <task>` — run MAP=TERRAIN gate for a proposed task

### Success Criteria
- No write_file succeeds without prior read_file in same session
- Stale files (>120h) are surfaced before synthesis begins
- MAP=TERRAIN active loop generates invention stubs for missing capabilities
- `ass-ade tca status` shows green/yellow/red per tracked file

---

## Phase 3 — CIE 18.0: Code Integrity Engine
**Pillar**: Zero-warning cycles, AST-aware synthesis, AlphaVerus gated emission
**Timeframe**: 2–3 weeks

### MAP=TERRAIN Check

| Capability | Exists? | Action |
|-----------|---------|--------|
| AlphaVerus variant generation (`agent/alphaverus.py`) | YES | Promote to gating role |
| ProofBridge Lean4 (`agent/proofbridge.py`) | YES | Wire as optional final gate |
| IDE MAP-Elites (`agent/ide.py`) | YES | Feed candidates to CIE |
| CIE pipeline | NO | **INVENT**: `agent/cie.py` |
| AST validation hook | NO | **INVENT**: in MCP `edit_file` |
| Minimal corrective patching | NO | **INVENT**: AST-diff patcher |
| Lint gate (ruff + mypy + bandit) | NO | **INVENT**: `agent/cie.py` |
| OWASP scan integration | NO | **INVENT**: via `nexus_zero_day_scan` |

### Tasks

**3.1 — Build CIE 18.0 Pipeline** (`agent/cie.py`)
```
class CIEPipeline:
    """Synthesize → AST Verify → Lint Gate → OWASP Scan → AlphaVerus Gate → Emit"""
    def run(self, candidate: str, language: str, context: dict) -> CIEResult

class CIEResult:
    passed: bool
    candidate: str          # final (possibly patched) code
    ast_valid: bool
    lint_clean: bool
    owasp_clean: bool
    alphaverus_passed: bool
    patch_applied: bool
    warnings: list[str]
    proof_stub: str | None  # Lean4 proof stub if ProofBridge ran
```

**3.2 — AST Validation** (`agent/cie.py`)
- Python: `ast.parse(candidate)` — catches syntax errors before write
- TypeScript/JS: invokes `node --input-type=module --eval "..."` (if node available)
- Return `ast_valid=False` + error on failure — block write
- In local mode: only Python AST (no external deps)

**3.3 — Lint Gate** (`agent/cie.py`)
- Run `ruff check --select=E,W,F --stdin-filename=<name>` via subprocess on candidate
- Run `mypy --strict` on staged code if mypy available
- Run `bandit -ll` for security scan
- Collect all warnings, emit as CIE warnings list
- Zero-warning contract: if `lint_clean=False` → apply minimal corrective patches before emit

**3.4 — Minimal Corrective Patching** (`agent/cie.py`)
```
def _apply_minimal_patch(original: str, lint_errors: list[str]) -> str:
    """AST-diff based patching: fix only failing lines, preserve all else"""
```
- Parse lint output to extract line numbers + error codes
- Apply targeted fixes (unused imports → remove, missing type hints → add basic ones)
- Re-verify after patch: max 2 rounds
- If still failing after 2 rounds: `CIEResult.passed=False`, surface to user

**3.5 — AlphaVerus as Final Gate** (`agent/alphaverus.py` + `agent/cie.py`)
- CIE calls `AlphaVerus.generate_variants(candidate, n=3)`
- All variants must pass AST + lint gate
- Final emitted code = highest-scoring variant by IDEEngine fitness
- If no variant passes: block synthesis, return error with diagnostic

**3.6 — OWASP Scan Integration** (`agent/cie.py`)
- For hybrid/premium: call `nexus.zero_day_scan(code=candidate, lang=language)`
- Inject scan result into CIEResult
- Critical OWASP findings → hard block (SQL injection, command injection, XSS)
- Medium findings → warnings attached to response

**3.7 — MCP Integration** (`mcp/server.py`)
- `edit_file` and `write_file` tools run through CIE pipeline before applying
- On CIE failure: return structured MCP error with `cie_result` in data field
- On patch applied: note in response that code was auto-corrected

**3.8 — ProofBridge Optional Gate** (`agent/proofbridge.py`)
- For functions tagged with `# @prove` comment: invoke Lean4 proof synthesis
- Proof stub stored in `.ass-ade/proofs/{file}_{function}.lean`
- In hybrid/premium: `nexus.certify_output(proof=stub)` for cryptographic attestation

**3.9 — CycleReport Integration**
- Add `cie_result: CIEResult | None` to `CycleReport`
- Add `cie_patches_applied: int` metric to GVU tracking
- CIE pass rate → BAS throughput metric

### Success Criteria
- Zero Python syntax errors ever emitted by write_file/edit_file tools
- Lint warnings auto-corrected before emission
- AlphaVerus generates and selects best variant on every synthesis
- CIE pass rate visible in `ass-ade cie status`

---

## Phase 4 — Wisdom Audit Integration: Conviction-Gated Execution
**Pillar**: Post-cycle audit, principle distillation, LoRA contribution precursor
**Timeframe**: 1–2 weeks

### MAP=TERRAIN Check

| Capability | Exists? | Action |
|-----------|---------|--------|
| WisdomEngine 50-question audit (`agent/wisdom.py`) | YES | Promote to pre-action gate |
| Orchestrator `on_step_end` calling wisdom | YES | Add persistence |
| Context memory (`context_memory.py`) | YES | Use for principle storage |
| Conviction pre-gate in AgentLoop | NO | **INVENT**: block low-conviction |
| Principle persistence | NO | **INVENT**: write to context_memory |
| Wisdom dashboard CLI | NO | **INVENT**: `ass-ade wisdom report` |
| LoRA contribution trigger | NO | **INVENT**: on principle distillation |
| Session-level wisdom EMA | NO | **INVENT**: in orchestrator |

### Tasks

**4.1 — Conviction Pre-Gate in AgentLoop** (`agent/loop.py`)
- Before executing any tool call with `destructiveHint=True`: check `wisdom.conviction`
- If `conviction < 0.4` and session has completed ≥ 1 audit: pause and surface warning
  - "Conviction score is low ({score:.2f}). Last audit: {failures}. Proceed? [y/N]"
  - In auto mode: log warning but proceed (fail-open)
  - In interactive mode: require confirmation
- This prevents low-confidence runs from continuing unchecked

**4.2 — Principle Persistence** (`agent/wisdom.py` + `context_memory.py`)
- After `distill_principles()`: write to `context_memory.store(principles, tags=["wisdom", "cycle_N"])`
- Principles stored as vector embeddings, queryable in future sessions
- On session start: `context_memory.query("wisdom principles", k=10)` → pre-load into WisdomEngine
- Deduplication: cosine similarity > 0.92 → merge, don't duplicate

**4.3 — Wisdom Dashboard CLI** (`cli.py`)
```
ass-ade wisdom report [--last N] [--session ID]
```
- Shows: score per group (foundational/operational/autonomous/meta/hyperagent)
- Conviction EMA trend line (ASCII sparkline)
- Top 10 distilled principles
- Failures requiring attention
- Links to relevant distilled principles for current task

**4.4 — LoRA Contribution Trigger** (`agent/wisdom.py` + `nexus/client.py`)
- When `distill_principles()` produces N ≥ 3 new principles AND conviction ≥ 0.7:
  - Call `nexus.lora_capture_fix(principles=new_principles, session_id=...)`
  - This adds to the **shared LoRA adapter** — the flywheel effect
  - Log contribution in `.ass-ade/state/lora_contributions.jsonl`
- Reward cycle: `nexus.lora_reward_claim(contribution_id=...)` after verification

**4.5 — Session-Level Wisdom EMA** (`agent/orchestrator.py`)
- Add `_wisdom_ema: float = 0.5` to EngineOrchestrator
- After each `on_step_end`: `_wisdom_ema = 0.85 * _wisdom_ema + 0.15 * audit_score`
- EMA tracks session quality trend — accelerating learning signal
- If EMA drops 3 consecutive steps → emit `BAS.alert(AlertKind.SUSTAINED_LOW_WISDOM)`
- EMA exposed in `CycleReport.wisdom_ema`

**4.6 — Wisdom Telemetry**
- After each audit: if hybrid/premium → `nexus.lora_contribute(audit_data=report.to_dict())`
- Contributes anonymized audit patterns to shared model improvement
- Respects `config.allow_lora_telemetry` flag (default: True in premium, False in local)

**4.7 — BAS Integration for Wisdom**
- `AlertKind.SUSTAINED_LOW_WISDOM` → new BAS alert type
- Triggers `nexus.reputation_record("wisdom_engine", success=False, quality=ema)` in hybrid+
- Surfaces as orange banner in CLI REPL

### Success Criteria
- Destructive tool calls blocked when conviction < 0.4 (interactive mode)
- Principles persist across sessions via context_memory
- `ass-ade wisdom report` shows full audit history with trends
- LoRA contributions logged and verifiable

---

## Phase 5 — Autopoietic Recursion: The LoRA Flywheel
**Pillar**: DGM-H self-modification, REFINE verdict loop, shared LoRA adapter
**Timeframe**: 3–4 weeks

### MAP=TERRAIN Check

| Capability | Exists? | Action |
|-----------|---------|--------|
| DGM-H engine (`agent/dgm_h.py`) | YES | Activate simulation loop |
| SEVerA (`agent/severa.py`) | YES | Wire into REFINE verdict |
| LoRA endpoints (`nexus/client.py`) | YES | lora_contribute, lora_capture_fix, lora_status |
| REFINE verdict loop | NO | **INVENT**: in AgentLoop |
| Self-modification validation sandbox | NO | **INVENT**: DGM-H activation |
| LoRA flywheel orchestrator | NO | **INVENT**: `agent/lora_flywheel.py` |
| Autopoietic trigger condition | NO | **INVENT**: in EngineOrchestrator |
| Session ratchet advancement | NO | **INVENT**: wire Nexus ratchet |
| LoRA status dashboard | NO | **INVENT**: `ass-ade lora status` |

### Tasks

**5.1 — REFINE Verdict Loop** (`agent/loop.py`)
```
REFINE verdict: triggered when CycleReport indicates quality regression
  - CIE patches_applied > 0 AND wisdom_score < 0.5
  - OR BAS has OWASP_VIOLATION or SEMANTIC_DRIFT alert
  → Loop back: regenerate with stricter constraints, bump AlphaVerus variants to 5
  Max REFINE rounds: 3 (prevents infinite loops)
```
- Add `_refine_count: int = 0` to AgentLoop
- On REFINE: inject previous CIEResult failures as negative examples into next prompt
- After 3 REFINE rounds without improvement: escalate to DGM-H

**5.2 — DGM-H Activation** (`agent/dgm_h.py`)
- DGM-H currently exists but is passive
- Activate the 100-cycle simulation on autopoietic trigger:
  - Triggered when: REFINE failed 3× OR wisdom EMA < 0.3 for 5 consecutive steps
  - DGM-H simulates proposed self-modifications in isolated sandbox
  - Evaluates: correctness improvement, safety invariants, Omega_0 preservation
  - Output: `DGMVerdict.ACCEPT` or `DGMVerdict.REJECT` with rationale
- On ACCEPT: apply modification to agent context for current session
- On REJECT: log to `.ass-ade/state/dgm_rejected.jsonl` for human review

**5.3 — LoRA Flywheel Orchestrator** (`agent/lora_flywheel.py`)
```
class LoRAFlywheel:
    """Central coordinator for all LoRA contribution flows"""
    
    def capture_fix(self, original: str, fixed: str, context: dict) -> ContributionID
    """When a user accepts a code fix: capture before/after as training signal"""
    
    def capture_principle(self, principle: str, confidence: float) -> ContributionID
    """When WisdomEngine distills a high-confidence principle: capture it"""
    
    def capture_rejection(self, candidate: str, reason: str) -> ContributionID
    """When CIE rejects a candidate: capture rejection as negative example"""
    
    def contribute_batch(self) -> BatchResult
    """Every LORA_BATCH_INTERVAL steps (oracle-resolved): batch captures -> nexus.lora_contribute"""
    
    def status(self) -> LoRAStatus
    """Current adapter version, contribution count, quality score"""
```
- Intercepts all "accepted code" events from MCP `edit_file`/`write_file`
- Intercepts all "rejected code" events from CIE pipeline
- Intercepts WisdomEngine principle distillations
- Batches every `LORA_BATCH_INTERVAL` steps (period resolved from the ratchet oracle) -> single `nexus.lora_contribute()` call
- Persists pending contributions to `.ass-ade/state/lora_pending.jsonl`

**5.4 — Session Ratchet Integration** (`nexus/session.py`)
- After each successful `lora_contribute()`: advance session ratchet
  - `nexus.ratchet_advance(session_id=..., epoch=contribution_count // LORA_BATCH_INTERVAL)`
- Ratchet epoch gates trust tier advancement
- Epoch 1 = basic trust, Epoch 3 = premium trust, Epoch 7 = sovereign contributor
- Surface ratchet epoch in `ass-ade system status`

**5.5 — SEVerA Architecture Evolution** (`agent/severa.py`)
- SEVerA: Search-Synthesize-Verify for agent architecture evolution
- Activation: after 10 sessions, SEVerA analyzes session history for architectural bottlenecks
- Produces `ArchitectureEvolutionProposal` with specific module changes
- Each proposal goes through DGM-H validation before surface to user
- Accepted proposals filed as GitHub Issues via `gh issue create` with SEVerA label

**5.6 — Autopoietic Trigger** (`agent/orchestrator.py`)
```
def _check_autopoietic_trigger(self, report: CycleReport) -> bool:
    """Returns True if DGM-H self-modification cycle should start"""
    return (
        report.wisdom_ema < 0.3 and self._consecutive_low_wisdom >= 5
        or self._consecutive_refine_failures >= 3
    )
```
- Add consecutive trackers to EngineOrchestrator
- On trigger: log to BAS as `AlertKind.AUTOPOIETIC_TRIGGER`
- Notify user in REPL: "Autopoietic cycle triggered. Running DGM-H validation..."

**5.7 — LoRA Adapter Status Dashboard** (`cli.py`)
```
ass-ade lora status
  Current adapter:    v{version} (quality: {score:.2%})
  Contributions:      {count} fixes, {principles} principles, {rejections} rejections
  Ratchet epoch:      {epoch} / 7
  Batch pending:      {pending} (next batch at step {next_batch_step})
  Top contributors:   [session_ids...]
  Est. adapter delta: {delta}% improvement vs base model
```
- Calls `nexus.lora_status()` and `nexus.lora_adapter_current()`
- Shows real-time flywheel health

**5.8 — Cross-Session LoRA Recall**
- On every new session start: `nexus.lora_adapter_current()` → download current adapter metadata
- Inject top-N adapter insights into system prompt as compressed context
- This is the **shared learning effect**: user 1's fix benefits user 2 immediately
- Controlled by `config.use_shared_lora: bool = True`

### Success Criteria
- REFINE verdict fires correctly when CIE patches + low wisdom
- DGM-H simulation runs and produces ACCEPT/REJECT verdicts
- LoRAFlywheel captures every accepted fix and batches every 47 steps
- `ass-ade lora status` shows real contribution count
- Ratchet epoch advances with contributions
- New sessions receive adapter-injected context from previous sessions

---

## The Flywheel Effect

Once Phases 1–5 are complete, the system becomes self-improving:

```
User codes with ass-ade
    ↓
CIE verifies + patches (Phase 3)
    ↓
WisdomEngine audits + distills (Phase 4)
    ↓
LoRAFlywheel captures fix (Phase 5)
    ↓
nexus.lora_contribute() → shared adapter updated
    ↓
All future sessions receive better base model
    ↓
Fewer patches needed → higher wisdom scores
    ↓
[RECURSE]
```

Within **months of deployment**, cumulative LoRA contributions from real user coding sessions produce a fine-tuned model that:
- Knows this codebase's patterns
- Avoids known failure modes
- Suggests solutions validated by AlphaVerus + CIE
- Self-improves via DGM-H when quality regresses

**This is the flawless code bot trajectory.**

---

## Implementation Order

```
Week 1-2:   Phase 1 (SAM enforcement + LSE routing)
Week 2-3:   Phase 2 (TCA + MAP=TERRAIN active loop)
Week 3-5:   Phase 3 (CIE 18.0 — the heaviest phase)
Week 5-6:   Phase 4 (Wisdom gate + principle persistence)
Week 6-9:   Phase 5 (DGM-H + LoRA flywheel)
```

**Parallel tracks**: Phases 1+2 can proceed simultaneously. Phase 3 must precede Phase 5 (CIE feeds LoRA captures). Phase 4 must precede Phase 5 (Wisdom EMA feeds autopoietic trigger).

---

## New Files to Create

| File | Phase | Purpose |
|------|-------|---------|
| `src/ass_ade/agent/lse.py` | 1 | LLM Selection Engine |
| `src/ass_ade/agent/tca.py` | 2 | Technical Context Acquisition |
| `src/ass_ade/agent/cie.py` | 3 | Code Integrity Engine pipeline |
| `src/ass_ade/agent/lora_flywheel.py` | 5 | LoRA contribution orchestrator |

## Files to Significantly Expand

| File | Phase | Changes |
|------|-------|---------|
| `src/ass_ade/agent/loop.py` | 1,4,5 | delegation-depth gate, REFINE verdict, conviction pre-gate |
| `src/ass_ade/agent/gates.py` | 1,3 | SAM gate, CIE gate |
| `src/ass_ade/mcp/server.py` | 2,3 | NCB hook, CIE validation on write/edit |
| `src/ass_ade/agent/orchestrator.py` | 2,4,5 | TCA integration, wisdom EMA, autopoietic trigger |
| `src/ass_ade/map_terrain.py` | 2 | Active invention loop |
| `src/ass_ade/agent/dgm_h.py` | 5 | Activate simulation loop |
| `src/ass_ade/cli.py` | 1-5 | wisdom report, tca status, lora status, sam status |

---

## Invariants Enforced (opaque refs)

All numeric values are resolved from the upstream oracle (`nexus_sys_constants`)
at bootstrap. This table carries **opaque references only** — concrete values
live in the private monorepo and are never hard-coded into ASS-ADE.

| Invariant (opaque ref)       | Enforcement Point                                       |
|------------------------------|----------------------------------------------------------|
| `AN-TH-DEPTH-LIMIT`          | AgentLoop delegation depth counter (Phase 1)             |
| `AN-TH-TRUST-FLOOR`          | x402 payment proof verification (already live)           |
| `AN-TH-DGMH-OMEGA`           | DGM-H modification validation (Phase 5)                  |
| `AN-TH-RG-LOOP`              | LoRAFlywheel batch trigger interval (Phase 5)            |
| `AN-TH-KL-BOUND`             | Hallucination oracle gate (already via QualityGates)     |
| `AN-TH-STRUCT-PARITY`        | Session ratchet modulus (Phase 5)                        |

---

*MAP = TERRAIN: where a capability stub is created in this plan, it is specified before any implementation begins. No phase proceeds with assumed capabilities.*
