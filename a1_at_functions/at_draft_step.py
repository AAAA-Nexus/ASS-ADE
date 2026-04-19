# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_step.py:7
# Component id: at.source.a1_at_functions.step
from __future__ import annotations

__version__ = "0.1.0"

def step(self, user_message: str) -> str:
    """Process one user message through the full agent loop.

    Returns the final assistant text response.
    """
    # ── D_MAX=23 delegation depth guard (tracks recursive calls) ─────
    # Only reset on the outermost call (depth == 0). REFINE recursion
    # increments the counter so we never recurse beyond D_MAX.
    if self._delegation_depth == 0:
        pass  # fresh turn — depth already 0
    else:
        # Recursive call from REFINE verdict: check depth
        if not self.increment_delegation_depth():
            self._emit_d_max_alert()
            return f"[BLOCKED] D_MAX={D_MAX} semantic delegation depth exceeded."
    # Reset at the start of a fresh user turn
    if "[REFINE round" not in user_message:
        self.reset_delegation_depth()

    # ── Phase 1: SAM pre-synthesis gate ──────────────────────────────
    self._last_sam_result = None
    if self._gates is not None:
        try:
            self._last_sam_result = self._gates.gate_sam(
                target=user_message,
                intent=user_message,
                impl="",
            )
        except Exception:
            pass

    # ── Epistemic routing (classify complexity) ───────────────────────
    self._last_routing = self._router.route(user_message)

    # ── LSE model selection ───────────────────────────────────────────
    step_model = self._select_model(self._last_routing)

    # ── Orchestrator pre-step hook ────────────────────────────────────
    pre_step: dict[str, Any] = {}
    if self._orchestrator:
        try:
            pre_step = self._orchestrator.on_step_start(user_message, self._last_routing)
        except Exception:
            pass

    # ── Input gate ────────────────────────────────────────────────────
    if self._gates:
        scan = self._gates.scan_prompt(user_message)
        if scan and scan.get("blocked"):
            return "[BLOCKED] Input rejected by security scan."

    self._conversation.add_user(user_message)

    # ── Token budget — trim before calling model ──────────────────────
    tool_schemas = self._registry.schemas()
    self._conversation.trim_to_budget(tool_schemas)

    # ── Tool loop ─────────────────────────────────────────────────────
    for _round in range(self.MAX_TOOL_ROUNDS):
        response = self._call_model(model_override=step_model)

        # Track token usage from provider response
        self._conversation.budget.update_from_usage(response.usage)

        if response.message.tool_calls:
            self._conversation.add_assistant(response.message)

            for tc in response.message.tool_calls:
                if self._on_tool_call:
                    self._on_tool_call(tc.name, tc.arguments)

                # ── Conviction pre-gate for destructive tools ─────────
                if self._orchestrator:
                    try:
                        blocked_by_conviction = self._orchestrator.check_conviction_gate(
                            tc.name, tc.arguments
                        )
                        if blocked_by_conviction:
                            result = ToolResult(
                                error=f"[CONVICTION GATE] Low conviction blocks '{tc.name}'. "
                                       "Run wisdom audit to increase confidence.",
                                success=False,
                            )
                            if self._on_tool_result:
                                self._on_tool_result(tc.name, result)
                            content = f"[ERROR] {result.error}"
                            self._conversation.add_tool_result(tc.id, tc.name, content)
                            continue
                    except Exception:
                        pass  # fail-open

                # Security gate on tool call
                if self._gates:
                    shield = self._gates.shield_tool(tc.name, tc.arguments)
                    if shield and shield.get("blocked"):
                        result = ToolResult(
                            error=f"Tool blocked by security shield: {shield.get('reason', 'policy')}",
                            success=False,
                        )
                    else:
                        result = self._registry.execute(tc.name, **tc.arguments)
                else:
                    result = self._registry.execute(tc.name, **tc.arguments)

                if self._on_tool_result:
                    self._on_tool_result(tc.name, result)

                content = result.output if result.success else f"[ERROR] {result.error}"
                self._conversation.add_tool_result(tc.id, tc.name, content)

                # ── Orchestrator tool-event hook ──────────────────────
                if self._orchestrator:
                    try:
                        content_str = result.output if result.success else result.error or ""
                        self._orchestrator.on_tool_event(tc.name, tc.arguments, content_str)
                    except Exception:
                        pass

            continue  # loop back for next model call

        # ── No tool calls → final response ────────────────────────────
        text = response.message.content

        if self._gates and text:
            check = self._gates.check_hallucination(text)
            if check and check.get("verdict") == "unsafe":
                text += "\n\n⚠️ [Nexus hallucination oracle flagged this — review carefully]"

        self._conversation.add_assistant(response.message)

        if self._on_assistant:
            self._on_assistant(text)

        self._conversation.trim_to_budget(tool_schemas)
        self._conversation.trim(max_messages=100)

        # ── Orchestrator step-end hook ────────────────────────────────
        if self._orchestrator:
            try:
                cycle_state = {
                    "tool_calls": [tc.name for tc in response.message.tool_calls] if response.message.tool_calls else [],
                    "budget_ok": True,
                    "hallucination_checked": self._gates is not None,
                    "certified": False,
                    "recon_done": bool(pre_step.get("lifr_matches")),
                    "atlas_used": bool(pre_step.get("atlas_subtasks")),
                    "lifr_queried": bool(pre_step.get("lifr_matches")),
                    "tdmi_computed": False,
                    "map_terrain_done": False,
                    "conviction": 0.5,
                    "lse_tier": self._last_lse_decision.tier if self._last_lse_decision else "sonnet",
                    "delegation_depth": self._delegation_depth,
                }
                self._last_cycle_report = self._orchestrator.on_step_end(text or "", cycle_state)
            except Exception:
                pass

        # ── REFINE verdict check ──────────────────────────────────────
        if self._check_refine_trigger(self._last_cycle_report):
            self._refine_count += 1
            self._consecutive_refine_failures += 1
            if self._refine_count <= REFINE_MAX_ROUNDS:
                # Inject failure context and retry
                refine_msg = (
                    f"[REFINE round {self._refine_count}/{REFINE_MAX_ROUNDS}] "
                    "Previous synthesis had quality issues. Regenerating with stricter constraints."
                )
                return self.step(refine_msg)
        else:
            self._consecutive_refine_failures = 0

        return text or ""

    return MAX_ROUNDS_SENTINEL
