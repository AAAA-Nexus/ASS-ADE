"""Tier a0 — TypedDicts for cherry-pick manifests, candidate items, and assimilation results."""

from __future__ import annotations

from typing import TypedDict


class CherryItemDict(TypedDict):
    """One candidate symbol surfaced by cherry-pick from a scout report or direct scan."""

    index: int
    action: str  # "assimilate" | "rebuild" | "enhance"
    kind: str  # "function" | "class" | "method"
    qualname: str
    module: str
    rel_path: str
    source_root: str
    lineno: int
    end_lineno: int
    confidence: float
    reasons: list[str]
    recommended_path: str
    docstring_present: bool
    has_nearby_test: bool


class CherryManifestDict(TypedDict):
    """Saved manifest from a cherry-pick session; consumed by ass-ade assimilate."""

    schema_version: str
    source_label: str  # path to scout JSON or "direct-scan:<path>"
    source_root: str  # root of the scouted/scanned repo
    target_root: str  # intended assimilation target directory
    selected_count: int
    items: list[CherryItemDict]


class AssimilateResultDict(TypedDict):
    """Result for one symbol from an assimilate run."""

    qualname: str
    rel_path: str  # source relative path
    action: str
    status: str  # "written" | "skipped" | "dry_run" | "error"
    target_file: str  # written file (relative to target_root)
    tier: str  # a1_at_functions / a2_mo_composites
    lines: int  # lines written
    error: str  # non-empty on error
