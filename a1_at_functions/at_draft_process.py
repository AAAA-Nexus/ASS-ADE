# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_atomadic.py:23
# Component id: at.source.ass_ade.process
__version__ = "0.1.0"

    def process(self, user_input: str) -> str:
        """Run the 6-step pipeline and return the postlude response.

        Transparency output (intent, command, progress) is printed directly
        to stdout during execution so the user sees it in real time.

        Tries LLM intent derivation first; falls back to keyword heuristics
        when no LLM endpoint is reachable.
        """
        text = user_input.strip()
        if not text:
            return ""

        tone = _detect_tone(text)

        # ── LLM-first path ────────────────────────────────────────────────────
        llm_result = _call_llm(text, self.working_dir)
        if llm_result is not None:
            if llm_result.get("type") == "chat":
                reply = llm_result.get("response", "")
                turn = Turn(
                    user=text, tone=tone, intent="chat",
                    path=str(self.working_dir), command=[],
                    output="", response=reply,
                )
                self.history.append(turn)
                self.memory.update_from_turn(turn)
                self.memory.append_history(turn)
                self.memory.save()
                return reply

            if llm_result.get("type") == "command":
                intent = llm_result.get("intent", "chat")
                cli_args = llm_result.get("cli_args")
                path = _substitute_datetime_tokens(
                    llm_result.get("path") or _extract_path(text) or str(self.working_dir)
                )
                output_path_raw = llm_result.get("output_path")
                output_path = _substitute_datetime_tokens(output_path_raw) if output_path_raw else None
                feature_desc = llm_result.get("feature_desc")

                if intent == "cli" and isinstance(cli_args, list):
                    raw_output, cmd = self._dispatch_cli_args(cli_args, tone)
                    response_intent = "cli"
                else:
                    raw_output, cmd = self._dispatch(intent, path, text, tone, feature_desc, output_path)
                    response_intent = intent
                response = self._postlude(response_intent, path, raw_output, tone)
                turn = Turn(
                    user=text, tone=tone, intent=response_intent, path=path,
                    command=cmd, output=raw_output, response=response,
                )
                self.history.append(turn)
                self.memory.update_from_turn(turn)
                self.memory.append_history(turn)
                self.memory.save()
                return response

        # ── Keyword-heuristic fallback (no LLM available) ─────────────────────
        path = _substitute_datetime_tokens(_extract_path(text) or str(self.working_dir))

        if self._pending_clarification:
            intent = self._clarification_ctx.get("intent", _classify_intent(text))
            new_path = _extract_path(text)
            if new_path:
                path = _substitute_datetime_tokens(new_path)
            elif text not in {"", ".", "here"}:
                path = _substitute_datetime_tokens(text.strip().strip("\"'")) or path
            self._pending_clarification = None
            self._clarification_ctx = {}
        else:
            lower_t = text.lower().strip()
            if lower_t in {"help", "?", "commands"} or any(
                p in lower_t for p in (
                    "what commands", "what can you", "what do you do",
                    "commands available", "show commands", "capabilities",
                )
            ):
                intent = "help"
            else:
                intent = _classify_intent(text)

        if intent == "rebuild" and path == str(self.working_dir) and not self.history:
            self._pending_clarification = "path"
            self._clarification_ctx = {"intent": intent}
            return self._ask_clarification(tone)

        raw_output, cmd = self._dispatch(intent, path, text, tone)
        response = self._postlude(intent, path, raw_output, tone)

        turn = Turn(
            user=text, tone=tone, intent=intent, path=path,
            command=cmd, output=raw_output, response=response,
        )
        self.history.append(turn)
        self.memory.update_from_turn(turn)
        self.memory.append_history(turn)
        self.memory.save()
        return response
