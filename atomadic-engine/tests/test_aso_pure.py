"""Tier a1 — ASO pure helpers."""

from __future__ import annotations

from pathlib import Path

from ass_ade.aso.pure import aso_layout_paths, is_valid_topology, merge_swarm_config_payload


def test_topology_validation() -> None:
    assert is_valid_topology("parallel")
    assert not is_valid_topology("triangle")


def test_merge_swarm_config_roundtrip() -> None:
    merged = merge_swarm_config_payload(
        {"topology": "sequential", "schema": "ass-ade.swarm-config.v0"},
        topology="hierarchical",
        shared_memory_endpoint="http://localhost:9999",
        notes="unit",
    )
    assert merged["topology"] == "hierarchical"
    assert merged["shared_memory_endpoint"] == "http://localhost:9999"


def test_aso_layout_paths() -> None:
    p = aso_layout_paths(Path("/tmp/repo"))
    assert p["aso_root"] == Path("/tmp/repo") / ".ass-ade" / "aso"
    assert p["swarm_config"].name == "config.json"
