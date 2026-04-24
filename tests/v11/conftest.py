from __future__ import annotations

from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent  # tests/v11
_ROOT = _HERE.parent.parent  # SEED root


@pytest.fixture
def minimal_pkg_root() -> Path:
    return _HERE / "fixtures" / "minimal_pkg"


@pytest.fixture
def repo_root() -> Path:
    return _ROOT
