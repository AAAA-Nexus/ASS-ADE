# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_run_returns_dict.py:7
# Component id: at.source.a1_at_functions.test_run_returns_dict
from __future__ import annotations

__version__ = "0.1.0"

def test_run_returns_dict(self) -> None:
    b = BAS({})
    result = b.run({"metrics": {"synergy": 0.9}})
    assert "alert" in result
