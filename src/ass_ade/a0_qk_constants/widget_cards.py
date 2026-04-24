"""Tier a0 — typed A2UI widget card schemas.

These are the contract between the Python agent and any frontend that renders
generative UI cards. Each `WidgetKind` maps to a TypedDict payload shape.

Frontend code subscribes to `WIDGET_CARD` events on the AG-UI bus and switches
on `card.kind` to pick the right component:

    event.type === "WIDGET_CARD"
    event.data.kind === "scout_report"
    event.data.payload  // matches ScoutReportCard below

Keep these payloads small, JSON-safe, and additive — the frontend should ignore
unknown fields so this schema can evolve without breaking older clients.
"""

from __future__ import annotations

from typing import Literal, TypedDict


WidgetKind = Literal[
    "scout_report",
    "assimilation_table",
    "skill_result",
    "episode_recorded",
    "trust_gate_result",
    "command_result",
    "personality_snapshot",
    "anchor_added",
    "wiring_report",
    "cherry_manifest",
]


class ScoutReportCard(TypedDict, total=False):
    """Summary card emitted after `scout` runs. Full report is fetched via /scout/report."""
    repo: str
    filename: str
    counts: dict[str, int]  # action_counts: assimilate/enhance/rebuild/skip
    total_symbols: int
    tested_symbols: int
    llm_status: str
    opportunities: list[str]


class AssimilationTableRow(TypedDict, total=False):
    qualname: str
    module: str
    rel_path: str
    kind: str
    action: str
    confidence: float
    reasons: list[str]


class AssimilationTableCard(TypedDict, total=False):
    """Cherry-pick candidates table payload."""
    rows: list[AssimilationTableRow]
    action_filter: str
    min_confidence: float
    total_candidates: int


class SkillResultCard(TypedDict, total=False):
    """Fired each time a skill runs inside the interpreter."""
    name: str
    output: str
    working_dir: str


class EpisodeRecordedCard(TypedDict, total=False):
    project: str
    intents: list[str]
    note: str
    tags: list[str]


class TrustGateResultCard(TypedDict, total=False):
    gate: str  # "trust" | "drift" | "hallucination" | "prompt_inject"
    verdict: str  # "PASS" | "REFINE" | "QUARANTINE" | "REJECT"
    score: float
    evidence: list[str]


class CommandResultCard(TypedDict, total=False):
    command: str
    args: list[str]
    exit_code: int
    stdout_head: str
    stderr_head: str


class PersonalitySnapshotCard(TypedDict, total=False):
    persona: str
    energy: str
    verbosity: str
    domain_level: str
    use_emoji: bool


class AnchorAddedCard(TypedDict, total=False):
    key: str
    value: str


class WiringReportCard(TypedDict, total=False):
    """Emitted after a wire scan/apply completes."""
    source_dir: str
    violations_found: int
    auto_fixed: int
    would_fix: int
    not_fixable: int
    files_changed: int
    files_to_change: int
    verdict: str  # PASS | REFINE | DRY_RUN
    dry_run: bool
    manual_review_count: int


class CherryManifestCard(TypedDict, total=False):
    """Emitted when a cherry-pick manifest is created or refreshed."""
    source_label: str
    target_root: str
    selected_count: int
    actions: dict[str, int]  # assimilate/enhance/rebuild/skip totals


# Export-by-name registry for runtime lookup (e.g. doc generation, validation)
WIDGET_CARD_SCHEMAS: dict[str, type] = {
    "scout_report": ScoutReportCard,
    "assimilation_table": AssimilationTableCard,
    "skill_result": SkillResultCard,
    "episode_recorded": EpisodeRecordedCard,
    "trust_gate_result": TrustGateResultCard,
    "command_result": CommandResultCard,
    "personality_snapshot": PersonalitySnapshotCard,
    "anchor_added": AnchorAddedCard,
    "wiring_report": WiringReportCard,
    "cherry_manifest": CherryManifestCard,
}
