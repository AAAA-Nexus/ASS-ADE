# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1199
# Component id: mo.source.a2_mo_composites.lora_adapter_current
from __future__ import annotations

__version__ = "0.1.0"

def lora_adapter_current(self, language: str = "python", **kwargs: Any) -> dict[str, Any]:
    """GET /v1/lora/adapter/{language} — latest adapter id for a language."""
    return self._get_raw(f"/v1/lora/adapter/{_pseg(language, 'language')}", **kwargs)
