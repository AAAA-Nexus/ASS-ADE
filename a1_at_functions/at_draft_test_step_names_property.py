# Extracted from C:/!ass-ade/tests/test_pipeline.py:271
# Component id: at.source.ass_ade.test_step_names_property
from __future__ import annotations

__version__ = "0.1.0"

def test_step_names_property(self) -> None:
    pipe = Pipeline("names")
    pipe.add("alpha", pass_step)
    pipe.add("beta", pass_step)
    pipe.add("gamma", fail_step)
    assert pipe.step_names == ["alpha", "beta", "gamma"]
