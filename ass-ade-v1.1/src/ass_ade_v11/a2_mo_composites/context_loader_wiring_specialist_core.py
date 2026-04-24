"""Tier a2 — stateful Context Loader & Wiring Specialist for monadic source trees.

Loads tier context from the source directory, scans for upward import violations
using the a1 scanner, and applies auto-fixable patches in-place.  The wire()
method is the primary entry point; it returns a structured wiring report.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ass_ade_v11.a0_qk_constants.tier_names import TIERS
from ass_ade_v11.a1_at_functions.import_violation_scanner import (
    ImportViolation,
    SymbolLocation,
    build_symbol_index,
    resolve_correct_import,
    scan_source_for_violations,
)


@dataclass
class WireRecord:
    """One import violation with an optional auto-fix patch."""

    file: str
    file_tier: str
    old_import: str
    new_import: str | None
    imported_tier: str
    reason: str
    lineno: int
    end_lineno: int
    auto_fixable: bool = field(init=False)

    def __post_init__(self) -> None:
        self.auto_fixable = self.new_import is not None


def _detect_package_name(source_dir: Path) -> str | None:
    """Infer the Python package name from pyproject.toml or directory name."""
    pyproject = source_dir / "pyproject.toml"
    if pyproject.is_file():
        try:
            for line in pyproject.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped.startswith("name") and "=" in stripped:
                    value = stripped.split("=", 1)[1].strip().strip("\"'")
                    if value:
                        return value.replace("-", "_")
        except OSError:
            pass
    name = source_dir.name
    return name if name.isidentifier() else None


class ContextLoaderWiringSpecialist:
    """Loads tier context and rewires upward imports across a monadic source tree.

    Usage::

        specialist = ContextLoaderWiringSpecialist()
        report = specialist.wire("/path/to/src/ass_ade_v11")

    The report dict contains:
      - violations_found  : total upward violations detected
      - auto_fixed        : number of import statements rewritten
      - files_changed     : number of files patched on disk
      - not_fixable       : count of violations needing manual review
      - changes           : {file: [{old, new}, ...]}
      - manual_review     : [{file, file_tier, import, reason}, ...]
      - verdict           : "PASS" | "REFINE"
    """

    def __init__(self, package_name: str | None = None) -> None:
        self._package_name = package_name
        self._context: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_context(self, source_dir: str | Path) -> dict[str, Any]:
        """Load tier map and source tree metadata; cache internally and return."""
        source_dir = Path(source_dir)

        tier_map: dict[str, Any] = {}
        tier_map_path = source_dir / ".ass-ade" / "tier-map.json"
        if tier_map_path.is_file():
            try:
                tier_map = json.loads(tier_map_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

        present_tiers = [t for t in TIERS if (source_dir / t).is_dir()]

        package_name = self._package_name or _detect_package_name(source_dir)

        self._context = {
            "source_dir": str(source_dir),
            "tier_map": tier_map,
            "present_tiers": present_tiers,
            "package_name": package_name,
        }
        return dict(self._context)

    def rewire_imports(self, source_dir: str | Path) -> list[WireRecord]:
        """Scan source_dir for tier violations; return WireRecords with patches where possible.

        Builds a symbol index so that symbols defined at a lower tier can be
        proposed as auto-fix replacements for upward import statements.
        """
        source_dir = Path(source_dir)
        ctx = self._context if self._context.get("source_dir") == str(source_dir) else None
        package_name = (ctx or {}).get("package_name") or self._package_name or _detect_package_name(source_dir)

        violations: list[ImportViolation] = scan_source_for_violations(source_dir)
        symbol_index: dict[str, list[SymbolLocation]] = build_symbol_index(
            source_dir,
            package_prefix=package_name,
        )

        records: list[WireRecord] = []
        for v in violations:
            new_import = resolve_correct_import(v, symbol_index)
            records.append(WireRecord(
                file=v.file,
                file_tier=v.file_tier,
                old_import=v.import_stmt,
                new_import=new_import,
                imported_tier=v.imported_tier,
                reason=v.reason,
                lineno=v.import_lineno,
                end_lineno=v.import_end_lineno,
            ))
        return records

    def wire(self, source_dir: str | Path) -> dict[str, Any]:
        """Full wiring cycle: extract context → detect violations → patch fixable ones.

        Applies patches in reverse line-number order per file so that earlier
        line numbers remain valid as later lines are rewritten.

        Returns a structured report dict.
        """
        source_dir = Path(source_dir)
        context = self.extract_context(source_dir)
        records = self.rewire_imports(source_dir)

        # Group fixable records by file; apply in reverse line order
        fixable_by_file: dict[str, list[WireRecord]] = {}
        not_fixable: list[dict[str, str | int]] = []

        for rec in records:
            if rec.auto_fixable:
                fixable_by_file.setdefault(rec.file, []).append(rec)
            else:
                not_fixable.append({
                    "file": rec.file,
                    "file_tier": rec.file_tier,
                    "import": rec.old_import,
                    "imported_tier": rec.imported_tier,
                    "reason": rec.reason,
                })

        changes: dict[str, list[dict[str, str]]] = {}
        for file_path, file_records in fixable_by_file.items():
            applied: list[dict[str, str]] = []
            for rec in sorted(file_records, key=lambda r: r.lineno, reverse=True):
                assert rec.new_import is not None
                ok = self._apply_patch(Path(file_path), rec.lineno, rec.end_lineno, rec.new_import)
                if ok:
                    applied.append({"old": rec.old_import, "new": rec.new_import})
            if applied:
                changes[file_path] = applied

        total_auto_fixed = sum(len(v) for v in changes.values())
        verdict = "PASS" if not not_fixable else "REFINE"

        return {
            "source_dir": str(source_dir),
            "context": context,
            "violations_found": len(records),
            "auto_fixed": total_auto_fixed,
            "not_fixable": len(not_fixable),
            "files_changed": len(changes),
            "changes": changes,
            "manual_review": not_fixable,
            "verdict": verdict,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _apply_patch(py_file: Path, lineno: int, end_lineno: int, new_import: str) -> bool:
        """Replace lines lineno..end_lineno (1-based, inclusive) with new_import.

        Returns True on success, False if the file could not be read/written.
        Line numbers come from the AST parser so they are always valid.
        Patches are applied in reverse order by callers so indices stay stable.
        """
        try:
            content = py_file.read_text(encoding="utf-8")
        except OSError:
            return False
        lines = content.splitlines(keepends=True)
        if lineno < 1 or end_lineno > len(lines):
            return False
        new_line = new_import.rstrip("\n") + "\n"
        patched = lines[: lineno - 1] + [new_line] + lines[end_lineno:]
        try:
            py_file.write_text("".join(patched), encoding="utf-8")
        except OSError:
            return False
        return True
