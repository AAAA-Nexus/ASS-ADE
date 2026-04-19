# Extracted from C:/!ass-ade/tests/test_engine_integration.py:401
# Component id: mo.source.ass_ade.test_hooks_receive_config
from __future__ import annotations

__version__ = "0.1.0"

def test_hooks_receive_config(self) -> None:
    mock_client = MagicMock()
    mock_client.certify_output_verify.return_value = MagicMock(rubric_passed=True)
    config = {"alphaverus": {"beam_width": 2}}
    gates = QualityGates(mock_client, config=config)
    # hook_alphaverus_refine uses self._v18_config — verify it's the right dict
    with patch("ass_ade.agent.alphaverus.AlphaVerus") as MockAV:
        instance = MockAV.return_value
        instance.tree_search.return_value = MagicMock(code="x=1", verified=True, score=0.9)
        result = gates.hook_alphaverus_refine("x = 1", "x == 1")
        # AlphaVerus was instantiated with our config
        MockAV.assert_called_once_with(config, mock_client)
