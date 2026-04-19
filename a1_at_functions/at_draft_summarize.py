# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:357
# Component id: at.source.ass_ade.summarize
from __future__ import annotations

__version__ = "0.1.0"

def summarize(self) -> str:
    if not self.user_profile and not self.project_contexts:
        return "No memory yet. Start chatting to build it up."
    lines = ["**Atomadic memory**\n"]
    if self.user_profile:
        lines.append("**You:**")
        tone = self.user_profile.get("dominant_tone", "unknown")
        lines.append(f"  - Tone: {tone}")
        fav = self.user_profile.get("favorite_command")
        if fav:
            lines.append(f"  - Favorite command: `{fav}`")
        count = self.user_profile.get("session_interactions", 0)
        lines.append(f"  - Total interactions: {count}")
    if self.project_contexts:
        lines.append("\n**Projects:**")
        for path, ctx in list(self.project_contexts.items())[-5:]:
            name = Path(path).name
            last = ctx.get("last_seen", "")[:10]
            n_cmds = len(ctx.get("commands_run", []))
            lines.append(f"  - `{name}` — last seen {last}, {n_cmds} commands run")
    return "\n".join(lines)
