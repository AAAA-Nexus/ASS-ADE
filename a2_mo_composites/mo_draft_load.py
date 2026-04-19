# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_memorystore.py:27
# Component id: mo.source.a2_mo_composites.load
from __future__ import annotations

__version__ = "0.1.0"

def load(cls) -> "MemoryStore":
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    store = cls()
    for attr, filename in [
        ("user_profile", "user_profile.json"),
        ("project_contexts", "project_contexts.json"),
        ("preferences", "preferences.json"),
    ]:
        p = _MEMORY_DIR / filename
        if p.exists():
            try:
                setattr(store, attr, json.loads(p.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                pass
    return store
