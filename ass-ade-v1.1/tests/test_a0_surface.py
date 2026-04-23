"""Unit tests for a0 constants tables (Atomadic enhance / coverage)."""

from __future__ import annotations

from ass_ade_v11.a0_qk_constants import exclude_dirs, schemas, tier_names


def test_tier_names_tiers_match_prefix_map() -> None:
    assert set(tier_names.TIERS) == set(tier_names.TIER_PREFIX.keys())
    for tier, prefix in tier_names.TIER_PREFIX.items():
        assert tier_names.PREFIX_TO_TIER[prefix] == tier


def test_schemas_strings_are_non_empty_identifiers() -> None:
    for name in (
        "INGESTION_SCHEMA",
        "GAP_FILL_SCHEMA",
        "COMPONENT_SCHEMA_V11",
        "REGISTRY_SNAPSHOT_SCHEMA",
    ):
        val = getattr(schemas, name)
        assert isinstance(val, str)
        assert val.startswith("ASSADE-")


def test_exclude_dirs_covers_vcs_and_caches() -> None:
    assert ".git" in exclude_dirs.EXCLUDED_DIRS
    assert "__pycache__" in exclude_dirs.EXCLUDED_DIRS
    assert "node_modules" in exclude_dirs.EXCLUDED_DIRS
