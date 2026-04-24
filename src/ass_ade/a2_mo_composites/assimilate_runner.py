"""Tier a2 — stateful assimilate runner: reads a cherry-pick manifest, copies symbols into target tiers."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.cherry_types import AssimilateResultDict, CherryItemDict, CherryManifestDict
from ass_ade.a1_at_functions.assimilate_helpers import (
    compose_file_header,
    count_loc,
    extract_module_imports,
    extract_source_lines,
    suggest_target_filename,
    tier_for_kind,
)


class AssimilateRunner:
    """Read a cherry_pick manifest and copy selected symbols into the target project's tier directories."""

    def __init__(
        self,
        manifest_path: str | Path,
        target_root: str | Path | None = None,
        tier_override: str | None = None,
    ) -> None:
        self.manifest_path = Path(manifest_path).resolve()
        self._tier_override = tier_override
        self._manifest: CherryManifestDict | None = None
        self._target_root: Path | None = Path(target_root).resolve() if target_root else None

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self) -> CherryManifestDict:
        if self._manifest is not None:
            return self._manifest
        raw = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self._manifest = raw  # type: ignore[assignment]
        return self._manifest  # type: ignore[return-value]

    @property
    def target_root(self) -> Path:
        if self._target_root is not None:
            return self._target_root
        manifest = self.load()
        stored = manifest.get("target_root", "")
        return Path(stored).resolve() if stored else Path.cwd()

    # ------------------------------------------------------------------
    # Single item
    # ------------------------------------------------------------------

    def run_item(self, item: CherryItemDict, *, dry_run: bool = False) -> AssimilateResultDict:
        """Assimilate one cherry-picked symbol into the target project."""
        qualname = item["qualname"]
        kind = item["kind"]
        source_root = item["source_root"]
        rel_path = item["rel_path"]
        lineno = item["lineno"]
        end_lineno = item["end_lineno"]

        result: AssimilateResultDict = {
            "qualname": qualname,
            "rel_path": rel_path,
            "action": item["action"],
            "status": "error",
            "target_file": "",
            "tier": "",
            "lines": 0,
            "error": "",
        }

        if lineno == 0:
            result["status"] = "skipped"
            result["error"] = "lineno=0: symbol was surfaced from sample_modules without exact position"
            return result

        tier = tier_for_kind(kind, self._tier_override)
        filename = suggest_target_filename(qualname, kind, tier)

        source_abs = Path(source_root) / rel_path
        body = extract_source_lines(source_abs, lineno, end_lineno)
        imports_block = extract_module_imports(source_abs)

        description = f"assimilated {kind} {qualname!r}"
        source_ref = f"{rel_path}:{lineno}-{end_lineno}"
        header = compose_file_header(tier, description, source_ref)

        # Build file content
        content_parts = [header]
        if imports_block:
            content_parts.append(f"\n# --- imports from original module ---\n{imports_block}\n")
        content_parts.append(f"\n\n# --- assimilated symbol ---\n{textwrap.dedent(body)}\n")
        content = "".join(content_parts)

        # Target path: src/ass_ade/<tier>/<filename> if target has that structure, else <tier>/<filename>
        tier_dir = self._resolve_tier_dir(tier)
        target_file = tier_dir / filename
        rel_target = target_file.relative_to(self.target_root) if target_file.is_relative_to(self.target_root) else target_file

        result["tier"] = tier
        result["target_file"] = str(rel_target)
        result["lines"] = count_loc(content)

        if dry_run:
            result["status"] = "dry_run"
            return result

        try:
            tier_dir.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
            result["status"] = "written"
        except OSError as exc:
            result["status"] = "error"
            result["error"] = str(exc)

        return result

    # ------------------------------------------------------------------
    # Batch
    # ------------------------------------------------------------------

    def run_all(self, *, dry_run: bool = False) -> list[AssimilateResultDict]:
        """Run assimilation for all items in the manifest."""
        manifest = self.load()
        items: list[CherryItemDict] = manifest.get("items", [])  # type: ignore[assignment]
        return [self.run_item(item, dry_run=dry_run) for item in items]

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _resolve_tier_dir(self, tier: str) -> Path:
        """Find or create the tier directory inside the target project."""
        root = self.target_root

        # Check for src/<pkg>/<tier> pattern (standard ASS-ADE layout)
        src_candidates = list(root.glob(f"src/*/{tier}"))
        if src_candidates:
            return src_candidates[0]

        # Check for direct <tier> subdirectory
        direct = root / tier
        if direct.is_dir():
            return direct

        # Fall back: create <root>/<tier>
        return root / tier

    def summary(self, results: list[AssimilateResultDict]) -> dict[str, Any]:
        """Build a summary dict from a run_all() result set."""
        by_status: dict[str, int] = {}
        for r in results:
            by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        # dry_run items are treated as "would write" for display purposes
        actionable = [r for r in results if r["status"] in ("written", "dry_run")]
        return {
            "total": len(results),
            "by_status": by_status,
            "written": actionable,
            "skipped": [r for r in results if r["status"] == "skipped"],
            "errors": [r for r in results if r["status"] == "error"],
        }
