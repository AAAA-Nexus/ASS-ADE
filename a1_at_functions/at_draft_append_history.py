# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_append_history.py:7
# Component id: at.source.a1_at_functions.append_history
from __future__ import annotations

__version__ = "0.1.0"

def append_history(self, turn: "Turn") -> None:
    try:
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "user": turn.user,
            "intent": turn.intent,
            "tone": turn.tone,
            "path": turn.path,
            "ok": "[error" not in (turn.output or "").lower(),
        }
        lines: list[str] = []
        if self._history_path.exists():
            lines = self._history_path.read_text(encoding="utf-8").splitlines()
        lines.append(json.dumps(entry))
        lines = lines[-_HISTORY_MAX:]
        self._history_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError:
        pass
