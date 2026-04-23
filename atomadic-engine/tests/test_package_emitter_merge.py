"""Tests for emitted-package dependency merge (rebuild / package_emitter)."""

from __future__ import annotations

from ass_ade.engine.rebuild.package_emitter import (
    _DEFAULT_PYPROJECT_DEPS,
    _merge_emit_dependencies,
)


def test_merge_empty_uses_defaults() -> None:
    assert _merge_emit_dependencies([]) == list(_DEFAULT_PYPROJECT_DEPS)


def test_merge_adds_jsonschema_when_source_omits() -> None:
    source = [
        "httpx>=0.28,<0.29",
        "pydantic>=2.11,<3",
        "python-dotenv>=1.0,<2",
        "rich>=14,<15",
        "typer>=0.15,<1",
    ]
    merged = _merge_emit_dependencies(source)
    assert "jsonschema>=4.23,<5" in merged
    assert merged[0] == "httpx>=0.28,<0.29"


def test_merge_source_wins_version_pin() -> None:
    source = [
        "httpx>=0.28,<0.29",
        "pydantic>=2.11,<3",
        "python-dotenv>=1.0,<2",
        "rich>=14,<15",
        "typer>=0.15,<1",
        "jsonschema>=4.23,<5",
    ]
    merged = _merge_emit_dependencies(source)
    assert merged == list(_DEFAULT_PYPROJECT_DEPS)


def test_merge_appends_source_only_extra() -> None:
    source = [
        "httpx>=0.28,<0.29",
        "pydantic>=2.11,<3",
        "python-dotenv>=1.0,<2",
        "rich>=14,<15",
        "typer>=0.15,<1",
        "orjson>=3.9,<4",
    ]
    merged = _merge_emit_dependencies(source)
    assert merged[-1] == "orjson>=3.9,<4"
    assert "jsonschema>=4.23,<5" in merged
