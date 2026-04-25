from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ass_ade.a3_og_features.cherry_feature import preview_cherry_pick, run_cherry_pick
from ass_ade.cli import app


def _write_scout(path: Path) -> None:
    payload = {
        "schema_version": "ass-ade.scout/v1",
        "repo": str(path.parent),
        "target_map": {
            "action_counts": {"assimilate": 2, "rebuild": 1},
            "targets": [
                {
                    "action": "assimilate",
                    "confidence": 0.91,
                    "symbol": {
                        "root": str(path.parent),
                        "rel_path": "pkg.py",
                        "module": "pkg",
                        "qualname": "high_value",
                        "kind": "function",
                        "lineno": 1,
                        "end_lineno": 3,
                        "docstring_present": True,
                        "has_nearby_test": True,
                    },
                    "reasons": ["tested"],
                    "recommended_path": "a1_at_functions/",
                },
                {
                    "action": "assimilate",
                    "confidence": 0.4,
                    "symbol": {"qualname": "low_value", "module": "pkg", "rel_path": "pkg.py"},
                    "reasons": ["weak"],
                },
                {
                    "action": "rebuild",
                    "confidence": 0.8,
                    "symbol": {"qualname": "needs_rebuild", "module": "pkg", "rel_path": "pkg.py"},
                    "reasons": ["risk"],
                },
            ],
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_preview_cherry_pick_filters_confidence_and_summarizes(tmp_path: Path) -> None:
    scout = tmp_path / "scout.json"
    _write_scout(scout)

    preview = preview_cherry_pick(
        scout,
        tmp_path,
        actions={"assimilate"},
        min_confidence=0.5,
    )

    assert preview["summary"]["total"] == 1
    assert preview["summary"]["actions"] == {"assimilate": 1}
    assert preview["candidates"][0]["qualname"] == "high_value"


def test_run_cherry_pick_honors_confidence_filter(tmp_path: Path) -> None:
    scout = tmp_path / "scout.json"
    _write_scout(scout)

    manifest = run_cherry_pick(
        scout,
        tmp_path,
        pick="all",
        interactive=False,
        console_print=False,
        min_confidence=0.5,
    )

    assert manifest["selected_count"] == 2
    assert {item["qualname"] for item in manifest["items"]} == {"high_value", "needs_rebuild"}


def test_direct_scan_excludes_control_and_worktree_dirs(tmp_path: Path) -> None:
    live = tmp_path / "src" / "real.py"
    live.parent.mkdir(parents=True)
    live.write_text("def live_symbol():\n    return 1\n", encoding="utf-8")

    hidden = tmp_path / ".hive" / ".worktrees" / "old.py"
    hidden.parent.mkdir(parents=True)
    hidden.write_text("def stale_symbol():\n    return 2\n", encoding="utf-8")

    preview = preview_cherry_pick(tmp_path, tmp_path)
    names = {item["qualname"] for item in preview["candidates"]}

    assert "live_symbol" in names
    assert "stale_symbol" not in names


def test_cli_cherry_pick_preview_json(tmp_path: Path) -> None:
    scout = tmp_path / "scout.json"
    _write_scout(scout)

    result = CliRunner().invoke(
        app,
        [
            "cherry-pick",
            str(scout),
            "--preview",
            "--action",
            "assimilate",
            "--min-confidence",
            "0.5",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.stdout + (result.stderr or "")
    payload = json.loads(result.stdout)
    assert payload["summary"]["total"] == 1


def test_cli_cherry_pick_quiet_json_is_parseable(tmp_path: Path) -> None:
    scout = tmp_path / "scout.json"
    _write_scout(scout)

    result = CliRunner().invoke(
        app,
        [
            "cherry-pick",
            str(scout),
            "--pick",
            "all",
            "--min-confidence",
            "0.5",
            "--quiet",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.stdout + (result.stderr or "")
    payload = json.loads(result.stdout)
    assert payload["selected_count"] == 2
