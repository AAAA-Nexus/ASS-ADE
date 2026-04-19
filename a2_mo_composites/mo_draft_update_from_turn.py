# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_memorystore.py:114
# Component id: mo.source.ass_ade.update_from_turn
__version__ = "0.1.0"

    def update_from_turn(self, turn: "Turn") -> None:
        profile = self.user_profile
        # Tone frequency tracking
        tones = profile.setdefault("tone_counts", {})
        tones[turn.tone] = tones.get(turn.tone, 0) + 1
        # Dominant tone
        profile["dominant_tone"] = max(tones, key=lambda k: tones[k])
        # Command frequency
        cmds = profile.setdefault("command_counts", {})
        cmds[turn.intent] = cmds.get(turn.intent, 0) + 1
        profile["favorite_command"] = max(cmds, key=lambda k: cmds[k])
        # Session count
        profile["session_interactions"] = profile.get("session_interactions", 0) + 1

        # Project context
        path_key = str(Path(turn.path).resolve())
        ctx = self.project_contexts.setdefault(path_key, {})
        ctx.setdefault("first_seen", datetime.now(timezone.utc).isoformat())
        ctx["last_seen"] = datetime.now(timezone.utc).isoformat()
        intent_log = ctx.setdefault("commands_run", [])
        intent_log.append({"intent": turn.intent, "ts": datetime.now(timezone.utc).isoformat()})
        ctx["commands_run"] = intent_log[-50:]  # keep last 50 per project
