# Extracted from C:/!ass-ade/tests/test_engine_integration.py:390
# Component id: mo.source.ass_ade.test_default_config_is_empty_dict
from __future__ import annotations

__version__ = "0.1.0"

def test_default_config_is_empty_dict(self) -> None:
    mock_client = MagicMock()
    gates = QualityGates(mock_client)
    assert gates._v18_config == {}
