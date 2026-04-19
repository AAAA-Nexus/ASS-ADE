# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lazy_init_atlas.py:7
# Component id: at.source.a1_at_functions.test_lazy_init_atlas
from __future__ import annotations

__version__ = "0.1.0"

def test_lazy_init_atlas(self) -> None:
    o = EngineOrchestrator({})
    assert o._atlas is None
    _ = o.atlas
    assert o._atlas is not None
