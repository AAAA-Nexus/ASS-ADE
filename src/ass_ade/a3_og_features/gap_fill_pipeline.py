"""Tier a3 — Gap-Fill Pipeline.

The playground's tight loop: take a CompositionPlan that the engine marked
REFINE (because of gaps), fill every gap, re-compile, materialize, wire, and
report. Uses the configured LLM provider (engine/router) to synthesize gap
bodies; falls back to a deterministic no-op stub when no provider is reachable
so the pipeline stays usable offline.

End-to-end flow:
    plan_with_gaps
      → fill_gaps()                    # LLM synth per Gap → a1 block files
      → rescan BlockRegistry           # discover the new blocks
      → rewrite plan (gap:slug → id)   # swap stubs for real blocks
      → CompositionEngine.compile      # expect PASS now
      → materialize to disk
      → ContextLoaderWiringSpecialist  # patch any upward imports
      → GapFillReport

Important: by default the pipeline runs with ``allow_stub_fallback=True`` so
REFINE-verdict plans can always complete (the stub is a safe no-op function
the user can later improve). Set ``allow_stub_fallback=False`` to require
live LLM output and raise otherwise.
"""

from __future__ import annotations

import ast
import hashlib
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.tier_names import TIERS
from ass_ade.a2_mo_composites.block_registry import BlockRegistry
from ass_ade.a2_mo_composites.context_loader_wiring_specialist_core import (
    ContextLoaderWiringSpecialist,
)
from ass_ade.a3_og_features.composition_engine import (
    CompositionEngine,
    CompositionPlan,
    Gap,
)


_SYNTH_PROMPT = """You are synthesizing a Python function body to fill a gap in a composed feature.

Gap slug:     {slug}
Target tier:  {tier}
Hint:         {hint}

Constraints:
- Write ONE Python function named exactly `{slug}`.
- The function MUST accept a single `results: dict` argument and return a value.
- Use only the Python standard library (no third-party imports).
- No top-level side effects; pure logic inside the function.
- Include a concise one-line docstring.
- Return ONLY the function source code — no prose, no markdown fences.

Begin:
"""


@dataclass
class GapFill:
    """Record of one gap synthesis attempt."""
    slug: str
    tier: str
    source: str          # "llm" | "stub_fallback" | "error"
    block_id: str = ""   # id of the new block after rescan
    file: str = ""       # where the synthesized function lives
    error: str = ""


@dataclass
class GapFillReport:
    """End-to-end result of the gap-fill pipeline."""
    plan_name: str
    gaps_total: int
    gaps_filled: int
    gaps_stubbed: int
    gaps_failed: int
    fills: list[GapFill] = field(default_factory=list)
    materialized_path: str = ""
    wire_verdict: str = ""
    wire_auto_fixed: int = 0
    wire_not_fixable: int = 0
    final_verdict: str = "REFINE"
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "fills": [asdict(f) for f in self.fills],
        }


def _slugify_identifier(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_]+", "_", name.strip()).strip("_")
    return s or "unnamed_gap"


def _stub_body(slug: str, hint: str) -> str:
    """Safe no-op fallback when no LLM is available."""
    hint_text = (hint or "synthesis target").replace('"""', "'''")
    return (
        f"def {slug}(results: dict):\n"
        f'    """GAP fallback: {hint_text}"""\n'
        f"    return None\n"
    )


def _validate_synthesized(source: str, slug: str) -> bool:
    """Reject obvious bad outputs: must parse, must define ``slug``, no scary imports."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    defined = False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == slug:
            defined = True
        if isinstance(node, ast.Import):
            # Reject third-party at the top level of the snippet
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root not in _STDLIB_WHITELIST:
                    return False
        if isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            if root and root not in _STDLIB_WHITELIST:
                return False
    return defined


_STDLIB_WHITELIST = frozenset({
    "typing", "json", "math", "re", "dataclasses", "pathlib", "collections",
    "functools", "itertools", "datetime", "time", "os", "hashlib", "enum",
    "uuid", "logging", "textwrap", "io",
})


def _extract_code(raw: str) -> str:
    """Pull a python code block out of an LLM response; return raw if no fence."""
    fence = re.search(r"```(?:python|py)?\s*(.*?)\s*```", raw, re.DOTALL)
    return (fence.group(1) if fence else raw).strip()


def _synthesize_via_llm(gap: Gap) -> str | None:
    """Ask the configured provider for a function body. Returns source or None."""
    from ass_ade.config import load_config
    from ass_ade.engine.router import build_provider
    from ass_ade.engine.types import CompletionRequest, Message

    settings = load_config(None)
    provider = build_provider(settings)
    try:
        slug = _slugify_identifier(gap.slug)
        prompt = _SYNTH_PROMPT.format(
            slug=slug,
            tier=gap.expected_tier or "a1_at_functions",
            hint=gap.hint or "fill this gap with the minimal correct implementation",
        )
        response = provider.complete(
            CompletionRequest(
                messages=[
                    Message(role="system", content="Return ONLY Python code. No commentary."),
                    Message(role="user", content=prompt),
                ],
                model=settings.agent_model,
                temperature=0.1,
                max_tokens=600,
            )
        )
        raw = (response.message.content or "").strip()
        body = _extract_code(raw)
        if _validate_synthesized(body, slug):
            return body
        return None
    finally:
        close = getattr(provider, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass


def _write_synthesized_module(
    source_root: Path, tier: str, slug: str, body: str
) -> Path:
    """Write the gap function to <tier>/<slug>_gapfill.py and return the path."""
    if tier not in TIERS:
        tier = "a1_at_functions"
    target_dir = source_root / tier
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{_slugify_identifier(slug)}_gapfill"
    dest = target_dir / f"{stem}.py"
    header = (
        f'"""Tier {tier.split("_", 1)[0]} — synthesized by gap_fill_pipeline for `{slug}`."""\n\n'
        "from __future__ import annotations\n\n"
    )
    dest.write_text(header + body + ("\n" if not body.endswith("\n") else ""), encoding="utf-8")
    return dest


class GapFillPipeline:
    """End-to-end synth → compose → materialize → wire loop for a single plan."""

    def __init__(
        self,
        registry: BlockRegistry,
        *,
        allow_stub_fallback: bool = True,
        use_llm: bool = True,
    ) -> None:
        self._registry = registry
        self._allow_stub = allow_stub_fallback
        self._use_llm = use_llm

    def run(
        self,
        plan: CompositionPlan,
        *,
        target_root: Path | None = None,
    ) -> GapFillReport:
        root = (target_root or self._registry.source_dir).resolve()
        engine = CompositionEngine(self._registry)
        report = GapFillReport(
            plan_name=plan.name,
            gaps_total=len(plan.gaps),
            gaps_filled=0,
            gaps_stubbed=0,
            gaps_failed=0,
        )

        # Fill gaps first
        for gap in plan.gaps:
            fill = self._fill_gap(gap, root)
            report.fills.append(fill)
            if fill.source == "llm":
                report.gaps_filled += 1
            elif fill.source == "stub_fallback":
                report.gaps_stubbed += 1
            else:
                report.gaps_failed += 1
                report.errors.append(f"gap `{gap.slug}`: {fill.error}")

        # Rescan so the new blocks are visible
        self._registry.scan()

        # Rewrite gap node ids to point at the fresh blocks
        rewritten = self._rewrite_plan(plan)

        # Compile + materialize
        result = engine.compile(rewritten)
        if result.verdict == "REJECT":
            report.final_verdict = "REJECT"
            report.errors.extend(result.tier_violations)
            return report

        result = engine.materialize(result, root)
        report.materialized_path = result.target_path

        if not result.wrote_to_disk:
            report.final_verdict = "REJECT"
            report.errors.append("materialize did not write the composed module")
            return report

        # Wire any upward imports the new code introduced
        specialist = ContextLoaderWiringSpecialist()
        wire_report = specialist.wire(root)
        report.wire_verdict = wire_report.get("verdict", "")
        report.wire_auto_fixed = int(wire_report.get("auto_fixed") or 0)
        report.wire_not_fixable = int(wire_report.get("not_fixable") or 0)

        if report.gaps_failed:
            report.final_verdict = "REFINE"
        elif wire_report.get("not_fixable"):
            report.final_verdict = "REFINE"
        else:
            report.final_verdict = "PASS"
        return report

    # ── Internals ──────────────────────────────────────────────────────────

    def _fill_gap(self, gap: Gap, root: Path) -> GapFill:
        slug = _slugify_identifier(gap.slug)
        tier = gap.expected_tier or "a1_at_functions"

        body: str | None = None
        source = "llm"
        err = ""
        if self._use_llm:
            try:
                body = _synthesize_via_llm(gap)
                if body is None:
                    err = "LLM output failed validation"
            except Exception as exc:
                err = f"{type(exc).__name__}: {exc}"

        if body is None:
            if self._allow_stub:
                body = _stub_body(slug, gap.hint or "")
                source = "stub_fallback"
            else:
                return GapFill(slug=gap.slug, tier=tier, source="error", error=err or "no body")

        try:
            dest = _write_synthesized_module(root, tier, slug, body)
        except OSError as exc:
            return GapFill(slug=gap.slug, tier=tier, source="error", error=str(exc))

        # The new module's dotted path is keyed off the body hash via BlockRegistry.
        # We return the relative file path; the block_id is resolved after rescan.
        return GapFill(
            slug=gap.slug,
            tier=tier,
            source=source,
            file=str(dest.relative_to(root)).replace("\\", "/"),
        )

    def _rewrite_plan(self, plan: CompositionPlan) -> CompositionPlan:
        """Swap every ``gap:slug`` node id for the freshly-synthesized block id."""
        slug_to_block: dict[str, str] = {}
        for block in self._registry.all_blocks():
            if not block.module.endswith("_gapfill") and "_gapfill." not in block.module:
                continue
            # block.module looks like "<tier>.<slug>_gapfill"; block.name is the fn name
            slug_to_block[block.name] = block.id

        new_nodes = []
        for node in plan.nodes:
            if node.id.startswith("gap:"):
                slug = _slugify_identifier(node.id.split(":", 1)[1])
                new_id = slug_to_block.get(slug)
                if new_id:
                    from ass_ade.a3_og_features.composition_engine import CompositionNode
                    new_nodes.append(CompositionNode(id=new_id, alias=node.alias or slug))
                    continue
            new_nodes.append(node)

        new_edges = []
        for edge in plan.edges:
            src = edge.src
            dst = edge.dst
            if src.startswith("gap:"):
                slug = _slugify_identifier(src.split(":", 1)[1])
                src = slug_to_block.get(slug, src)
            if dst.startswith("gap:"):
                slug = _slugify_identifier(dst.split(":", 1)[1])
                dst = slug_to_block.get(slug, dst)
            from ass_ade.a3_og_features.composition_engine import CompositionEdge
            new_edges.append(CompositionEdge(src=src, dst=dst, port=edge.port))

        return CompositionPlan(
            name=plan.name,
            target_tier=plan.target_tier,
            nodes=new_nodes,
            edges=new_edges,
            gaps=[],  # all gaps are now real blocks
            description=plan.description,
        )
