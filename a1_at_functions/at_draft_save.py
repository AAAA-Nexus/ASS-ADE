# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:225
# Component id: at.source.ass_ade.save
from __future__ import annotations

__version__ = "0.1.0"

def save(self) -> None:
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    for attr, filename in [
        ("user_profile", "user_profile.json"),
        ("project_contexts", "project_contexts.json"),
        ("preferences", "preferences.json"),
    ]:
        p = _MEMORY_DIR / filename
        try:
            p.write_text(
                json.dumps(getattr(self, attr), indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            pass
