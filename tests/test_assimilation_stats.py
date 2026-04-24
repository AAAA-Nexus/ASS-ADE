"""Tests for assimilation_stats aggregator (a3_og_features.assimilation_stats)."""

from __future__ import annotations

import json
from pathlib import Path

from ass_ade.a3_og_features.assimilation_stats import (
    aggregate_assimilation_stats,
    cherry_pick_candidates,
    collect_scout_reports,
    summarize_for_dashboard,
)


def _write_scout(path: Path, repo: str, counts: dict, targets: list[dict] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "ass-ade.scout/v1",
        "repo": repo,
        "summary": {"total_files": 10, "total_dirs": 3},
        "symbol_summary": {"symbols": 42, "tested_symbols": 12, "python_files": 7},
        "target_map": {"action_counts": counts, "targets": targets or []},
        "llm": {"status": "skipped"},
        "static_recommendations": [],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_collect_scout_reports_returns_empty_when_dir_missing(tmp_path: Path) -> None:
    assert collect_scout_reports(tmp_path) == []


def test_collect_scout_reports_finds_files(tmp_path: Path) -> None:
    _write_scout(tmp_path / ".ass-ade" / "scout-a.json", "/a", {"assimilate": 3})
    _write_scout(tmp_path / ".ass-ade" / "scout-b.json", "/b", {"assimilate": 1})
    reports = collect_scout_reports(tmp_path)
    assert len(reports) == 2
    repos = sorted(r["repo"] for r in reports)
    assert repos == ["/a", "/b"]


def test_aggregate_sums_action_counts(tmp_path: Path) -> None:
    _write_scout(tmp_path / ".ass-ade" / "scout-a.json", "/a", {"assimilate": 3, "skip": 2})
    _write_scout(tmp_path / ".ass-ade" / "scout-b.json", "/b", {"assimilate": 1, "enhance": 4})
    stats = aggregate_assimilation_stats(collect_scout_reports(tmp_path))

    assert stats["repos_scouted"] == 2
    assert stats["action_totals"]["assimilate"] == 4
    assert stats["action_totals"]["enhance"] == 4
    assert stats["action_totals"]["skip"] == 2
    assert stats["total_symbols"] == 84
    assert stats["total_tested_symbols"] == 24


def test_cherry_pick_candidates_filters_by_action_and_confidence(tmp_path: Path) -> None:
    targets = [
        {
            "action": "assimilate",
            "confidence": 0.9,
            "symbol": {"qualname": "pkg.hi", "module": "pkg", "rel_path": "pkg.py", "kind": "function"},
            "reasons": ["low-risk"],
            "recommended_path": "a1_at_functions/",
        },
        {
            "action": "assimilate",
            "confidence": 0.3,
            "symbol": {"qualname": "pkg.lo"},
        },
        {
            "action": "skip",
            "confidence": 0.99,
            "symbol": {"qualname": "pkg.skip_me"},
        },
    ]
    _write_scout(tmp_path / ".ass-ade" / "scout-a.json", "/a", {"assimilate": 2, "skip": 1}, targets)

    picked = cherry_pick_candidates(
        collect_scout_reports(tmp_path),
        action="assimilate",
        min_confidence=0.5,
    )
    qualnames = [p["qualname"] for p in picked]
    assert qualnames == ["pkg.hi"]
    assert picked[0]["confidence"] == 0.9
    assert picked[0]["recommended_path"] == "a1_at_functions/"


def test_summarize_for_dashboard_wraps_everything(tmp_path: Path) -> None:
    _write_scout(tmp_path / ".ass-ade" / "scout-a.json", "/a", {"assimilate": 2})
    out = summarize_for_dashboard(tmp_path)
    assert "stats" in out
    assert out["stats"]["repos_scouted"] == 1
    assert len(out["scout_reports"]) == 1
    assert out["scout_reports"][0]["counts"] == {"assimilate": 2}
