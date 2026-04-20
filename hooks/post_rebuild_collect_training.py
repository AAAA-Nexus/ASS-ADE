"""Post-rebuild hook: extract transformation data and append to training_data.jsonl.

After every rebuild, scans the rebuilt output folder for certification artifacts,
enhancement outputs, and report files, then appends new training samples to
training_data/training_data.jsonl. This feeds the local LoRA flywheel with
fresh before/after transformation data over time.

Hook contract:
    run(path: str) -> dict
        path: the output folder produced by ass-ade rebuild
        returns: {ok, samples_added, training_data_path, error}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def run(path: str) -> dict:
    """Extract training samples from the rebuilt folder and append to training_data.jsonl.

    Args:
        path: The output folder produced by ass-ade rebuild.

    Returns:
        dict with keys:
            ok (bool): True on success.
            samples_added (int): Number of new samples appended.
            training_data_path (str): Path to the training_data.jsonl file.
            error (str | None): Error message when ok=False.
    """
    target = Path(path)
    if not target.exists():
        return {
            "ok": False,
            "samples_added": 0,
            "training_data_path": None,
            "error": f"rebuilt output path does not exist: {path}",
        }

    # Find the project root (parent of the rebuilt output, or cwd)
    project_root = Path.cwd()

    # Locate the collect script relative to project root
    collect_script = project_root / "scripts" / "lora_training" / "collect_training_data.py"
    if not collect_script.exists():
        return {
            "ok": False,
            "samples_added": 0,
            "training_data_path": None,
            "error": f"collect script not found: {collect_script}",
        }

    training_data_dir = project_root / "training_data"
    training_data_dir.mkdir(parents=True, exist_ok=True)
    out_path = training_data_dir / "training_data.jsonl"

    # Count existing samples so we can report the delta
    existing_count = _count_lines(out_path)

    # Import the collect module and run it on the rebuilt path
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("collect_training_data", collect_script)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr]

        # Run collect on the rebuilt output directory (contains CERTIFICATE.json etc.)
        mod.collect(root=target.resolve(), out=out_path.resolve())  # type: ignore[attr-defined]

        # Also sweep the project root for any new reports accumulated since last run
        mod.collect(root=project_root.resolve(), out=out_path.resolve())  # type: ignore[attr-defined]

    except Exception as exc:
        return {
            "ok": False,
            "samples_added": 0,
            "training_data_path": str(out_path),
            "error": f"collect failed: {exc}",
        }

    new_count = _count_lines(out_path)
    added = max(0, new_count - existing_count)

    return {
        "ok": True,
        "samples_added": added,
        "training_data_path": str(out_path),
        "error": None,
    }


def _count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    try:
        with path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.strip():
                    count += 1
    except Exception:
        pass
    return count


if __name__ == "__main__":
    result = run(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(json.dumps(result, indent=2))
