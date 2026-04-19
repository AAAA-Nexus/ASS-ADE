# Extracted from C:/!ass-ade/tests/test_pipeline.py:278
# Component id: at.source.ass_ade.test_name_property
from __future__ import annotations

__version__ = "0.1.0"

def test_name_property(self) -> None:
    pipe = Pipeline("my-pipeline")
    assert pipe.name == "my-pipeline"
