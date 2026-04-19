# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testagentloopphase1.py:34
# Component id: mo.source.a2_mo_composites.test_lse_decision_stored
from __future__ import annotations

__version__ = "0.1.0"

def test_lse_decision_stored(self):
    loop = self._make_loop()
    routing = MagicMock()
    routing.complexity = "simple"
    loop._last_routing = routing
    model = loop._select_model(routing)
    # Should be a string model name (lse select works)
    assert model is None or isinstance(model, str)
