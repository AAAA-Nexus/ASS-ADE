from __future__ import annotations

from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def minimal_pkg_root() -> Path:
    return _ROOT / "tests" / "fixtures" / "minimal_pkg"


@pytest.fixture
def repo_root() -> Path:
    return _ROOT
