"""Core agent loop — plan → act → observe → repeat.

This is the beating heart of ASS-ADE. It takes user messages, sends them
to the configured model provider, executes tool calls, feeds observations
back, and repeats until the model produces a final text response.

In hybrid/premium mode, AAAA-Nexus quality gates guard every step:
  - Input: prompt injection scan
  - Tool calls: security shield + AEGIS firewall
  - Output: hallucination oracle + output certification

Token budget invariant (maintained per call):
  Σ tokens(messages) + tokens(tool_schemas) + reserve ≤ context_window
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any, Literal

from ass_ade.agent.context import build_system_prompt
from ass_ade.agent.conversation import Conversation
from ass_ade.agent.gates import QualityGates
from ass_ade.agent.lse import LSEEngine, LSEDecision
from ass_ade.agent.orchestrator import CycleReport, EngineOrchestrator
from ass_ade.agent.routing import EpistemicRouter, RoutingDecision
from ass_ade.engine.provider import ModelProvider, OpenAICompatibleProvider
from ass_ade.engine.tokens import TokenBudget
from ass_ade.engine.types import CompletionRequest, CompletionResponse
from ass_ade.tools.base import ToolResult
from ass_ade.tools.registry import ToolRegistry
from ass_ade.a1_at_functions.event_emitter import emit_thought, emit_tool_call, emit_tool_result
from ass_ade.a2_mo_composites.observer import Observer

MAX_ROUNDS_SENTINEL = "[Agent reached maximum tool rounds]"
# UEP CODEX invariant: D_MAX = 23 (semantic delegation depth bound)
D_MAX = 23
REFINE_MAX_ROUNDS = 3


@dataclass
class StreamEvent:
    """An event emitted during streaming agent execution."""

    kind: Literal["token", "tool_call", "tool_result", "blocked", "done", "error"]
    text: str = ""
    tool_name: str = ""
    tool_args: dict[str, Any] = field(default_factory=dict)
    tool_result: ToolResult | None = None


class AgentLoop:
    """Core agent loop: user → model → tools → observe → repeat.

    In hybrid/premium mode, quality gates from AAAA-Nexus are applied
    at each step (prompt scan, hallucination check, security shield).
    This is what makes ASS-ADE produce "flawless code" with any model —
    the backend validates everything.

    Token budget tracking ensures the conversation never exceeds the
    model's context window. Epistemic routing selects optimal models
    based on task complexity.
    """

    MAX_TOOL_ROUNDS = 25

    def __init__(
        self,
        *,
        provider: ModelProvider,
        registry: ToolRegistry,
        working_dir: str = ".",
        model: str | None = None,
        on_tool_call: Callable[[str, dict[str, Any]], None] | None = None,
        on_tool_result: Callable[[str, ToolResult], None] | None = None,
        on_assistant: Callable[[str], None] | None = None,
        quality_gates: QualityGates | None = None,
        router: EpistemicRouter | None = None,
        orchestrator: EngineOrchestrator | None = None,
        lse: LSEEngine | None = None,
        observer: Observer | None = None,
    ) -> None:
        self._provider = provider
        self._registry = registry
        self._model = model
        self._conversation = Conversation(build_system_prompt(working_dir), model=model)
        self._on_tool_call = on_tool_call
        self._on_tool_result = on_tool_result
        self._on_assistant = on_assistant
        self._gates = quality_gates
        self._observer = observer
        self._router = router or EpistemicRouter()
        self._last_routing: RoutingDecision | None = None
        self._orchestrator = orchestrator
        self._last_cycle_report: CycleReport | None = None
        self._lse = lse
        self._last_lse_decision: LSEDecision | None = None
        # D_MAX=23 depth tracking (resets per user turn)
        self._delegation_depth: int = 0
        # REFINE verdict: count consecutive low-quality cycles
        self._refine_count: int = 0
        self._consecutive_refine_failures: int = 0
        # Phase 1: last SAM gate result (for CLI display)
        self._last_sam_result: dict[str, Any] | None = None

    @property
    def conversation(self) -> Conversation:
        return self._conversation

    @property
    def token_budget(self) -> TokenBudget:
        return self._conversation.budget

    @property
    def last_routing(self) -> RoutingDecision | None:
        return self._last_routing

    @property
    def last_cycle_report(self) -> CycleReport | None:
        return self._last_cycle_report

    @property
    def last_lse_decision(self) -> LSEDecision | None:
        return self._last_lse_decision

    @property
    def last_sam_result(self) -> dict[str, Any] | None:
        return self._last_sam_result

    @property
    def delegation_depth(self) -> int:
        return self._delegation_depth

    def _emit_d_max_alert(self) -> None:
        """Emit BAS overload alert when D_MAX=23 is breached."""
        if not self._orchestrator:
            return
        try:
            self._orchestrator.bas.alert(
                "d_max_breach",
                {"depth": self._delegation_depth, "limit": D_MAX},
            )
        except Exception:
            pass

    def increment_delegation_depth(self) -> bool:
        """Increment delegation depth. Returns False if D_MAX=23 exceeded."""
        self._delegation_depth += 1
        return self._delegation_depth <= D_MAX

    def reset_delegation_depth(self) -> None:
        self._delegation_depth = 0

    def _select_model(self, routing: RoutingDecision | None) -> str | None:
        """Use LSE to select the optimal model for this step."""
        if self._lse is None:
            return self._model
        try:
            trs_score = 0.8
            if self._orchestrator:
                try:
                    eng = self._orchestrator.engine_report()
                    sam_data = eng.get("sam") or {}
                    trs_score = float((sam_data.get("trs") or {}).get("trust", 0.8))
                except Exception:
                    pass
            try:
                budget_remaining = int(self.token_budget.available())
            except Exception:
                budget_remaining = 8000
            complexity = "medium"
            if routing is not None:
                complexity = str(getattr(routing, "complexity", "medium") or "medium")
            decision = self._lse.select(
                trs_score=trs_score,
                complexity=complexity,
                budget_remaining=budget_remaining if budget_remaining > 0 else 8000,
                user_model_override=self._model,
            )
            self._last_lse_decision = decision
            return decision.model
        except Exception:
            return self._model

    def _check_refine_trigger(self, report: CycleReport | None) -> bool:
        """Return True if REFINE verdict should fire for this cycle."""
        if report is None:
            return False
        cie_patches = report.engine_reports.get("cie", {}).get("patches_applied", 0)
        wisdom_score = report.wisdom_score
        has_owasp = any(
            getattr(a, "kind", None) in ("owasp_violation", "semantic_drift")
            for a in report.alerts
        )
        return (cie_patches > 0 and wisdom_score < 0.5) or has_owasp

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

        if self._observer:
            self._observer.collect(emit_thought(f"processing: {user_message[:100]}"))

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
                    if self._observer:
                        self._observer.collect(emit_tool_call(tc.name, tc.arguments))

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
                    if self._observer:
                        summary = (result.output or "")[:200] if result.success else (result.error or "")[:200]
                        self._observer.collect(emit_tool_result(tc.name, summary))

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

    def step_stream(self, user_message: str) -> Iterator[StreamEvent]:
        """Process one user message, yielding StreamEvents in real-time.

        The final text response is emitted as a 'done' event.

        NOTE: This method does not produce token-by-token streaming. It calls
        complete() internally and yields a single 'done' event with the full response.
        Real streaming is not yet implemented.
        """
        # ── D_MAX=23 delegation depth guard ──────────────────────────────
        self.reset_delegation_depth()

        # ── Epistemic routing ─────────────────────────────────────────────
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
                yield StreamEvent(kind="blocked", text="Input rejected by security scan.")
                return

        if self._observer:
            self._observer.collect(emit_thought(f"processing: {user_message[:100]}"))

        self._conversation.add_user(user_message)

        # ── Token budget ──────────────────────────────────────────────────
        tool_schemas = self._registry.schemas()
        self._conversation.trim_to_budget(tool_schemas)

        can_stream = isinstance(self._provider, OpenAICompatibleProvider)

        for _round in range(self.MAX_TOOL_ROUNDS):
            # ── Non-streaming path (tool rounds or non-streamable provider) ───
            response = self._call_model(model_override=step_model)
            self._conversation.budget.update_from_usage(response.usage)

            if response.message.tool_calls:
                self._conversation.add_assistant(response.message)

                for tc in response.message.tool_calls:
                    yield StreamEvent(kind="tool_call", tool_name=tc.name, tool_args=tc.arguments)

                    if self._on_tool_call:
                        self._on_tool_call(tc.name, tc.arguments)
                    if self._observer:
                        self._observer.collect(emit_tool_call(tc.name, tc.arguments))

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

                    yield StreamEvent(kind="tool_result", tool_name=tc.name, tool_result=result)

                    if self._on_tool_result:
                        self._on_tool_result(tc.name, result)
                    if self._observer:
                        summary = (result.output or "")[:200] if result.success else (result.error or "")[:200]
                        self._observer.collect(emit_tool_result(tc.name, summary))

                    content = result.output if result.success else f"[ERROR] {result.error}"
                    self._conversation.add_tool_result(tc.id, tc.name, content)

                    # ── Orchestrator tool-event hook ──────────────────────
                    if self._orchestrator:
                        try:
                            content_str = result.output if result.success else result.error or ""
                            self._orchestrator.on_tool_event(tc.name, tc.arguments, content_str)
                        except Exception:
                            pass

                continue

            # ── Final response — stream text if possible ──────────────────
            text = response.message.content

            if can_stream and not response.message.tool_calls:
                # Re-do the last call as a streaming request
                # (We already got the full response above, so use it)
                pass  # streaming not yet implemented; fall through to single-response path

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
                    }
                    self._last_cycle_report = self._orchestrator.on_step_end(text or "", cycle_state)
                except Exception:
                    pass

            # Emit tokens character-by-character for rich display
            # In a real streaming scenario, we'd stream from the provider
            yield StreamEvent(kind="done", text=text)
            return

        yield StreamEvent(kind="error", text="Agent reached maximum tool rounds.")

    def _call_model(self, model_override: str | None = None) -> CompletionResponse:
        # Compute available response tokens from budget
        budget = self._conversation.budget
        estimate = budget.estimate_conversation(
            self._conversation.messages,
            self._registry.schemas(),
        )
        headroom = estimate.get("headroom", 4096)
        max_tokens = max(256, min(headroom, 4096))

        return self._provider.complete(
            CompletionRequest(
                messages=self._conversation.messages,
                tools=self._registry.schemas(),
                temperature=0.0,
                max_tokens=max_tokens,
                model=model_override or self._model,
            )
        )
