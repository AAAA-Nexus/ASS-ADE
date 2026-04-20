"""Forge-gate public contract (a0, frozen by plan r2 task T-P1).

This module declares the public response envelope schema and the closed
`reason_code` enum that every Forge-gate endpoint, every internal MCP
forge.gate.* tool, and every ASS-ADE a2/a3 client for those tools MUST
conform to.

Tier: a0 (pure, per .ass-ade/tier-map.json). No I/O, no logic, no imports
from a1..a4. Safe for open source.

IP boundary (authoritative):
This file belongs to the PUBLIC surface. It must not name or reveal any
numeric constant, theorem identifier, internal proof-layer mnemonic, or
sovereign-lattice terminology. The only public handle to a theorem is the
opaque reference string shape ``AN-TH-<slug>`` carried in the envelope.
See plan r2 `research.md` and `plan.md` for the non-disclosure allow-list
that ``ass-ade-nexus-enforcer`` enforces via the IP-boundary lint.

Plan: autopoietic-ai-research-enhance-assade-r2-20260420-0212 (task T-P1).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final, Optional


class ReasonCode(str, Enum):
    """Closed string enum for every Forge-gate outcome.

    Closed means: no free-form error strings are permitted in a response
    envelope. A Forge-gate implementation that cannot map an outcome to one
    of these values MUST return ``REJECT_UNKNOWN`` and quarantine the
    variant; it MUST NOT invent a new code.
    """

    OK = "OK"

    REJECT_ADMISSION_PARITY = "REJECT_ADMISSION_PARITY"
    REJECT_SAFETY_ENVELOPE = "REJECT_SAFETY_ENVELOPE"
    REJECT_STRUCTURAL_CLOSURE = "REJECT_STRUCTURAL_CLOSURE"
    REJECT_DRIFT_SNR = "REJECT_DRIFT_SNR"
    REJECT_STABILITY_INTERVAL = "REJECT_STABILITY_INTERVAL"
    REJECT_ORACLE_NOISE_FLOOR = "REJECT_ORACLE_NOISE_FLOOR"
    REJECT_TRUST_CEILING = "REJECT_TRUST_CEILING"
    REJECT_DELEGATION_DEPTH = "REJECT_DELEGATION_DEPTH"
    REJECT_LINEAGE_UNREACHABLE = "REJECT_LINEAGE_UNREACHABLE"

    REJECT_UNKNOWN = "REJECT_UNKNOWN"


REASON_CODES_ALLOW_LIST: Final[frozenset[str]] = frozenset(rc.value for rc in ReasonCode)


OPAQUE_REF_PREFIX: Final[str] = "AN-TH-"


@dataclass(frozen=True)
class ForgeGateResponse:
    """Canonical public response envelope for all three Forge-gate surfaces.

    Attributes:
        passed: Whether the gate admitted the input.
        opaque_ref: Public, stable handle to the backing proof. Shape is
            ``AN-TH-<slug>`` where ``<slug>`` is an ASCII identifier with no
            embedded numeric constants from the private proof layer.
        reason_code: Closed enum value from ``ReasonCode``. Never free-form.
        trust_score_normalised: Scalar in the closed interval ``[0.0, 1.0]``.
            Already normalised by the gate; callers do not apply additional
            scaling and MUST NOT infer thresholds from this value.
        lineage_ref: Required on rollback responses, optional elsewhere.
            Opaque pointer into the evolution-log archive. No internal
            index is exposed.
    """

    passed: bool
    opaque_ref: str
    reason_code: ReasonCode
    trust_score_normalised: float
    lineage_ref: Optional[str] = None


TRUST_SCORE_MIN: Final[float] = 0.0
TRUST_SCORE_MAX: Final[float] = 1.0


ENVELOPE_SCHEMA_VERSION: Final[str] = "forge-gate/response/v1"
