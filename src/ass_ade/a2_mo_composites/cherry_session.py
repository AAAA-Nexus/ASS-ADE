"""Tier a2 — stateful cherry-pick session: load candidates, present menu, collect selection, save manifest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.cherry_types import CherryItemDict, CherryManifestDict
from ass_ade.a1_at_functions.cherry_helpers import (
    filter_by_actions,
    format_menu_header,
    format_menu_row,
    parse_selection,
    rank_candidates,
)

_SCHEMA = "ass-ade.cherry-pick/v1"
_DEFAULT_ACTIONS = frozenset({"assimilate", "rebuild", "enhance"})


class CherryPickSession:
    """Load a scout report or scan a repo directly, present ranked candidates, and save a manifest."""

    def __init__(self, source: str | Path, target_root: str | Path) -> None:
        self.source = Path(source).resolve()
        self.target_root = Path(target_root).resolve()
        self._report: dict[str, Any] | None = None
        self._candidates: list[CherryItemDict] = []

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_report(self) -> dict[str, Any]:
        """Load and cache the source (scout JSON or direct symbol scan)."""
        if self._report is not None:
            return self._report

        if self.source.is_file() and self.source.suffix == ".json":
            report = json.loads(self.source.read_text(encoding="utf-8"))
            # If the scout JSON has no Python symbols but names a real repo dir,
            # transparently add a TypeScript scan into the target_map.
            repo_dir = Path(report.get("repo", ""))
            target_map = report.get("target_map") or {}
            targets = target_map.get("targets") or []
            if not targets and repo_dir.is_dir():
                ts_targets = self._scan_typescript(repo_dir)
                if ts_targets:
                    report["target_map"] = {
                        "targets": ts_targets,
                        "action_counts": {
                            "assimilate": len(ts_targets),
                            "rebuild": 0,
                            "enhance": 0,
                            "skip": 0,
                        },
                    }
            self._report = report
        elif self.source.is_dir():
            # Direct scan mode — no scout JSON needed
            self._report = self._scan_direct(self.source)
        else:
            raise ValueError(f"source must be a scout JSON file or a directory: {self.source}")
        return self._report

    def load_candidates(
        self, actions: set[str] | None = None
    ) -> list[CherryItemDict]:
        """Return ranked candidates from the loaded report, filtered by action set."""
        report = self.load_report()
        target_map = report.get("target_map")
        if isinstance(target_map, dict):
            raw_targets = target_map.get("targets") or []
        else:
            # Fallback: build targets from symbol_summary
            raw_targets = self._symbols_as_targets(report)

        effective_actions = set(actions) if actions else set(_DEFAULT_ACTIONS)
        ranked = rank_candidates(list(raw_targets))
        self._candidates = filter_by_actions(ranked, effective_actions)
        return self._candidates

    # ------------------------------------------------------------------
    # Presentation
    # ------------------------------------------------------------------

    def present_menu(self, items: list[CherryItemDict] | None = None) -> None:
        """Print a numbered ranked menu of candidates to stdout."""
        candidates = items if items is not None else self._candidates
        if not candidates:
            print("(no candidates found)")
            return
        print(f"\n{'─' * 100}")
        print(f"  ASS-ADE Cherry Pick — {len(candidates)} candidates from {self.source.name}")
        print(f"{'─' * 100}")
        print(format_menu_header())
        print("─" * 100)
        for item in candidates:
            print(format_menu_row(item))
        print(f"{'─' * 100}")
        print("  Actions: assimilate = copy directly  |  rebuild = needs tier-safe rewrite  |  enhance = augment existing")
        print("  Enter item numbers (e.g. 1,3,5-8) or 'all' or action filter (e.g. 'assimilate'):")

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def collect_selection(self, raw: str) -> list[CherryItemDict]:
        """Parse a selection string and return the matching items.

        Supports:
          "all"         → everything currently in candidates
          "assimilate"  → only assimilate-action items
          "rebuild"     → only rebuild-action items
          "enhance"     → only enhance-action items
          "1,3,5-8"     → explicit 1-based indices
        """
        raw = raw.strip().lower()
        if raw in ("assimilate", "rebuild", "enhance"):
            return [i for i in self._candidates if i["action"] == raw]
        indices = parse_selection(raw, len(self._candidates))
        by_index = {item["index"]: item for item in self._candidates}
        return [by_index[idx] for idx in indices if idx in by_index]

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_manifest(
        self,
        items: list[CherryItemDict],
        out_path: str | Path | None = None,
    ) -> Path:
        """Write a CherryManifestDict to disk and return the path."""
        if out_path is None:
            out_dir = self.target_root / ".ass-ade"
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / "cherry_pick.json"

        manifest: CherryManifestDict = {
            "schema_version": _SCHEMA,
            "source_label": str(self.source),
            "source_root": str(
                self._report.get("repo", str(self.source)) if self._report else str(self.source)
            ),
            "target_root": str(self.target_root),
            "selected_count": len(items),
            "items": items,
        }
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return path

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _scan_direct(self, root: Path) -> dict[str, Any]:
        """Scan a bare directory: Python via AST, TypeScript via regex, whichever has symbols."""
        from ass_ade.a1_at_functions.assimilation_target_map import scan_symbols

        py_summary, py_symbols = scan_symbols(root)
        targets: list[dict[str, Any]] = [
            {
                "action": "assimilate",
                "symbol": {
                    "root": sym.root,
                    "rel_path": sym.rel_path,
                    "module": sym.module,
                    "qualname": sym.qualname,
                    "kind": sym.kind,
                    "lineno": sym.lineno,
                    "end_lineno": sym.end_lineno,
                    "signature": sym.signature,
                    "body_sha256": sym.body_sha256,
                    "docstring_present": sym.docstring_present,
                    "decorators": list(sym.decorators),
                    "imports": list(sym.imports),
                    "has_nearby_test": sym.has_nearby_test,
                    "language": "python",
                },
                "matched_primary": None,
                "confidence": 0.75 if sym.has_nearby_test else 0.55,
                "reasons": ["direct-scan candidate (python)"],
                "recommended_path": f"direct-scan from {sym.rel_path}",
            }
            for sym in py_symbols
            if not sym.qualname.startswith("_")
        ]

        # TypeScript fallback: when no Python symbols found, scan .ts/.tsx files
        if not targets:
            targets = self._scan_typescript(root)

        return {
            "schema_version": "ass-ade.scout/direct-scan",
            "repo": str(root),
            "target_map": {
                "targets": targets,
                "action_counts": {"assimilate": len(targets), "rebuild": 0, "enhance": 0, "skip": 0},
            },
        }

    def _scan_typescript(self, root: Path) -> list[dict[str, Any]]:
        """Scan TypeScript files and return candidate target dicts."""
        from ass_ade.a1_at_functions.ts_symbol_scanner import scan_ts_symbols

        _summary, ts_symbols = scan_ts_symbols(root)
        return [
            {
                "action": "assimilate",
                "symbol": {
                    "root": sym.root,
                    "rel_path": sym.rel_path,
                    "module": sym.module,
                    "qualname": sym.qualname,
                    "kind": sym.kind,
                    "lineno": sym.lineno,
                    "end_lineno": sym.end_lineno,
                    "signature": sym.signature,
                    "body_sha256": sym.body_sha256,
                    "docstring_present": sym.docstring_present,
                    "decorators": [],
                    "imports": [],
                    "has_nearby_test": sym.has_nearby_test,
                    "language": "typescript",
                },
                "matched_primary": None,
                "confidence": (
                    0.80 if sym.docstring_present and sym.has_nearby_test
                    else 0.65 if sym.docstring_present
                    else 0.50
                ),
                "reasons": [f"direct-scan candidate (typescript/{sym.kind})"],
                "recommended_path": f"direct-scan from {sym.rel_path}:{sym.lineno}",
            }
            for sym in ts_symbols
        ]

    def _symbols_as_targets(self, report: dict[str, Any]) -> list[dict[str, Any]]:
        """Build minimal target dicts from symbol_summary when target_map is absent."""
        symbol_summary = report.get("symbol_summary") or {}
        sample_modules = symbol_summary.get("sample_modules") or []
        repo_root = report.get("repo", "")
        targets: list[dict[str, Any]] = []
        for mod in sample_modules:
            rel = mod.get("path", "")
            for fn_name in (mod.get("functions") or []):
                targets.append(
                    {
                        "action": "assimilate",
                        "symbol": {
                            "root": repo_root,
                            "rel_path": rel,
                            "module": rel.replace("/", ".").removesuffix(".py"),
                            "qualname": fn_name,
                            "kind": "function",
                            "lineno": 0,
                            "end_lineno": 0,
                            "signature": "()",
                            "body_sha256": "",
                            "docstring_present": False,
                            "decorators": [],
                            "imports": [],
                            "has_nearby_test": False,
                        },
                        "matched_primary": None,
                        "confidence": 0.50,
                        "reasons": ["surfaced from sample_modules; lineno unavailable"],
                        "recommended_path": f"from {rel}",
                    }
                )
            for cls_name in (mod.get("classes") or []):
                targets.append(
                    {
                        "action": "assimilate",
                        "symbol": {
                            "root": repo_root,
                            "rel_path": rel,
                            "module": rel.replace("/", ".").removesuffix(".py"),
                            "qualname": cls_name,
                            "kind": "class",
                            "lineno": 0,
                            "end_lineno": 0,
                            "signature": "class",
                            "body_sha256": "",
                            "docstring_present": False,
                            "decorators": [],
                            "imports": [],
                            "has_nearby_test": False,
                        },
                        "matched_primary": None,
                        "confidence": 0.50,
                        "reasons": ["surfaced from sample_modules; lineno unavailable"],
                        "recommended_path": f"from {rel}",
                    }
                )
        return targets
