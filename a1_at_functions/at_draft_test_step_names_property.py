# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_step_names_property.py:7
# Component id: at.source.a1_at_functions.test_step_names_property
from __future__ import annotations

__version__ = "0.1.0"

def test_step_names_property(self) -> None:
    pipe = Pipeline("names")
    pipe.add("alpha", pass_step)
    pipe.add("beta", pass_step)
    pipe.add("gamma", fail_step)
    assert pipe.step_names == ["alpha", "beta", "gamma"]
