# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_default_config_is_empty_dict.py:7
# Component id: at.source.a1_at_functions.test_default_config_is_empty_dict
from __future__ import annotations

__version__ = "0.1.0"

def test_default_config_is_empty_dict(self) -> None:
    mock_client = MagicMock()
    gates = QualityGates(mock_client)
    assert gates._v18_config == {}
