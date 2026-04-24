"""Tier a3 — Atomadic Copilot.

A brainstorming companion for the playground. Unlike the main interpreter
(which executes tasks), the Copilot is conversation-first:

  • Takes a natural-language prompt from the user.
  • Has the full BlockRegistry in context (so it knows every available block).
  • Can propose a CompositionPlan as a JSON payload the frontend drops
    onto the canvas.
  • Can critique a WIP plan ("your a1→a2 edge crosses tiers; use a1.foo
    instead").
  • Suggests gap-fills when no block fits.

Offline-safe fallback: when no LLM provider is reachable, the Copilot
returns a deterministic keyword-match suggestion so the playground
remains usable without network access.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ass_ade.a2_mo_composites.block_registry import Block, BlockRegistry
from ass_ade.a3_og_features.composition_engine import (
    CompositionEdge,
    CompositionEngine,
    CompositionNode,
    CompositionPlan,
    Gap,
)


_SYSTEM_PROMPT = """You are the Atomadic Copilot — a brainstorming partner for composing
software features from verified building blocks (a0 constants, a1 pure functions,
a2 stateful composites, a3 features). The user will describe a goal, and you
propose a composition plan using the blocks provided in the EVIDENCE_JSON.

Rules:
  - Only reference block_ids that appear in EVIDENCE_JSON.blocks.
  - Target tier must be >= every block tier (upward composition only).
  - When no block fits, add a Gap node with a descriptive slug and hint.
  - Keep plans small (≤ 6 blocks) unless the user asks for more.
  - Return STRICT JSON matching the PlanSchema — no prose, no markdown.

PlanSchema:
{
  "name": "<short_snake_case>",
  "target_tier": "a3_og_features" | "a2_mo_composites" | ...,
  "description": "<one sentence>",
  "nodes": [{"id": "<block_id or gap:<slug>>", "alias": null}],
  "edges": [{"src": "<node_id>", "dst": "<node_id>", "port": "value"}],
  "gaps": [{"slug": "<snake_case>", "hint": "<what to synthesize>",
            "expected_kind": "function", "expected_tier": "a1_at_functions"}]
}
"""


@dataclass
class CopilotMessage:
    role: str            # "user" | "assistant" | "system"
    content: str


@dataclass
class CopilotResponse:
    """Structured output of a Copilot turn."""
    text: str                                # human-readable reply
    suggested_plan: dict | None = None       # CompositionPlan.to_dict(), if parseable
    relevant_blocks: list[dict] = field(default_factory=list)
    mode: str = "llm"                        # "llm" | "offline_fallback"
    raw: str = ""                            # raw model output

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "suggested_plan": self.suggested_plan,
            "relevant_blocks": list(self.relevant_blocks),
            "mode": self.mode,
            "raw": self.raw,
        }


# ── Offline fallback ────────────────────────────────────────────────────────

def _keyword_rank_blocks(query: str, blocks: list[Block], limit: int = 8) -> list[Block]:
    """Rank blocks by keyword overlap with the user query."""
    q = query.lower()
    tokens = set(re.findall(r"\w+", q))
    if not tokens:
        return []
    scored: list[tuple[int, Block]] = []
    for b in blocks:
        hay = f"{b.name} {b.qualname} {b.docstring}".lower()
        hay_tokens = set(re.findall(r"\w+", hay))
        overlap = len(tokens & hay_tokens)
        if overlap > 0:
            scored.append((overlap, b))
    scored.sort(key=lambda p: (-p[0], p[1].name))
    return [b for _, b in scored[:limit]]


def _offline_fallback_plan(query: str, registry: BlockRegistry) -> CopilotResponse:
    """Keyword-match blocks when no LLM is available."""
    ranked = _keyword_rank_blocks(query, registry.all_blocks())
    if not ranked:
        return CopilotResponse(
            text=(
                "I don't see any blocks that match that description offline. "
                "Try rephrasing, or describe the building blocks you'd expect."
            ),
            mode="offline_fallback",
        )

    # Compose top-3 into a linear pipeline as a starter
    chosen = [b for b in ranked[:3] if b.tier_prefix != "a4"]
    if not chosen:
        chosen = ranked[:3]

    # Pick the highest tier seen as the target, min a3
    tier_order = ["a0_qk_constants", "a1_at_functions", "a2_mo_composites", "a3_og_features", "a4_sy_orchestration"]
    max_rank = max(tier_order.index(b.tier) for b in chosen)
    target = tier_order[max(max_rank, tier_order.index("a3_og_features"))]

    nodes = [CompositionNode(id=b.id) for b in chosen]
    edges = [
        CompositionEdge(src=chosen[i].id, dst=chosen[i + 1].id)
        for i in range(len(chosen) - 1)
    ]
    slug = re.sub(r"[^a-z0-9]+", "_", query.lower()).strip("_")[:40] or "suggested"
    plan = CompositionPlan(
        name=f"auto_{slug}",
        target_tier=target,
        description=f"Offline keyword-match suggestion for: {query[:120]}",
        nodes=nodes,
        edges=edges,
    )
    return CopilotResponse(
        text=(
            f"Offline mode — here's a keyword-match starter using "
            f"{', '.join(b.name for b in chosen)}. Tweak on the canvas."
        ),
        suggested_plan=plan.to_dict(),
        relevant_blocks=[b.to_dict() for b in ranked[:8]],
        mode="offline_fallback",
    )


# ── LLM path ────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> dict | None:
    """Pull the first JSON object out of a response, tolerant of code fences."""
    # strip ```json ... ``` fences
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        candidate = fence.group(1)
    else:
        # first balanced {...} scan
        start = text.find("{")
        if start < 0:
            return None
        depth = 0
        end = -1
        for i, ch in enumerate(text[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end < 0:
            return None
        candidate = text[start:end]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def _build_evidence(registry: BlockRegistry, query: str, max_blocks: int = 40) -> dict:
    """Build a compact EVIDENCE_JSON payload — top-N keyword-ranked blocks."""
    top = _keyword_rank_blocks(query, registry.all_blocks(), limit=max_blocks)
    if not top:
        top = registry.all_blocks()[:max_blocks]
    return {
        "stats": registry.stats(),
        "blocks": [
            {
                "id": b.id,
                "name": b.name,
                "qualname": b.qualname,
                "tier": b.tier,
                "kind": b.kind,
                "signature": b.signature,
                "doc": b.docstring,
            }
            for b in top
        ],
    }


# ── Copilot agent ───────────────────────────────────────────────────────────

class AtomadicCopilot:
    """Conversational partner for composing features from the block registry."""

    def __init__(
        self,
        registry: BlockRegistry,
        *,
        config_path: str | Path | None = None,
        model: str | None = None,
    ) -> None:
        self._registry = registry
        self._config_path = Path(config_path).resolve() if config_path else None
        self._model = model
        self._history: list[CopilotMessage] = []

    @property
    def history(self) -> list[CopilotMessage]:
        return list(self._history)

    def reset(self) -> None:
        self._history.clear()

    def ask(self, user_text: str) -> CopilotResponse:
        """One turn. Appends both user and assistant messages to history."""
        self._history.append(CopilotMessage(role="user", content=user_text))
        try:
            response = self._ask_llm(user_text)
        except Exception:
            response = _offline_fallback_plan(user_text, self._registry)
        self._history.append(CopilotMessage(role="assistant", content=response.text))
        return response

    def critique_plan(self, plan_dict: dict) -> CopilotResponse:
        """Compile a plan, surface tier violations and gaps as a critique."""
        plan = CompositionPlan.from_dict(plan_dict)
        engine = CompositionEngine(self._registry)
        result = engine.compile(plan)
        parts: list[str] = [f"**Critique of `{plan.name}`**"]
        parts.append(f"- Verdict: **{result.verdict}**")
        if result.tier_violations:
            parts.append("- Tier violations:")
            for v in result.tier_violations:
                parts.append(f"  - {v}")
        if result.detected_gaps:
            parts.append("- Gaps:")
            for g in result.detected_gaps:
                parts.append(f"  - `{g.slug}`: {g.hint or '(no hint)'}")
        if not result.tier_violations and not result.detected_gaps:
            parts.append("- Clean composition — ready to materialize.")
        return CopilotResponse(
            text="\n".join(parts),
            suggested_plan=plan.to_dict(),
            mode="critique",
            raw=json.dumps(result.to_dict(), default=str)[:4000],
        )

    # ── Internals ──────────────────────────────────────────────────────────

    def _ask_llm(self, user_text: str) -> CopilotResponse:
        from ass_ade.config import load_config
        from ass_ade.engine.router import build_provider
        from ass_ade.engine.types import CompletionRequest, Message

        settings = load_config(self._config_path)
        provider = build_provider(settings)
        try:
            evidence = _build_evidence(self._registry, user_text)
            prompt = (
                f"USER GOAL:\n{user_text}\n\n"
                f"EVIDENCE_JSON:\n{json.dumps(evidence, indent=2, default=str)}\n\n"
                "Return a PlanSchema JSON object followed by a one-line human summary."
            )
            history_msgs = [Message(role=m.role, content=m.content) for m in self._history[-6:]]
            response = provider.complete(
                CompletionRequest(
                    messages=[
                        Message(role="system", content=_SYSTEM_PROMPT),
                        *history_msgs,
                        Message(role="user", content=prompt),
                    ],
                    model=self._model or settings.agent_model,
                    temperature=0.2,
                    max_tokens=1800,
                )
            )
            raw = response.message.content or ""
        finally:
            close = getattr(provider, "close", None)
            if callable(close):
                try:
                    close()
                except Exception:
                    pass

        plan_json = _extract_json(raw)
        # Human-readable part: everything after the JSON block
        text_after = raw
        if plan_json is not None:
            try:
                dumped = json.dumps(plan_json)
                idx = raw.find(dumped[:40]) if len(dumped) >= 40 else -1
                if idx >= 0:
                    text_after = raw[:idx].strip() or raw
            except Exception:
                pass
        summary = (text_after or raw).strip()
        if plan_json and summary == raw.strip():
            # Trim the JSON block out of the summary if still present
            summary = re.sub(r"```json.*?```", "", raw, flags=re.DOTALL).strip() or "Plan ready."

        return CopilotResponse(
            text=summary[:2000] if summary else "Plan ready.",
            suggested_plan=plan_json,
            relevant_blocks=evidence.get("blocks", [])[:8],
            mode="llm",
            raw=raw[:6000],
        )
