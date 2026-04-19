# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_dependency_finds_external_deps.py:7
# Component id: at.source.a1_at_functions.test_dependency_finds_external_deps
from __future__ import annotations

__version__ = "0.1.0"

def test_dependency_finds_external_deps(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)

    assert result["python_files"] > 0
    assert isinstance(result["unique_external_deps"], int)
    assert isinstance(result["circular_deps"], list)
    assert isinstance(result["max_import_depth"], int)
