"""Dispatch layer: map (language) -> Transpiler, and drive tree walks."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from ass_ade.engine.transpile.base import (
    TranspileError,
    TranspileResult,
    Transpiler,
)
from ass_ade.engine.transpile.detect import detect_language, is_transpile_target

_REGISTRY: dict[str, Callable[[], Transpiler]] = {}


def _register(language: str, factory: Callable[[], Transpiler]) -> None:
    _REGISTRY[language] = factory


def _build_registry() -> None:
    if _REGISTRY:
        return
    from ass_ade.engine.transpile.kotlin import KotlinTranspiler
    from ass_ade.engine.transpile.python import PythonTranspiler
    from ass_ade.engine.transpile.rust import RustTranspiler
    from ass_ade.engine.transpile.swift import SwiftTranspiler
    from ass_ade.engine.transpile.typescript import TypeScriptTranspiler

    _register("python", PythonTranspiler)
    _register("swift", SwiftTranspiler)
    _register("typescript", TypeScriptTranspiler)
    _register("javascript", TypeScriptTranspiler)
    _register("kotlin", KotlinTranspiler)
    _register("rust", RustTranspiler)


def get_transpiler(language: str) -> Transpiler:
    """Return a transpiler instance for ``language``.

    Raises :class:`TranspileError` if the language is unknown or the
    backing transpiler fails to import.
    """
    _build_registry()
    factory = _REGISTRY.get(language.lower())
    if factory is None:
        raise TranspileError(
            f"no transpiler registered for language={language!r}. "
            f"Supported: {sorted(_REGISTRY)}"
        )
    return factory()


def transpile_source(
    source: str,
    *,
    language: str,
    source_path: str | Path | None = None,
) -> TranspileResult:
    """Transpile an in-memory source string."""
    return get_transpiler(language).transpile_source(source, source_path=source_path)


def transpile_file(
    path: str | Path,
    *,
    output_path: str | Path | None = None,
    language: str | None = None,
) -> TranspileResult:
    """Transpile ``path`` and optionally write the Python output."""
    src_path = Path(path)
    lang = language or detect_language(src_path)
    if lang is None:
        raise TranspileError(
            f"cannot detect language for {src_path!s}; pass language= explicitly"
        )
    result = get_transpiler(lang).transpile_file(src_path)
    if output_path is not None:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result.python_code, encoding="utf-8")
    return result


def transpile_tree(
    root: str | Path,
    *,
    output_root: str | Path,
    languages: tuple[str, ...] | None = None,
    exclude: tuple[str, ...] = (
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        "dist",
        "build",
        ".git",
        ".ass-ade",
    ),
) -> dict[str, TranspileResult]:
    """Walk ``root`` and transpile every recognized source into ``output_root``.

    Returns a mapping of ``source_rel_path -> TranspileResult``. Skips paths
    whose any component is in ``exclude``. If ``languages`` is provided,
    only transpile files whose detected language is in the allowlist.
    """
    src_root = Path(root).resolve()
    dst_root = Path(output_root).resolve()
    if not src_root.exists():
        raise TranspileError(f"tree root does not exist: {src_root}")
    results: dict[str, TranspileResult] = {}
    lang_allow = {l.lower() for l in languages} if languages else None
    excluded = set(exclude)

    for p in src_root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in excluded for part in p.parts):
            continue
        if not is_transpile_target(p):
            continue
        lang = detect_language(p)
        if lang_allow is not None and lang not in lang_allow:
            continue
        rel = p.relative_to(src_root)
        out_rel = rel.with_suffix(".py")
        out_path = dst_root / out_rel
        try:
            result = transpile_file(p, output_path=out_path, language=lang)
        except TranspileError as exc:
            results[str(rel).replace("\\", "/")] = TranspileResult(
                source_language=lang or "unknown",
                source_path=str(p),
                python_code="",
                warnings=(f"TranspileError: {exc}",),
                backend="error",
            )
            continue
        results[str(rel).replace("\\", "/")] = result
    return results
