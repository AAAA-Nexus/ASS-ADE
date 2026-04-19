# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_teststepnames.py:7
# Component id: mo.source.a2_mo_composites.teststepnames
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
