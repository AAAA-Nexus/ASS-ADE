from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade_v11.a4_sy_orchestration.run_rebuild_v11 import rebuild_project_v11


@pytest.mark.rebuild_v11
def test_rebuild_v11_runs_through_phase7(minimal_pkg_root: Path, tmp_path: Path) -> None:
    tag = "e2e-rebuild-v11"
    book = rebuild_project_v11(minimal_pkg_root, tmp_path, rebuild_tag=tag)
    assert book["stopped_after"] == 7
    assert book["rebuild_tag"] == tag

    root = Path(book["phase5"]["target_root"])
    assert root.is_dir()
    assert (root / "BLUEPRINT.json").is_file()

    audit = book["phase6"]["audit"]
    assert audit["validated"] is True
    assert audit["total"] >= 1
    assert audit["summary"]["structure_conformant"] is True

    pkg = book["phase7"]["package"]
    assert pkg["importable"] is True
    assert (Path(pkg["pyproject"])).is_file()
