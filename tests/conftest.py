"""Shared test fixtures and path setup for the ASS-ADE seed test suite."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
for _path in (_ROOT, _SRC):
    if _path.is_dir() and str(_path) not in sys.path:
        sys.path.insert(0, str(_path))


@pytest.fixture
def repo_root() -> Path:
    return _ROOT


@pytest.fixture
def minimal_pkg_root() -> Path:
    """Minimal fixture package used by monadic pipeline tests."""
    # Try both possible locations (engine tests use tests/fixtures, v11 tests use tests/v11/fixtures)
    candidates = [
        _ROOT / "tests" / "fixtures" / "minimal_pkg",
        _ROOT / "tests" / "v11" / "fixtures" / "minimal_pkg",
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"minimal_pkg fixture not found; checked: {candidates}")
