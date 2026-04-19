# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:263
# Component id: at.source.ass_ade.append_history
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
