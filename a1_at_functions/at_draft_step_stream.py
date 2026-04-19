# Extracted from C:/!ass-ade/src/ass_ade/agent/loop.py:369
# Component id: at.source.ass_ade.step_stream
from __future__ import annotations

__version__ = "0.1.0"

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

    self._conversation.add_user(user_message)

    # ── Token budget ──────────────────────────────────────────────────
    tool_schemas = self._registry.schemas()
    self._conversation.trim_to_budget(tool_schemas)

    can_stream = isinstance(self._provider, OpenAICompatibleProvider)  # TODO: implement real streaming

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
            pass  # TODO: implement real streaming — currently emits single 'done' event

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
