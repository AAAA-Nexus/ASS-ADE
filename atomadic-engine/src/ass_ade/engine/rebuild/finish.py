"""Stub detector + in-place completer (Cap-B).

Scans a Python codebase for "incomplete" function/method bodies — defined
as bodies that are only ``pass``, ``...``, ``raise NotImplementedError``,
``return None``, or contain only a ``TODO``/``FIXME`` comment — and
completes them via the AAAA-Nexus refinement loop.

Produces deterministic patches that preserve signatures, decorators, and
surrounding formatting. Patches are written to ``.ass-ade/patches/``
alongside a receipt; the user applies them with ``--apply`` or by hand.
"""

from __future__ import annotations

import ast
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ass_ade.engine.rebuild.synthesis import (
    DEFAULT_BASE_URL,
    _cie_gate,
    _synthesize_via_nexus,
)


@dataclass(frozen=True)
class IncompleteFunction:
    path: Path
    qualname: str
    lineno: int
    end_lineno: int
    col_offset: int
    signature: str
    docstring: str | None
    reason: str  # "pass" | "ellipsis" | "not_implemented" | "todo_only" | "return_none_only"


# ── detection ──────────────────────────────────────────────────────────────


def _body_is_stub(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    body = list(node.body)
    # Strip leading docstring, if any.
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    if not body:
        return "pass"
    if len(body) == 1:
        stmt = body[0]
        if isinstance(stmt, ast.Pass):
            return "pass"
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
            return "ellipsis"
        if isinstance(stmt, ast.Raise) and isinstance(stmt.exc, (ast.Call, ast.Name)):
            name = _raised_name(stmt.exc)
            if name == "NotImplementedError":
                return "not_implemented"
        if isinstance(stmt, ast.Return):
            if stmt.value is None or (
                isinstance(stmt.value, ast.Constant) and stmt.value.value is None
            ):
                return "return_none_only"
    return None


def _raised_name(exc: ast.AST) -> str | None:
    if isinstance(exc, ast.Name):
        return exc.id
    if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name):
        return exc.func.id
    return None


def _signature(source: str, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    # Take the def-line through the colon.
    start = node.lineno - 1
    lines = source.splitlines()
    buf: list[str] = []
    for i in range(start, min(start + 10, len(lines))):
        buf.append(lines[i])
        if lines[i].rstrip().endswith(":"):
            break
    return "\n".join(buf)


def _docstring(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    return ast.get_docstring(node)


def scan_file(path: Path) -> list[IncompleteFunction]:
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    results: list[IncompleteFunction] = []

    def visit(node: ast.AST, stack: list[str]) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fqn = stack + [child.name]
                reason = _body_is_stub(child)
                if reason is not None:
                    results.append(
                        IncompleteFunction(
                            path=path,
                            qualname=".".join(fqn),
                            lineno=child.lineno,
                            end_lineno=child.end_lineno or child.lineno,
                            col_offset=child.col_offset,
                            signature=_signature(source, child),
                            docstring=_docstring(child),
                            reason=reason,
                        )
                    )
                visit(child, fqn)
            elif isinstance(child, ast.ClassDef):
                visit(child, stack + [child.name])
            else:
                visit(child, stack)

    visit(tree, [])
    return results


def scan_path(root: Path) -> list[IncompleteFunction]:
    incomplete: list[IncompleteFunction] = []
    if root.is_file() and root.suffix == ".py":
        return scan_file(root)
    for py in sorted(root.rglob("*.py")):
        # Skip test and build artifacts.
        parts = set(py.parts)
        if parts & {"__pycache__", ".venv", "venv", "build", "dist", ".ass-ade"}:
            continue
        incomplete.extend(scan_file(py))
    return incomplete


# ── completion ─────────────────────────────────────────────────────────────


def _indent_body(body: str, indent: str) -> str:
    lines = body.splitlines() or [""]
    return "\n".join(f"{indent}{line}" if line.strip() else line for line in lines)


def _apply_body(source: str, fn: IncompleteFunction, new_body: str) -> str:
    """Return the source with ``fn``'s body replaced by ``new_body``.

    Preserves the def-line(s), decorators, and trailing blank lines.
    """
    lines = source.splitlines(keepends=True)
    # def-line runs from fn.lineno to the first line ending with ':'.
    def_end = fn.lineno - 1
    for i in range(fn.lineno - 1, min(fn.lineno + 20, len(lines))):
        if lines[i].rstrip().endswith(":"):
            def_end = i
            break
    # Determine body indent: def-line indent + 4 spaces.
    def_indent = lines[fn.lineno - 1][: len(lines[fn.lineno - 1]) - len(lines[fn.lineno - 1].lstrip())]
    body_indent = def_indent + "    "
    # End of original body = fn.end_lineno.
    end = fn.end_lineno
    before = "".join(lines[: def_end + 1])
    after = "".join(lines[end:])
    indented = _indent_body(new_body.rstrip(), body_indent) + "\n"
    return before + indented + after


def complete_function(
    fn: IncompleteFunction,
    *,
    base_url: str,
    api_key: str | None,
    agent_id: str | None,
    max_refinement_attempts: int = 3,
) -> tuple[str | None, list[dict[str, Any]]]:
    context_parts = [
        f"File: {fn.path.name}",
        f"Function: {fn.qualname}",
        f"Reason for completion: {fn.reason}",
        f"Signature:\n{fn.signature}",
    ]
    if fn.docstring:
        context_parts.append(f"Docstring:\n{fn.docstring}")
    context = "\n\n".join(context_parts)

    attempts: list[dict[str, Any]] = []
    feedback: str | None = None
    for attempt in range(1, max(1, max_refinement_attempts) + 1):
        candidate = _synthesize_via_nexus(
            component_id=fn.qualname,
            tier="a2_mo_composites",
            blueprint_id=f"finish:{fn.path.name}",
            context=context,
            base_url=base_url,
            api_key=api_key,
            agent_id=agent_id,
            language="python",
            adapter_id=None,
            feedback=feedback,
        )
        if candidate is None:
            attempts.append({"attempt": attempt, "status": "no_response"})
            break
        # Strip a leading markdown fence if the model ignored instructions.
        candidate = _strip_code_fence(candidate)
        # Accept only the *body* (not a redefinition of the function).
        body_only = _extract_body_only(candidate, fn.qualname.split(".")[-1])
        target = body_only or candidate
        probe = "def _probe():\n    pass\n\n" + (target if _looks_like_body(target) else candidate)
        ok, findings = _cie_gate(probe, "python")
        attempts.append({
            "attempt": attempt,
            "status": "passed" if ok else "cie_rejected",
            "findings": findings,
        })
        if ok:
            return target, attempts
        feedback = "; ".join(findings)
    return None, attempts


def _strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        # Remove the opening fence line.
        nl = stripped.find("\n")
        if nl != -1:
            stripped = stripped[nl + 1 :]
        if stripped.endswith("```"):
            stripped = stripped[: -3]
    return stripped.strip("\n")


def _extract_body_only(text: str, fn_name: str) -> str | None:
    """If the model returned a full `def fn(...):` block, extract just its body."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == fn_name:
            body_source_lines = text.splitlines()
            # body starts at node.body[0].lineno
            if not node.body:
                return None
            start = node.body[0].lineno - 1
            end = (node.body[-1].end_lineno or node.body[-1].lineno)
            body_slice = "\n".join(body_source_lines[start:end])
            # De-indent by the minimum leading whitespace of non-blank lines.
            non_blank = [ln for ln in body_slice.splitlines() if ln.strip()]
            if not non_blank:
                return None
            indent = min(len(ln) - len(ln.lstrip()) for ln in non_blank)
            return "\n".join(ln[indent:] if len(ln) >= indent else ln for ln in body_slice.splitlines())
    return None


def _looks_like_body(text: str) -> bool:
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False


# ── orchestration ──────────────────────────────────────────────────────────


def finish_project(
    root: Path,
    *,
    base_url: str = DEFAULT_BASE_URL,
    api_key: str | None = None,
    agent_id: str | None = None,
    out_dir: Path | None = None,
    apply_in_place: bool = False,
    max_refinement_attempts: int = 3,
    max_functions: int = 100,
) -> dict[str, Any]:
    api_key = api_key or os.environ.get("AAAA_NEXUS_API_KEY")
    agent_id = agent_id or os.environ.get("AAAA_NEXUS_AGENT_ID")

    targets = scan_path(root)[:max_functions]
    completed: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    refinement_trace: list[dict[str, Any]] = []

    out_dir = out_dir or (root / ".ass-ade" / "patches")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Group by file so we can apply multiple patches per file consistently.
    by_file: dict[Path, list[IncompleteFunction]] = {}
    for fn in targets:
        by_file.setdefault(fn.path, []).append(fn)

    for path, fns in by_file.items():
        try:
            original = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            rejected.append({"path": str(path), "reason": f"unreadable: {exc}"})
            continue
        patched = original
        # Process bottom-up so line numbers remain valid.
        for fn in sorted(fns, key=lambda f: -f.lineno):
            body, attempts = complete_function(
                fn,
                base_url=base_url,
                api_key=api_key,
                agent_id=agent_id,
                max_refinement_attempts=max_refinement_attempts,
            )
            refinement_trace.append({
                "path": str(path), "qualname": fn.qualname, "attempts": attempts,
            })
            if body is None:
                rejected.append({
                    "path": str(path),
                    "qualname": fn.qualname,
                    "reason": "refinement_exhausted",
                })
                continue
            patched = _apply_body(patched, fn, body)
            completed.append({
                "path": str(path),
                "qualname": fn.qualname,
                "reason": fn.reason,
            })

        if patched != original:
            patch_file = out_dir / (path.stem + path.suffix + ".patched")
            patch_file.write_text(patched, encoding="utf-8")
            if apply_in_place:
                path.write_text(patched, encoding="utf-8")

    receipt = {
        "schema": "ASSADE-FINISH-001",
        "root": str(root),
        "scanned_functions": len(targets),
        "completed_count": len(completed),
        "rejected_count": len(rejected),
        "applied_in_place": apply_in_place,
        "out_dir": str(out_dir),
        "completed": completed,
        "rejected": rejected,
        "refinement_trace": refinement_trace,
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "finish_receipt.json").write_text(
        json.dumps(receipt, indent=2), encoding="utf-8"
    )
    return receipt
