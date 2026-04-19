# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_memorystore.py:43
# Component id: mo.source.a2_mo_composites.save
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
