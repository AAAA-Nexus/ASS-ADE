"""Tier a3 — Composition Engine.

Takes a DAG of block_ids (from BlockRegistry) and a target tier, then:

  1. Validates the composition — all block tiers must compose upward only
     (target ≥ max block tier).
  2. Emits a tier-correct Python module that imports the blocks and calls
     them in DAG topological order.
  3. Detects gaps (edges referencing a non-existent block) and records them
     as synthesis candidates for the gap-filler (phase2).
  4. Optionally writes the composed module to disk at a tier-correct path.

The result is a `CompositionResult` with the source code, a list of gaps,
a target path, and a verdict (PASS | REFINE | REJECT).
"""

from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.tier_names import TIERS, TIER_PREFIX
from ass_ade.a2_mo_composites.block_registry import Block, BlockRegistry


# Target tier must be >= every block tier (blocks compose upward).
_TIER_ORDER = {t: i for i, t in enumerate(TIERS)}


@dataclass
class CompositionNode:
    """One node in a composition DAG."""
    id: str                          # block id from registry, OR "gap:<slug>" for a synthesis target
    alias: str | None = None         # optional local name override


@dataclass
class CompositionEdge:
    """Directed edge: src.output → dst.input."""
    src: str
    dst: str
    port: str = "value"


@dataclass
class Gap:
    """A missing block the composition references but doesn't exist yet."""
    slug: str                        # stable identifier the user / LLM refers to
    referenced_by: list[str]         # node_ids that depend on this gap
    expected_kind: str = "function"
    expected_tier: str = "a1_at_functions"
    hint: str = ""                   # user-provided description for synthesis


@dataclass
class CompositionPlan:
    """Input to the composition engine."""
    name: str                        # feature name, e.g. "scout_then_cherry"
    target_tier: str = "a3_og_features"
    nodes: list[CompositionNode] = field(default_factory=list)
    edges: list[CompositionEdge] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "CompositionPlan":
        return cls(
            name=data.get("name", "composed_feature"),
            target_tier=data.get("target_tier", "a3_og_features"),
            nodes=[CompositionNode(**n) for n in data.get("nodes", [])],
            edges=[CompositionEdge(**e) for e in data.get("edges", [])],
            gaps=[Gap(**g) for g in data.get("gaps", [])],
            description=data.get("description", ""),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "target_tier": self.target_tier,
            "nodes": [asdict(n) for n in self.nodes],
            "edges": [asdict(e) for e in self.edges],
            "gaps": [asdict(g) for g in self.gaps],
            "description": self.description,
        }


@dataclass
class CompositionResult:
    plan: CompositionPlan
    source_code: str
    target_path: str                 # tier-correct relative path
    tier_violations: list[str]
    detected_gaps: list[Gap]
    topo_order: list[str]
    verdict: str                     # PASS | REFINE | REJECT
    wrote_to_disk: bool = False

    def to_dict(self) -> dict:
        return {
            "plan": self.plan.to_dict(),
            "source_code": self.source_code,
            "target_path": self.target_path,
            "tier_violations": list(self.tier_violations),
            "detected_gaps": [asdict(g) for g in self.detected_gaps],
            "topo_order": list(self.topo_order),
            "verdict": self.verdict,
            "wrote_to_disk": self.wrote_to_disk,
        }


# ── Helpers ─────────────────────────────────────────────────────────────────

def _slugify(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_]+", "_", name.strip()).strip("_").lower()
    return s or "composed"


def _alias_for(block: Block, alias: str | None) -> str:
    return alias or block.name


def _topo_sort(node_ids: list[str], edges: list[CompositionEdge]) -> tuple[list[str], bool]:
    """Kahn's algorithm. Returns (order, has_cycle)."""
    in_degree: dict[str, int] = {n: 0 for n in node_ids}
    adj: dict[str, list[str]] = {n: [] for n in node_ids}
    for e in edges:
        if e.src in in_degree and e.dst in in_degree:
            adj[e.src].append(e.dst)
            in_degree[e.dst] = in_degree.get(e.dst, 0) + 1

    queue = [n for n in node_ids if in_degree[n] == 0]
    order: list[str] = []
    while queue:
        n = queue.pop(0)
        order.append(n)
        for succ in adj.get(n, []):
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                queue.append(succ)
    return order, len(order) != len(node_ids)


# ── Engine ──────────────────────────────────────────────────────────────────

class CompositionEngine:
    """Compile a CompositionPlan into a tier-pure Python module."""

    def __init__(self, registry: BlockRegistry) -> None:
        self._registry = registry

    def compile(self, plan: CompositionPlan) -> CompositionResult:
        """Validate, order, and emit source for the plan."""
        if plan.target_tier not in _TIER_ORDER:
            return CompositionResult(
                plan=plan,
                source_code="",
                target_path="",
                tier_violations=[f"unknown target_tier: {plan.target_tier}"],
                detected_gaps=list(plan.gaps),
                topo_order=[],
                verdict="REJECT",
            )

        target_rank = _TIER_ORDER[plan.target_tier]
        resolved_blocks: dict[str, Block] = {}
        detected_gaps: list[Gap] = list(plan.gaps)
        tier_violations: list[str] = []

        for node in plan.nodes:
            if node.id.startswith("gap:"):
                slug = node.id.split(":", 1)[1]
                # ensure a Gap record exists
                if not any(g.slug == slug for g in detected_gaps):
                    detected_gaps.append(Gap(slug=slug, referenced_by=[node.id]))
                continue
            block = self._registry.get(node.id)
            if block is None:
                detected_gaps.append(Gap(slug=_slugify(node.id), referenced_by=[node.id]))
                continue
            if _TIER_ORDER[block.tier] > target_rank:
                tier_violations.append(
                    f"block {block.qualname} is in {block.tier} but target is {plan.target_tier} "
                    f"(cannot import upward)"
                )
            resolved_blocks[node.id] = block

        node_ids = [n.id for n in plan.nodes]
        order, has_cycle = _topo_sort(node_ids, plan.edges)
        if has_cycle:
            tier_violations.append("composition DAG has a cycle")

        source = self._emit_source(plan, resolved_blocks, detected_gaps, order)
        target_path = self._target_path(plan)

        if tier_violations:
            verdict = "REJECT"
        elif detected_gaps or has_cycle:
            verdict = "REFINE"
        else:
            verdict = "PASS"

        return CompositionResult(
            plan=plan,
            source_code=source,
            target_path=target_path,
            tier_violations=tier_violations,
            detected_gaps=detected_gaps,
            topo_order=order,
            verdict=verdict,
        )

    def materialize(self, result: CompositionResult, root: Path) -> CompositionResult:
        """Write result.source_code to root/target_path. Only runs if verdict != REJECT."""
        if result.verdict == "REJECT":
            return result
        dest = root / result.target_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(result.source_code, encoding="utf-8")

        # Sanity-check the emitted source parses cleanly
        try:
            ast.parse(result.source_code)
        except SyntaxError as exc:
            return CompositionResult(
                plan=result.plan,
                source_code=result.source_code,
                target_path=result.target_path,
                tier_violations=result.tier_violations + [f"syntax error in emitted source: {exc}"],
                detected_gaps=result.detected_gaps,
                topo_order=result.topo_order,
                verdict="REJECT",
                wrote_to_disk=True,
            )

        return CompositionResult(
            plan=result.plan,
            source_code=result.source_code,
            target_path=result.target_path,
            tier_violations=result.tier_violations,
            detected_gaps=result.detected_gaps,
            topo_order=result.topo_order,
            verdict=result.verdict,
            wrote_to_disk=True,
        )

    # ── Source emission ────────────────────────────────────────────────────

    def _emit_source(
        self,
        plan: CompositionPlan,
        resolved: dict[str, Block],
        gaps: list[Gap],
        order: list[str],
    ) -> str:
        tier_short = TIER_PREFIX.get(plan.target_tier, "?")
        description = plan.description or f"Composed feature {plan.name}"
        lines: list[str] = [
            f'"""Tier {tier_short} — {description}',
            "",
            "Generated by ass-ade composition_engine. Edit by hand if needed —",
            "the engine preserves imports and top-level docstrings on recompose.",
            '"""',
            "",
            "from __future__ import annotations",
            "",
        ]

        # Imports, grouped by source module (stable order)
        imports_by_module: dict[str, list[str]] = {}
        for node in plan.nodes:
            block = resolved.get(node.id)
            if block is None:
                continue
            alias = node.alias
            imp_name = block.name if not alias or alias == block.name else f"{block.name} as {alias}"
            imports_by_module.setdefault(block.module, []).append(imp_name)
        for module in sorted(imports_by_module):
            names = ", ".join(sorted(set(imports_by_module[module])))
            lines.append(f"from {module} import {names}")

        # Gap stubs — emitted locally so the module type-checks before synthesis
        if gaps:
            lines.append("")
            lines.append("# Gap stubs — replaced by the synthesis engine in phase2_gapfill")
            for gap in gaps:
                lines.append(f"def {gap.slug}(*args, **kwargs):")
                hint = gap.hint or f"synthesis target (expected {gap.expected_kind}, tier {gap.expected_tier})"
                lines.append(f'    """GAP: {hint}"""')
                lines.append('    raise NotImplementedError("synthesize_missing_components must fill this gap")')
                lines.append("")

        # Main orchestration function — calls each block in topological order
        lines.append("")
        lines.append(f"def {_slugify(plan.name)}(**context) -> dict:")
        lines.append(f'    """Run the {plan.name} composition.')
        lines.append("")
        lines.append("    Each block is invoked in topological order. ``context`` is a dict")
        lines.append("    shared across all blocks — each block writes its return value under")
        lines.append("    the node_id key, so downstream blocks can consume it.")
        lines.append('    """')
        lines.append("    results: dict = dict(context)")
        for node_id in order:
            node = next((n for n in plan.nodes if n.id == node_id), None)
            if node is None:
                continue
            if node.id.startswith("gap:"):
                slug = node.id.split(":", 1)[1]
                lines.append(f"    results[{node.id!r}] = {slug}(results)")
            else:
                block = resolved.get(node.id)
                if block is None:
                    continue
                call_name = node.alias or block.name
                if block.kind == "constant":
                    lines.append(f"    results[{node.id!r}] = {call_name}")
                else:
                    lines.append(f"    results[{node.id!r}] = {call_name}(results)")
        lines.append("    return results")
        lines.append("")
        return "\n".join(lines)

    def _target_path(self, plan: CompositionPlan) -> str:
        return f"{plan.target_tier}/{_slugify(plan.name)}_feature.py"
