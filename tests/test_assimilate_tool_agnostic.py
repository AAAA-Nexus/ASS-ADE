from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_tool():
    path = Path(__file__).resolve().parents[1] / "tools" / "assimilate_v11_plus_legacy.py"
    spec = importlib.util.spec_from_file_location("assimilate_v11_plus_legacy", path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_root_ids_are_source_agnostic_and_unique(tmp_path: Path) -> None:
    tool = _load_tool()
    primary = tmp_path / "seed"
    a = tmp_path / "source"
    b = tmp_path / "source-copy"
    primary.mkdir()
    a.mkdir()
    b.mkdir()

    assert tool._root_ids(primary, [a, b], None) == ["seed", "source", "source_copy"]


def test_root_ids_accept_explicit_ids(tmp_path: Path) -> None:
    tool = _load_tool()
    primary = tmp_path / "primary"
    source = tmp_path / "donor"
    primary.mkdir()
    source.mkdir()

    assert tool._root_ids(primary, [source], ["map", "mcp"]) == ["map", "mcp"]


def test_dedupe_roots_removes_primary_and_duplicates(tmp_path: Path) -> None:
    tool = _load_tool()
    primary = tmp_path / "primary"
    source = tmp_path / "source"
    primary.mkdir()
    source.mkdir()

    result = tool._dedupe_roots(primary, [primary, source, source])

    assert result == [source.resolve()]
