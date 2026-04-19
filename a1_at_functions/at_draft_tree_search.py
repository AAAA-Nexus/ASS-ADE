# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_tree_search.py:7
# Component id: at.source.a1_at_functions.tree_search
from __future__ import annotations

__version__ = "0.1.0"

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
