# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/interpreter.py:281
# Component id: at.source.ass_ade.greeting
__version__ = "0.1.0"

    def greeting(self, working_dir: Path) -> str | None:
        if not self.user_profile:
            return None
        parts: list[str] = []
        tone = self.user_profile.get("dominant_tone", "formal")
        path_key = str(working_dir.resolve())
        ctx = self.project_contexts.get(path_key, {})
        recent = self.recent_history(3)

        if tone == TONE_CASUAL:
            parts.append("Hey, welcome back!")
        else:
            parts.append("Welcome back.")

        if ctx:
            last_cmds = [e.get("intent") for e in ctx.get("commands_run", [])[-3:]]
            if last_cmds:
                last = last_cmds[-1]
                if tone == TONE_CASUAL:
                    parts.append(f"Last time here we ran `{last}` on this project.")
                else:
                    parts.append(f"Last operation on this project: `{last}`.")

        fav = self.user_profile.get("favorite_command")
        if fav and fav != "chat":
            if tone == TONE_CASUAL:
                parts.append(f"Quick tip: `{fav}` is your most-used command.")
            else:
                parts.append(f"Most-used command: `{fav}`.")

        return " ".join(parts) if parts else None
