"""Tests for Cap-C feature → blueprint proposer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade.engine.rebuild import feature as FMOD
from ass_ade.engine.rebuild.feature import (
    _parse_components,
    propose_feature_blueprint,
)


def test_parse_components_accepts_clean_json() -> None:
    text = json.dumps([
        {"name": "TokenBucket", "tier": "a2_mo_composites",
         "purpose": "rate limiter", "signature": "def acquire(self) -> bool:"},
    ])
    out = _parse_components(text)
    assert out and out[0]["name"] == "token_bucket"
    assert out[0]["tier"] == "a2_mo_composites"


def test_parse_components_strips_markdown_fence() -> None:
    text = "```json\n" + json.dumps([
        {"name": "cfg", "tier": "a0_qk_constants"},
    ]) + "\n```"
    out = _parse_components(text)
    assert out and out[0]["tier"] == "a0_qk_constants"


def test_parse_components_rejects_invalid_tier() -> None:
    text = json.dumps([{"name": "x", "tier": "bogus"}])
    assert _parse_components(text) is None


def test_parse_components_rejects_non_json() -> None:
    assert _parse_components("not-json") is None


def test_propose_blueprint_with_fallback(monkeypatch) -> None:
    monkeypatch.setattr(FMOD, "_propose_via_nexus", lambda *a, **kw: None)
    bp = propose_feature_blueprint(
        "add a rate limiter middleware",
        feature_name="rate_limiter",
        allow_fallback=True,
    )
    assert bp["schema"] == "AAAA-SPEC-004"
    assert bp["blueprint_id"].startswith("bp_")
    assert bp["components"], "fallback must emit at least one component"
    assert bp["metadata"]["source"] == "fallback"
    for c in bp["components"]:
        assert c["id"].startswith(("qk_", "at_", "mo_", "og_", "sy_"))


def test_propose_blueprint_no_fallback_raises(monkeypatch) -> None:
    monkeypatch.setattr(FMOD, "_propose_via_nexus", lambda *a, **kw: None)
    with pytest.raises(RuntimeError):
        propose_feature_blueprint(
            "any feature",
            allow_fallback=False,
        )


def test_propose_blueprint_uses_nexus_when_available(monkeypatch) -> None:
    monkeypatch.setattr(
        FMOD,
        "_propose_via_nexus",
        lambda *a, **kw: [
            {"name": "RateLimiter", "tier": "a2_mo_composites",
             "purpose": "per-ip bucket", "signature": "def check(ip): ..."},
            {"name": "LimitConfig", "tier": "a0_qk_constants",
             "purpose": "constants", "signature": ""},
        ],
    )
    bp = propose_feature_blueprint("limit traffic", feature_name="rl")
    assert bp["metadata"]["source"] == "nexus"
    names = {c["name"] for c in bp["components"]}
    assert "rate_limiter" in names
    assert "limit_config" in names
    assert set(bp["tiers"]) == {"a2_mo_composites", "a0_qk_constants"}


def test_blueprint_roundtrips_through_json(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(FMOD, "_propose_via_nexus", lambda *a, **kw: None)
    bp = propose_feature_blueprint("x", allow_fallback=True)
    path = tmp_path / "bp.json"
    path.write_text(json.dumps(bp), encoding="utf-8")
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["schema"] == "AAAA-SPEC-004"
