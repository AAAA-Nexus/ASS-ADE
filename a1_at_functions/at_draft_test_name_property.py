# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_name_property.py:7
# Component id: at.source.a1_at_functions.test_name_property
from __future__ import annotations

__version__ = "0.1.0"

def test_name_property(self) -> None:
    pipe = Pipeline("my-pipeline")
    assert pipe.name == "my-pipeline"
