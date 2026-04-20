"""Post-rebuild hook: build a vector context map for the rebuilt output.

Reads all materialized components and writes a context-map JSON that downstream
tools (chat, enhance, design) can load for semantic search. Runs after rebuild;
failures are warnings and do not block the pipeline.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


_VECTOR_STUBS = True  # flip to False when real embedding client is wired


def _collect_components(output_dir: Path) -> list[dict]:
    """Walk tier folders and collect component metadata."""
    tier_prefixes = [
        "a0_qk_constants",
        "a1_at_functions",
        "a2_mo_composites",
        "a3_og_features",
        "a4_sy_orchestration",
    ]
    components = []
    for tier in tier_prefixes:
        tier_dir = output_dir / tier
        if not tier_dir.exists():
            continue
        for py_file in sorted(tier_dir.glob("**/*.py")):
            rel = py_file.relative_to(output_dir)
            try:
                source = py_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                source = ""
            components.append({
                "id": str(rel).replace("\\", "/"),
                "tier": tier,
                "path": str(py_file),
                "size_bytes": py_file.stat().st_size,
                "lines": source.count("\n") + 1,
                # Stub: in production this would be a real embedding vector.
                "embedding": None,
            })
    return components


def _build_context_map(output_dir: Path, components: list[dict]) -> dict:
    manifest_path = output_dir / "MANIFEST.json"
    manifest: dict = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "schema": "ass-ade/context-map/v1",
        "source_dir": str(output_dir),
        "component_count": len(components),
        "rebuild_tag": manifest.get("rebuild_tag", ""),
        "components": components,
        "embedding_model": None,  # set when real embeddings are used
        "generated_by": "post_rebuild_context_load",
    }


def run(path: str) -> dict:
    """Build a context map for the rebuilt codebase.

    Args:
        path: The output folder produced by ass-ade rebuild.

    Returns:
        dict with keys:
            ok (bool): Always True; context-load failure is a warning.
            context_map_path (str | None): Path to the written context-map JSON.
            component_count (int): Number of components indexed.
            warnings (list[str]): Any issues encountered.
    """
    target = Path(path)
    if not target.exists():
        return {
            "ok": True,
            "context_map_path": None,
            "component_count": 0,
            "warnings": [f"rebuilt output path does not exist: {path}"],
        }

    warnings: list[str] = []

    try:
        components = _collect_components(target)
        context_map = _build_context_map(target, components)
        out_path = target / ".context-map.json"
        out_path.write_text(json.dumps(context_map, indent=2), encoding="utf-8")
    except Exception as exc:
        warnings.append(f"context map build failed: {exc}")
        return {
            "ok": True,
            "context_map_path": None,
            "component_count": 0,
            "warnings": warnings,
        }

    return {
        "ok": True,
        "context_map_path": str(out_path),
        "component_count": len(components),
        "warnings": warnings,
    }


if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = run(target_path)
    print(json.dumps(result, indent=2))
    # Always exit 0; context-load failure is a warning.
