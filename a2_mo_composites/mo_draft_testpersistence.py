# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpersistence.py:7
# Component id: mo.source.a2_mo_composites.testpersistence
from __future__ import annotations

__version__ = "0.1.0"

class TestPersistence:
    def test_persist_creates_file(self, tmp_path: Path) -> None:
        pipe = Pipeline("persist", persist_dir=str(tmp_path))
        pipe.add("s1", pass_step)
        pipe.run()

        files = list(tmp_path.glob("persist_*.json"))
        assert len(files) == 1

        data = json.loads(files[0].read_text())
        assert data["name"] == "persist"
        assert data["passed"] is True
        assert len(data["steps"]) == 1

    def test_persist_records_failure(self, tmp_path: Path) -> None:
        pipe = Pipeline("failp", persist_dir=str(tmp_path))
        pipe.add("s1", fail_step)
        pipe.run()

        files = list(tmp_path.glob("failp_*.json"))
        data = json.loads(files[0].read_text())
        assert data["passed"] is False
        assert data["steps"][0]["error"] == "something broke"

    def test_no_persist_when_not_configured(self, tmp_path: Path) -> None:
        pipe = Pipeline("nopersist")
        pipe.add("s1", pass_step)
        pipe.run()
        # No files created anywhere — this is just a sanity check
        assert not list(tmp_path.glob("*.json"))
