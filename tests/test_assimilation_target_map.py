from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ass_ade.a1_at_functions.assimilation_target_map import build_assimilation_target_map
from ass_ade.cli import app


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_target_map_classifies_skip_assimilate_rebuild_and_enhance(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    sibling = tmp_path / "sibling"
    _write(
        primary / "src" / "ass_ade" / "core.py",
        '''
def duplicate(value):
    return value + 1


def existing(value):
    return value * 2
''',
    )
    _write(
        sibling / "src" / "candidate.py",
        '''
import pickle


def duplicate(value):
    return value + 1


def existing(value):
    """Sibling knows a safer branch."""
    return value * 3


def clean_new(value):
    """A small low-risk feature."""
    return value.strip()


def risky_new(value):
    return pickle.loads(value)
''',
    )
    _write(
        sibling / "tests" / "test_candidate.py",
        '''
from src.candidate import clean_new


def test_clean_new():
    assert clean_new(" x ") == "x"
''',
    )

    result = build_assimilation_target_map(primary_root=primary, sibling_roots=[sibling])
    by_name = {target.symbol.qualname: target for target in result.targets}

    assert by_name["duplicate"].action == "skip"
    assert by_name["existing"].action == "enhance"
    assert by_name["clean_new"].action == "assimilate"
    assert by_name["risky_new"].action == "rebuild"
    assert result.action_counts["assimilate"] == 1


def test_target_map_focus_filters_symbols(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    sibling = tmp_path / "sibling"
    _write(primary / "pkg.py", "def existing():\n    return 1\n")
    _write(
        sibling / "pkg.py",
        '''
def alpha_feature():
    """Alpha."""
    return 1


def beta_feature():
    """Beta."""
    return 2
''',
    )
    _write(sibling / "tests" / "test_pkg.py", "def test_alpha_feature():\n    assert True\n")

    result = build_assimilation_target_map(
        primary_root=primary,
        sibling_roots=[sibling],
        focus=["alpha"],
    )

    assert [target.symbol.qualname for target in result.targets] == ["alpha_feature"]


def test_cli_selfbuild_target_map_writes_json(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    sibling = tmp_path / "sibling"
    out = tmp_path / "target-map.json"
    _write(primary / "pkg.py", "def existing():\n    return 1\n")
    _write(sibling / "pkg.py", "def new_feature():\n    return 2\n")

    result = CliRunner().invoke(
        app,
        [
            "selfbuild",
            "target-map",
            "--primary",
            str(primary),
            "--sibling",
            str(sibling),
            "--out",
            str(out),
        ],
    )

    assert result.exit_code == 0, result.stdout + (result.stderr or "")
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "ass-ade.assimilation-target-map/v1"
    assert payload["action_counts"]["rebuild"] == 1
