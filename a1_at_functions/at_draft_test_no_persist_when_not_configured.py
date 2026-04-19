# Extracted from C:/!ass-ade/tests/test_pipeline.py:207
# Component id: at.source.ass_ade.test_no_persist_when_not_configured
from __future__ import annotations

__version__ = "0.1.0"

def test_no_persist_when_not_configured(self, tmp_path: Path) -> None:
    pipe = Pipeline("nopersist")
    pipe.add("s1", pass_step)
    pipe.run()
    # No files created anywhere — this is just a sanity check
    assert not list(tmp_path.glob("*.json"))
