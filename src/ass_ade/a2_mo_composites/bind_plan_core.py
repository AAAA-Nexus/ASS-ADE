"""Tier a2 — assimilated class 'BindPlan'

Assimilated from: types.py:274-295
"""

from __future__ import annotations


# --- assimilated symbol ---
class BindPlan:
    """Binder output.

    `fallback_atoms` records runner-up candidates within SCORING_EPSILON
    of the winner, for downstream consumer introspection and genesis log
    audit trails. `trust_receipt` is the Nexus postflight handle sealed
    into the plan per `_PROTOCOL.md §11.3`: an opaque receipt, never
    the raw hallucination ceiling. `None` in offline mode where the
    binder is invoked without a Nexus transport (tests + bootstrap).
    """

    reused: list[AtomRef] = field(default_factory=list)
    extended: list[AtomRef] = field(default_factory=list)
    refactored: list[RefactorDesc] = field(default_factory=list)
    synthesized: list[SynthDesc] = field(default_factory=list)
    fallback_atoms: dict[str, list[AtomRef]] = field(default_factory=dict)
    bindings_lock: LockFile | None = None
    phase_transition: bool = False
    needs_human: list[str] = field(default_factory=list)
    manifest_fingerprint: str = ""
    trust_receipt: TrustReceiptLike | None = None
    nexus_preflight: PreflightResultLike | None = None

