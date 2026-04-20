"""v18 pillar 76 — AlphaVerus tree search for verified code variants.

Real implementation: beam search (width=4, depth=3) over code mutations.
Each node is scored on AST validity, cyclomatic complexity, OWASP hit
count, semantic distance vs spec, and an optional adjacent-pytest run.

A candidate passes verification iff:
    ast_valid AND cc <= 7 AND owasp_hits == 0 AND score > 0
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


# ── OWASP pattern set ───────────────────────────────────────────────────────
_OWASP_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p) for p in (
        r"\beval\s*\(",
        r"\bexec\s*\(",
        r"\bpickle\.loads?\s*\(",
        r"subprocess\.\w+\([^)]*shell\s*=\s*True",
        r"\bos\.system\s*\(",
        # SQL concat / fstring injection heuristics.
        r"SELECT.*\+\s*\w+",
        r"f\"SELECT.*\{",
        r"\.format\(.*\).*(SELECT|INSERT|UPDATE|DELETE)",
        # yaml.load without Loader=.
        r"yaml\.load\s*\([^)]*\)(?!.*Loader)",
        # Weak hashes used for security.
        r"hashlib\.md5\s*\(",
        r"hashlib\.sha1\s*\(",
    )
)

_WEAK_RNG = re.compile(r"random\.")
_AUTH_CTX = re.compile(r"\b(auth|token|key|password|secret|nonce|salt)\b", re.IGNORECASE)


@dataclass
class VerifiedCode:
    code: str
    verified: bool
    score: float
    trace: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


# ── Scoring helpers ─────────────────────────────────────────────────────────

def _ast_parses(code: str) -> bool:
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    return True


def _cyclomatic_complexity(code: str) -> int:
    # Prefer radon when available; fall back to AST walk.
    try:
        from radon.complexity import cc_visit  # type: ignore

        blocks = cc_visit(code)
        if blocks:
            return max(int(b.complexity) for b in blocks)
    except Exception:
        pass
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 999
    count = 1
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
            count += 1
        elif isinstance(node, ast.BoolOp):
            count += max(0, len(node.values) - 1)
    return count


def _owasp_regex_scan(code: str) -> int:
    hits = 0
    for pat in _OWASP_PATTERNS:
        if pat.search(code):
            hits += 1
    # Weak RNG in auth/token/key/password context.
    if _WEAK_RNG.search(code) and _AUTH_CTX.search(code):
        hits += 1
    return hits


def _tokenize(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text or "") if len(t) > 1}


def _semantic_distance(spec: str, code: str) -> float:
    s = _tokenize(spec)
    c = _tokenize(code)
    if not s and not c:
        return 0.0
    return len(s ^ c) / max(1, len(s | c))


def _run_pytest_if_exists(code_path: Optional[Path]) -> bool:
    if code_path is None:
        return False
    try:
        code_path = Path(code_path)
        adjacent = code_path.parent / f"test_{code_path.stem}.py"
        if not adjacent.exists():
            return False
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", str(adjacent)],
            capture_output=True,
            timeout=20,
            cwd=str(code_path.parent),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        return proc.returncode == 0
    except Exception:
        return False


def _score(code: str, spec: str, code_path: Optional[Path] = None) -> dict[str, Any]:
    ast_valid = _ast_parses(code)
    cc = _cyclomatic_complexity(code) if ast_valid else 999
    owasp_hits = _owasp_regex_scan(code)
    semantic_dist = _semantic_distance(spec, code)
    pytest_adjacent = _run_pytest_if_exists(code_path)
    score = (
        (10 if ast_valid else 0)
        - 2 * cc
        - 5 * owasp_hits
        - 0.1 * semantic_dist
        + (5 if pytest_adjacent else 0)
    )
    return {
        "cc": cc,
        "owasp": owasp_hits,
        "valid": ast_valid,
        "sem": semantic_dist,
        "pytest": pytest_adjacent,
        "score": float(score),
    }


def _passes(metrics: dict[str, Any]) -> bool:
    return bool(
        metrics.get("valid")
        and int(metrics.get("cc", 999)) <= 7
        and int(metrics.get("owasp", 1)) == 0
        and float(metrics.get("score", 0.0)) > 0.0
    )


# ── Beam search ─────────────────────────────────────────────────────────────

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
