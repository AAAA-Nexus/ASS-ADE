# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_engineorchestrator.py:498
# Component id: mo.source.a2_mo_composites.engine_report
from __future__ import annotations

__version__ = "0.1.0"

def engine_report(self) -> dict:
    """Combined report from all initialized engines."""
    reports: dict[str, Any] = {}
    for name, getter in [
        ("atlas", lambda: self._atlas),
        ("bas", lambda: self._bas),
        ("wisdom", lambda: self._wisdom),
        ("gvu", lambda: self._gvu),
        ("tdmi", lambda: self._tdmi),
        ("edee", lambda: self._edee),
        ("severa", lambda: self._severa),
        ("ide", lambda: self._ide),
        ("lifr", lambda: self._lifr),
        ("puppeteer", lambda: self._puppeteer),
        ("sam", lambda: self._sam),
        ("lse", lambda: self._lse),
        ("tca", lambda: self._tca),
        ("cie", lambda: self._cie),
        ("lora_flywheel", lambda: self._lora_flywheel),
    ]:
        engine = getter()
        if engine is not None:
            try:
                reports[name] = engine.report()
            except Exception:
                pass
    return reports
