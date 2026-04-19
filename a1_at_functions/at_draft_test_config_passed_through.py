# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_config_passed_through.py:7
# Component id: at.source.a1_at_functions.test_config_passed_through
from __future__ import annotations

__version__ = "0.1.0"

def test_config_passed_through(self) -> None:
    mock_client = MagicMock()
    config = {"alphaverus": {"beam_width": 8}, "dgm_h": {"simulation_cycles": 20}}
    gates = QualityGates(mock_client, config=config)
    assert gates._v18_config == config
