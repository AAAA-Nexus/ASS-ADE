# Extracted from C:/!ass-ade/src/ass_ade/agent/alphaverus.py:165
# Component id: mo.source.ass_ade.alphaverus
from __future__ import annotations

__version__ = "0.1.0"

class AlphaVerus:
    DEFAULT_WIDTH = 4
    DEFAULT_DEPTH = 3

    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        cfg = config.get("alphaverus") or {}
        self._budget = int(cfg.get("exploration_budget", 10))
        self._width = int(cfg.get("beam_width", self.DEFAULT_WIDTH))
        self._depth = int(cfg.get("beam_depth", self.DEFAULT_DEPTH))
        self._log: list[dict] = []

    # ── public verify kept for back-compat ──────────────────────────────────
    def verify(self, code: str, spec: str) -> bool:
        if self._nexus is not None and hasattr(self._nexus, "certify_output_verify"):
            try:
                result = self._nexus.certify_output_verify(code)
                verdict = getattr(result, "rubric_passed", None)
                if verdict is not None:
                    return bool(verdict)
            except Exception:
                pass
        metrics = _score(code, spec)
        return _passes(metrics)

    # ── Mutation operators ──────────────────────────────────────────────────
    @staticmethod
    def _mutations(code: str) -> list[tuple[str, str]]:
        """Return (label, mutated_code) pairs. Cheap, deterministic."""
        out: list[tuple[str, str]] = []
        # Identity (no-op) variant — keeps the beam anchored.
        out.append(("identity", code))
        # Add a docstring if missing.
        if '"""' not in code and "'''" not in code:
            lines = code.splitlines()
            for i, ln in enumerate(lines):
                if ln.lstrip().startswith("def ") and ln.rstrip().endswith(":"):
                    indent = " " * (len(ln) - len(ln.lstrip()) + 4)
                    lines.insert(i + 1, f'{indent}"""Auto-synthesized docstring."""')
                    break
            out.append(("docstring", "\n".join(lines)))
        # Guard against None if there is a parameter.
        if "def " in code and "is None" not in code:
            m = re.search(r"def\s+\w+\s*\(\s*([A-Za-z_]\w*)", code)
            if m:
                param = m.group(1)
                guard = f"\n    if {param} is None:\n        return None"
                mutated = re.sub(
                    r"(def\s+\w+\s*\([^)]*\)\s*:)",
                    r"\1" + guard,
                    code,
                    count=1,
                )
                out.append(("none_guard", mutated))
        # Trailing type-hint free comment.
        out.append(("annotate", code + "\n# verified: alphaverus\n"))
        return out

    # ── Tree search ─────────────────────────────────────────────────────────
    def tree_search(
        self,
        code: str,
        spec: str,
        *,
        code_path: Optional[Path] = None,
    ) -> Optional[VerifiedCode]:
        """Beam search for a verified variant. Returns None if none pass."""
        root_metrics = _score(code, spec, code_path)
        root = VerifiedCode(
            code=code,
            verified=_passes(root_metrics),
            score=root_metrics["score"],
            trace=["root"],
            metrics=root_metrics,
        )
        self._log.append({"step": "root", **root_metrics})

        # Beam of (VerifiedCode, trace_labels).
        beam: list[VerifiedCode] = [root]
        best_passing: Optional[VerifiedCode] = root if root.verified else None

        steps_used = 0
        for depth in range(self._depth):
            candidates: list[VerifiedCode] = []
            for node in beam:
                for label, variant in self._mutations(node.code):
                    if steps_used >= self._budget:
                        break
                    metrics = _score(variant, spec, code_path)
                    ok = _passes(metrics)
                    vc = VerifiedCode(
                        code=variant,
                        verified=ok,
                        score=metrics["score"],
                        trace=node.trace + [f"d{depth}:{label}"],
                        metrics=metrics,
                    )
                    candidates.append(vc)
                    self._log.append({
                        "step": steps_used,
                        "depth": depth,
                        "label": label,
                        "verified": ok,
                        **metrics,
                    })
                    steps_used += 1
                    if ok and (best_passing is None or vc.score > best_passing.score):
                        best_passing = vc
                if steps_used >= self._budget:
                    break
            if not candidates:
                break
            # Keep top-N by score for next depth.
            candidates.sort(key=lambda v: v.score, reverse=True)
            beam = candidates[: self._width]
            if steps_used >= self._budget:
                break

        return best_passing

    def run(self, ctx: dict) -> dict:
        code = ctx.get("code", "")
        spec = ctx.get("spec", "")
        result = self.tree_search(code, spec)
        if result is None:
            return {"code": code, "verified": False, "score": 0.0, "trace": [], "passed": False}
        return {
            "code": result.code,
            "verified": result.verified,
            "score": result.score,
            "trace": result.trace,
            "passed": True,
        }

    def report(self) -> dict:
        return {
            "engine": "alphaverus",
            "budget": self._budget,
            "width": self._width,
            "depth": self._depth,
            "iterations": len(self._log),
            "last": self._log[-1] if self._log else None,
        }
