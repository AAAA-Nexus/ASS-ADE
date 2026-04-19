# Extracted from C:/!ass-ade/tests/test_pipeline.py:270
# Component id: mo.source.ass_ade.teststepnames
from __future__ import annotations

__version__ = "0.1.0"

class TestStepNames:
    def test_step_names_property(self) -> None:
        pipe = Pipeline("names")
        pipe.add("alpha", pass_step)
        pipe.add("beta", pass_step)
        pipe.add("gamma", fail_step)
        assert pipe.step_names == ["alpha", "beta", "gamma"]

    def test_name_property(self) -> None:
        pipe = Pipeline("my-pipeline")
        assert pipe.name == "my-pipeline"
