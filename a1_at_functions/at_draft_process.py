# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:537
# Component id: at.source.ass_ade.process
from __future__ import annotations

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
    lower_text = text.lower()

    # ── Startup suggestion number dispatch ────────────────────────────────
    if self._startup_suggestions and re.fullmatch(r"[1-9]", text):
        idx = int(text) - 1
        if 0 <= idx < len(self._startup_suggestions):
            label = self._startup_suggestions[idx]
            # Translate suggestion label into a concrete user utterance and recurse
            _suggestion_intents = {
                "Fix": "lint .",
                "Add tests": "lint .",
                "Consider a rebuild": "rebuild .",
            }
            mapped = next(
                (v for k, v in _suggestion_intents.items() if label.startswith(k)),
                label,
            )
            self._startup_suggestions = []  # consume once
            return self.process(mapped)

    # ── Design approval gate ──────────────────────────────────────────────
    if self._pending_design_approval:
        approve_words = {"yes", "add it", "create it", "build it", "apply",
                         "go", "do it", "proceed", "yep", "yeah", "sure",
                         "ok", "looks good", "create the files"}
        reject_words = {"no", "cancel", "stop", "skip", "not now", "nope",
                        "don't", "hold off"}
        words = set(lower_text.split())
        if words & approve_words or any(p in lower_text for p in
                                        ("build it", "do it", "looks good", "add it", "create it")):
            self._pending_design_approval = False
            feature = self._pending_design_feature or "feature"
            path = str(self.working_dir)
            raw_output, cmd = self._dispatch("add-feature", path, feature, tone, feature_desc=feature)
            response = self._postlude("add-feature", path, raw_output, tone)
            turn = Turn(user=text, tone=tone, intent="add-feature", path=path,
                        command=cmd, output=raw_output, response=response)
            self.history.append(turn)
            self.memory.update_from_turn(turn)
            self.memory.append_history(turn)
            self.memory.save()
            return response
        if words & reject_words or any(p in lower_text for p in ("not now", "hold off")):
            self._pending_design_approval = False
            msg = ("Got it — blueprint saved but not applied. "
                   "Run `ass-ade rebuild` to materialize it whenever you're ready.")
            return msg

    # ── Add-feature — intercept before LLM (LLM doesn't know this intent) ──
    _add_feature_triggers = (
        "add a tool", "add a skill", "add a feature", "new tool",
        "new skill", "create a tool", "create a skill",
        "add web search", "add search tool", "new feature",
        "add feature", "add a web", "add an ", "create a new",
    )
    if any(t in lower_text for t in _add_feature_triggers):
        feature = self._extract_feature_desc(text) or text.strip()
        raw_output, cmd = self._dispatch(
            "add-feature", str(self.working_dir), text, tone, feature_desc=feature
        )
        response = self._postlude("add-feature", str(self.working_dir), raw_output, tone)
        turn = Turn(user=text, tone=tone, intent="add-feature",
                    path=str(self.working_dir), command=cmd,
                    output=raw_output, response=response)
        self.history.append(turn)
        self.memory.update_from_turn(turn)
        self.memory.append_history(turn)
        self.memory.save()
        return response

    # ── Memory save — intercept before LLM (LLM doesn't know this intent) ──
    _memory_triggers = (
        "remember my", "save that", "my name is", "call me ",
        "remember me as", "my email is", "my role is", "i'm a ",
        "i am a ", "i work as", "remember that", "note that",
        "don't forget", "save my",
    )
    if any(t in lower_text for t in _memory_triggers):
        raw_output, _cmd = self._dispatch("memory", str(self.working_dir), text, tone)
        response = self._postlude("memory", str(self.working_dir), raw_output, tone)
        turn = Turn(user=text, tone=tone, intent="memory", path=str(self.working_dir),
                    command=[], output=raw_output, response=response)
        self.history.append(turn)
        self.memory.update_from_turn(turn)
        self.memory.append_history(turn)
        self.memory.save()
        return response

    # ── Enhance apply-all conversational shortcut ─────────────────────────
    enhance_apply_ids = self._parse_enhance_apply(lower_text)
    if enhance_apply_ids is not None:
        path = self._last_scan_path or str(self.working_dir)
        ids_str = ",".join(str(i) for i in enhance_apply_ids)
        cmd = [sys.executable, "-m", "ass_ade", "enhance", path, "--apply", ids_str]
        self._print_dispatch("enhance", cmd)
        print(f"Applying {len(enhance_apply_ids)} enhancement(s): {ids_str}", flush=True)
        print(flush=True)
        raw_output = self._execute(cmd)
        response = self._postlude("enhance", path, raw_output, tone)
        turn = Turn(user=text, tone=tone, intent="enhance", path=path,
                    command=cmd, output=raw_output, response=response)
        self.history.append(turn)
        self.memory.update_from_turn(turn)
        self.memory.append_history(turn)
        self.memory.save()
        return response

    # ── LLM-first path ────────────────────────────────────────────────────
    llm_result = _call_llm(text, self.working_dir, _summarize_memory(self.memory))
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
