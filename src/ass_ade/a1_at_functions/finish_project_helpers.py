"""Tier a1 — assimilated function 'finish_project'

Assimilated from: rebuild/finish.py:279-361
"""

from __future__ import annotations


# --- assimilated symbol ---
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

