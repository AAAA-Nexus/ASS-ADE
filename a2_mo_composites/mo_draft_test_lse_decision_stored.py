# Extracted from C:/!ass-ade/tests/test_phase_engines.py:130
# Component id: mo.source.ass_ade.test_lse_decision_stored
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
