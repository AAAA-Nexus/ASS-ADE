"""Tier a3 — Hot-Patch Runtime.

After the gap-fill pipeline materializes a new feature, you want the live
Atomadic session to pick it up without restarting. This module does that
safely:

  1. Map a newly-written file path to its dotted Python module name.
  2. If the module is already in ``sys.modules``, ``importlib.reload`` it.
  3. If not, ``importlib.import_module`` it.
  4. Refuse to touch load-bearing modules that would crash the running
     interpreter (``ass_ade.interpreter``, ``ass_ade.cli``, uvicorn, etc.).
  5. Return a structured report the dashboard renders as a card.

Safety posture: hot-patch is opt-in. The default path of the gap-fill
pipeline does NOT call this — the user must explicitly hit /playground/
hot-patch or run ``@patch``. If anything goes wrong mid-reload the error
is caught and returned; the original module stays in sys.modules.
"""

from __future__ import annotations

import importlib
import sys
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path


# Modules that are structurally important to keep loaded "as-is" during a
# running REPL session. Reloading these risks dangling references.
_BLOCKLIST: frozenset[str] = frozenset({
    "ass_ade.interpreter",
    "ass_ade.cli",
    "ass_ade.a3_og_features.ag_ui_server",
    "ass_ade.a3_og_features.hot_patch_runtime",
    "ass_ade.a3_og_features.gap_fill_pipeline",
    "ass_ade.a2_mo_composites.ag_ui_bus",
    "ass_ade.commands.ui",
    "uvicorn",
    "fastapi",
})


@dataclass
class ModuleReloadResult:
    module: str
    status: str                # reloaded | imported | skipped_blocked | error | not_found
    path: str = ""
    error: str = ""


@dataclass
class HotPatchReport:
    root: str
    requested_paths: list[str]
    resolved_modules: list[str]
    results: list[ModuleReloadResult] = field(default_factory=list)
    verdict: str = "PASS"      # PASS | REFINE | REJECT

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "results": [asdict(r) for r in self.results],
        }


def _find_package_root(path: Path) -> Path | None:
    """Walk up from ``path`` until we stop seeing ``__init__.py``.

    The package root is the highest directory that *does* contain an
    ``__init__.py`` — the one above it is the import search path.
    """
    current = path.parent
    last_with_init: Path | None = None
    while current != current.parent:
        if (current / "__init__.py").exists():
            last_with_init = current
            current = current.parent
        else:
            break
    return last_with_init


def module_for_path(file_path: Path) -> str | None:
    """Return the dotted module name for a Python file under a package root."""
    file_path = file_path.resolve()
    if not file_path.is_file() or file_path.suffix != ".py":
        return None
    pkg_root = _find_package_root(file_path)
    if pkg_root is None:
        return None
    search_path = pkg_root.parent
    try:
        rel = file_path.relative_to(search_path)
    except ValueError:
        return None
    parts = list(rel.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts) if parts else None


def _ensure_search_path(pkg_parent: Path) -> None:
    """Make sure ``pkg_parent`` is on sys.path so import_module works."""
    s = str(pkg_parent)
    if s not in sys.path:
        sys.path.insert(0, s)


def reload_module(module_name: str) -> ModuleReloadResult:
    """Reload or import a single module by dotted name."""
    if module_name in _BLOCKLIST:
        return ModuleReloadResult(
            module=module_name, status="skipped_blocked",
            error="load-bearing module — refused to reload to protect the live session",
        )
    try:
        existing = sys.modules.get(module_name)
        if existing is not None:
            reloaded = importlib.reload(existing)
            return ModuleReloadResult(
                module=module_name, status="reloaded",
                path=getattr(reloaded, "__file__", "") or "",
            )
        mod = importlib.import_module(module_name)
        return ModuleReloadResult(
            module=module_name, status="imported",
            path=getattr(mod, "__file__", "") or "",
        )
    except Exception as exc:
        return ModuleReloadResult(
            module=module_name, status="error",
            error=f"{type(exc).__name__}: {exc}",
        )


def hot_patch(paths: list[Path], root: Path | None = None) -> HotPatchReport:
    """Reload / import every module corresponding to the given file paths.

    ``paths`` can be absolute or relative to ``root``. Unknown or non-Python
    paths are surfaced as ``not_found`` results without raising.
    """
    resolved_root = (root or Path.cwd()).resolve()
    resolved_paths: list[Path] = []
    for p in paths:
        path = p if p.is_absolute() else (resolved_root / p)
        resolved_paths.append(path.resolve())

    report = HotPatchReport(
        root=str(resolved_root),
        requested_paths=[str(p) for p in resolved_paths],
        resolved_modules=[],
    )
    errors = 0
    blocked = 0

    for path in resolved_paths:
        mod_name = module_for_path(path)
        if mod_name is None:
            report.results.append(ModuleReloadResult(
                module="", status="not_found", path=str(path),
                error="could not map to a Python module",
            ))
            errors += 1
            continue
        report.resolved_modules.append(mod_name)

        pkg_root = _find_package_root(path)
        if pkg_root is not None:
            _ensure_search_path(pkg_root.parent)

        result = reload_module(mod_name)
        result.path = result.path or str(path)
        report.results.append(result)
        if result.status == "error":
            errors += 1
        elif result.status == "skipped_blocked":
            blocked += 1

    if errors and any(r.status in {"reloaded", "imported"} for r in report.results):
        report.verdict = "REFINE"
    elif errors:
        report.verdict = "REJECT"
    elif blocked and not any(r.status in {"reloaded", "imported"} for r in report.results):
        report.verdict = "REJECT"
    else:
        report.verdict = "PASS"
    return report
