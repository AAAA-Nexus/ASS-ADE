"""Regression: published demos stay PASS-marked; CLI import chain stays within a loose CI budget."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEMOS = _REPO_ROOT / "docs" / "demos"
_DEMO_FILES = (
    "DEMO1_BLUEPRINT_BUILD.md",
    "DEMO2_HALF_BUILT_COMPLETION.md",
    "DEMO3_FEATURE_ENHANCEMENT.md",
)
_STATUS_NEEDLE = "**Status:** PASS ✓"


@pytest.mark.parametrize("filename", _DEMO_FILES)
def test_demo_markdown_reports_pass(filename: str) -> None:
    path = _DEMOS / filename
    assert path.is_file(), f"missing demo doc {path}"
    text = path.read_text(encoding="utf-8")
    assert _STATUS_NEEDLE in text, f"{filename} must keep {_STATUS_NEEDLE!r} for CI demo gate"


def test_ass_ade_cli_import_under_loose_budget() -> None:
    """Warm-cache import budget — catches catastrophic import regressions, not micro-optimizations."""
    if __import__("os").environ.get("ASS_ADE_SKIP_IMPORT_BENCH") == "1":
        pytest.skip("ASS_ADE_SKIP_IMPORT_BENCH=1")
    t0 = time.perf_counter()
    import ass_ade.cli  # noqa: F401

    elapsed = time.perf_counter() - t0
    assert elapsed < 90.0, f"import ass_ade.cli took {elapsed:.1f}s (expected < 90s on CI)"
