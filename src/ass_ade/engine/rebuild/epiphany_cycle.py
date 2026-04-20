"""Pure helpers for the Epiphany → Breakthrough planning envelope (JSON document).

Used by MCP ``epiphany_breakthrough_cycle`` and ``local.planner``. No I/O.
"""

from __future__ import annotations

SCHEMA_VERSION = "ass-ade.epiphany-breakthrough-cycle.v1"


def detect_track_and_steps(goal: str) -> tuple[str, list[str]]:
    """Classify goal into a track id and default step list (planner / MCP)."""
    normalized = goal.lower()

    if any(token in normalized for token in ("doc", "readme", "guide", "write", "document")):
        return "documentation", [
            "Audit the current documentation surface and note the missing reader outcomes.",
            "Outline the smallest document set that explains installation, usage, and limits.",
            "Draft the content with a clear separation between local behavior and remote behavior.",
            "Proofread for consistency with the public/private boundary before publishing.",
        ]

    if any(token in normalized for token in ("api", "mcp", "nexus", "endpoint", "integrate")):
        return "integration", [
            "Inspect the public contract first: OpenAPI, A2A manifest, and MCP manifest.",
            "Define the smallest typed adapter needed for the chosen integration path.",
            "Implement the adapter with graceful fallback and explicit error handling.",
            "Run a live or mocked smoke check against the public contract before shipping.",
        ]

    if any(token in normalized for token in ("test", "verify", "validate", "qa")):
        return "validation", [
            "Define the behaviors that must be proven correct before changing code.",
            "Add focused tests around the highest-risk paths first.",
            "Run validation locally and record any gaps that remain outside public scope.",
            "Update docs or examples if the verified behavior changes user expectations.",
        ]

    return "implementation", [
        "Define the smallest public-safe slice of the goal that creates real user value.",
        "Inspect the relevant code or contract surface before making any change.",
        "Implement the smallest end-to-end path with clean local fallback behavior.",
        "Validate the result with focused tests or smoke checks and tighten docs if needed.",
    ]

EPIPHANY_PHASE_STEPS: list[str] = [
    "Epiphany — capture concrete observations (recon paths, failing tests, user quotes); tag deficits.",
    "Hypothesis — state falsifiable claims tied to epiphanies; avoid orphan speculation.",
    "Smallest experiment — one command or one file change that could invalidate the top hypothesis.",
    "Integration — fold only what survived experiments; defer the rest with explicit deficits.",
    "Promotion — run trust_gate / certify when profile allows; always run named tests before accept.",
]


def observations_to_epiphanies(observations: list[str]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for i, raw in enumerate(observations[:8]):
        text = str(raw).strip()
        if not text:
            continue
        out.append(
            {
                "id": f"e{i + 1}",
                "insight": text,
                "evidence_refs": [],
                "deficit_tags": [],
            }
        )
    if not out:
        out.append(
            {
                "id": "e1",
                "insight": (
                    "No observations yet — run phase0_recon (or paste failing output) "
                    "then re-run epiphany_breakthrough_cycle with observations[]."
                ),
                "evidence_refs": [],
                "deficit_tags": ["needs_grounding"],
            }
        )
    return out


def hypotheses_from_epiphanies(epiphanies: list[dict[str, object]]) -> list[dict[str, object]]:
    hy: list[dict[str, object]] = []
    for i, ep in enumerate(epiphanies[:8]):
        eid = str(ep.get("id", f"e{i + 1}"))
        hy.append(
            {
                "id": f"h{i + 1}",
                "statement": f"Address root cause suggested by {eid} with smallest reversible change.",
                "parent_epiphany_ids": [eid],
            }
        )
    return hy


def experiments_from_track(track: str, plan_steps: list[str]) -> list[dict[str, object]]:
    """Single default experiment slot; agents replace with repo-specific commands."""
    hint = "pytest -q path/to/tests"
    if track == "integration":
        hint = "python -m pytest tests/ -q --tb=no  # or MCP smoke against manifest"
    elif track == "documentation":
        hint = "docs link check or markdown linter configured for the repo"
    elif track == "validation":
        hint = "pytest -q on the highest-risk module named in recon"
    mid = plan_steps[1] if len(plan_steps) > 1 else (plan_steps[0] if plan_steps else "")
    return [
        {
            "id": "x1",
            "command_or_hint": hint,
            "success_criteria": "Exit 0 and no new failures vs baseline; record diff scope.",
            "grounding_from_plan": mid[:240],
        }
    ]


def promotion_checks() -> list[dict[str, str]]:
    return [
        {
            "id": "p1",
            "tool": "named_tests",
            "notes": "At least one named pytest or smoke command recorded and passing.",
        },
        {
            "id": "p2",
            "tool": "trust_gate",
            "notes": "When hybrid/premium profile: run trust_gate before treating output as production-safe.",
        },
        {
            "id": "p3",
            "tool": "certify_output",
            "notes": "Optional certify_output after substantive codegen for audit trail.",
        },
    ]


def build_epiphany_document(
    goal: str,
    *,
    track: str,
    plan_steps: list[str],
    recon_verdict: str | None,
    recon_files: list[str],
    observations: list[str],
) -> dict[str, object]:
    """Assemble the machine-readable cycle document (no filesystem access)."""
    epiphanies = observations_to_epiphanies(observations)
    hypotheses = hypotheses_from_epiphanies(epiphanies)
    experiments = experiments_from_track(track, plan_steps)
    files = [str(p) for p in recon_files[:24]]

    return {
        "schema_version": SCHEMA_VERSION,
        "goal": goal.strip(),
        "track": track,
        "epiphany_phase_steps": list(EPIPHANY_PHASE_STEPS),
        "epiphanies": epiphanies,
        "hypotheses": hypotheses,
        "experiments": experiments,
        "promotion_checks": promotion_checks(),
        "plan_steps": list(plan_steps),
        "recon": {
            "verdict": recon_verdict,
            "relevant_files": files,
        },
    }


def validate_epiphany_document(doc: object) -> list[str]:
    """Return human-readable errors; empty list means OK."""
    errs: list[str] = []
    if not isinstance(doc, dict):
        return ["document must be a JSON object"]
    if doc.get("schema_version") != SCHEMA_VERSION:
        errs.append("schema_version mismatch")
    if not str(doc.get("goal", "")).strip():
        errs.append("goal is required")
    for key in ("epiphanies", "hypotheses", "experiments", "promotion_checks", "plan_steps"):
        val = doc.get(key)
        if not isinstance(val, list) or not val:
            errs.append(f"{key} must be a non-empty array")
    if isinstance(doc.get("epiphanies"), list):
        for i, ep in enumerate(doc["epiphanies"]):
            if not isinstance(ep, dict) or not str(ep.get("insight", "")).strip():
                errs.append(f"epiphanies[{i}] needs non-empty insight")
    return errs
