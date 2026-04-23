"""Import smoke tests — manifest driven (regenerate via ``ass-ade-v11 synth-tests``)."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

_MAN = Path(__file__).resolve().parent / "_qualnames.json"
QUALNAMES: list[str] = json.loads(_MAN.read_text(encoding="utf-8"))


@pytest.mark.generated_smoke
@pytest.mark.parametrize("qualname", QUALNAMES)
def test_import_smoke(qualname: str) -> None:
    mod = importlib.import_module(qualname)
    assert mod is not None
