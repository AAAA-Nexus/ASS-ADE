"""Collect training samples from ASS-ADE's own development data.

Scans the project for:
  - CERTIFICATE.json and REBUILD_REPORT.md from past rebuilds
  - benchmarks/ for self-rebuild, self-enhance, self-certify outputs
  - .ass-ade/reports/ for cycle markdown and JSON
  - NEXT_ENHANCEMENT.md for suggestion quality data
  - conversation_history.jsonl from memory if it exists
  - Before/after code transformations from the rebuild engine

Outputs training_data/training_data.jsonl in HuggingFace format:
  {"instruction": "...", "input": "...", "output": "..."}

Usage:
    python scripts/lora_training/collect_training_data.py
    python scripts/lora_training/collect_training_data.py --root /path/to/project --out custom.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SAMPLE_LIMIT = 2000  # hard cap — avoid giant jsonl files
_MIN_OUTPUT_LEN = 40  # discard samples whose output is too short to be useful


def _emit(instruction: str, input_: str, output: str) -> dict[str, str] | None:
    output = output.strip()
    if len(output) < _MIN_OUTPUT_LEN:
        return None
    return {
        "instruction": instruction.strip(),
        "input": input_.strip(),
        "output": output,
    }


# ── Source: CERTIFICATE.json ──────────────────────────────────────────────────


def _from_certificate(root: Path) -> list[dict[str, str]]:
    cert = root / "CERTIFICATE.json"
    if not cert.exists():
        return []
    try:
        data = json.loads(cert.read_text(encoding="utf-8"))
    except Exception:
        return []
    schema = data.get("schema", "ASS-ADE-CERT-001")
    digest = data.get("root_digest", "")
    n_files = len(data.get("files", {}))
    samples: list[dict[str, str]] = []
    s = _emit(
        "Generate a rebuild certificate for this codebase.",
        f"schema: {schema}, files: {n_files}",
        f"schema: {schema}\nfiles: {n_files}\nroot_digest: {digest}",
    )
    if s:
        samples.append(s)
    s = _emit(
        "Verify the integrity of a codebase rebuild certificate.",
        f"root_digest: {digest}\nfiles: {n_files}",
        f"Certificate is valid. Schema {schema}, {n_files} files, root digest {digest[:16]}…",
    )
    if s:
        samples.append(s)
    return samples


# ── Source: REBUILD_REPORT.md / NEXT_ENHANCEMENT.md ──────────────────────────


def _from_markdown_report(path: Path, instruction: str) -> list[dict[str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return []
    lines = text.splitlines()
    header = lines[0] if lines else path.name
    body = "\n".join(lines[1:]).strip()
    s = _emit(instruction, header, body)
    return [s] if s else []


# ── Source: benchmarks/*.txt ──────────────────────────────────────────────────

_BENCHMARK_INSTRUCTIONS: dict[str, str] = {
    "self_rebuild": "Rebuild this codebase using the Atomadic ecosystem rebuilder and report the output.",
    "self_enhance": "Analyze this codebase for enhancement opportunities and list the top findings.",
    "self_certify": "Run the full certification pipeline on this codebase and summarize the result.",
    "self_docs": "Generate or refresh documentation for this codebase and describe the output.",
    "rebuild_demo": "Run a demo rebuild and summarize the result.",
}


def _from_benchmarks(benchmarks_dir: Path) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    if not benchmarks_dir.is_dir():
        return samples
    for txt_file in benchmarks_dir.glob("*.txt"):
        stem = txt_file.stem.lower()
        instruction = next(
            (v for k, v in _BENCHMARK_INSTRUCTIONS.items() if k in stem),
            f"Run the '{stem}' pipeline and summarize the output.",
        )
        text = txt_file.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            continue
        # Use the first 100 chars of the filename as a terse input
        input_ = f"target: {txt_file.name}"
        # Trim very long outputs to 4000 chars to avoid oversized samples
        output = text[:4000]
        s = _emit(instruction, input_, output)
        if s:
            samples.append(s)
    return samples


# ── Source: .ass-ade/reports/*.md and *.json ─────────────────────────────────


def _from_cycle_report_md(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return []
    lines = text.splitlines()
    # Extract goal from ## Assessment block or first heading
    instruction = "Run an ASS-ADE enhancement cycle and report the result."
    input_lines: list[str] = []
    for line in lines[:20]:
        if line.startswith("Goal:"):
            instruction = line[5:].strip() or instruction
        elif line.startswith("- Root:") or line.startswith("- Files:") or line.startswith("- Profile:"):
            input_lines.append(line.lstrip("- "))
    input_ = "\n".join(input_lines) or f"report: {path.name}"
    s = _emit(instruction, input_, text[:4000])
    return [s] if s else []


def _from_cycle_report_json(path: Path) -> list[dict[str, str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(data, dict):
        return []
    goal = data.get("goal", data.get("name", path.stem))
    status = data.get("status", data.get("result", "unknown"))
    steps = data.get("steps", [])
    step_summary = "; ".join(
        f"{s.get('name','?')}={s.get('status','?')}" for s in steps[:10] if isinstance(s, dict)
    )
    output = f"goal: {goal}\nstatus: {status}"
    if step_summary:
        output += f"\nsteps: {step_summary}"
    s = _emit(
        "Show the result of the most recent ASS-ADE cycle run.",
        f"report: {path.name}",
        output,
    )
    return [s] if s else []


def _from_reports_dir(reports_dir: Path) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    if not reports_dir.is_dir():
        return samples
    for md_file in sorted(reports_dir.glob("*.md")):
        samples.extend(_from_cycle_report_md(md_file))
    for json_file in sorted(reports_dir.glob("*.json")):
        samples.extend(_from_cycle_report_json(json_file))
    return samples


# ── Source: conversation_history.jsonl ────────────────────────────────────────


def _from_conversation_history(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    samples: list[dict[str, str]] = []
    pending_user: str | None = None
    with path.open(encoding="utf-8", errors="replace") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                entry: dict[str, Any] = json.loads(raw)
            except Exception:
                continue
            role = entry.get("role", "")
            content = entry.get("content", "")
            if not content:
                continue
            if role == "user":
                pending_user = content
            elif role == "assistant" and pending_user is not None:
                s = _emit(
                    "Respond as the ASS-ADE assistant.",
                    pending_user,
                    content,
                )
                if s:
                    samples.append(s)
                pending_user = None
    return samples


# ── Source: code transformations from agent/lora_flywheel buffer ─────────────


def _from_lora_buffer(root: Path) -> list[dict[str, str]]:
    """Read the local LoRA capture buffer if it exists."""
    buffer_paths = [
        root / ".ass-ade" / "lora_buffer.jsonl",
        root / ".lora-buffer.jsonl",
        root / "training_data" / "lora_buffer.jsonl",
    ]
    samples: list[dict[str, str]] = []
    for bp in buffer_paths:
        if not bp.exists():
            continue
        with bp.open(encoding="utf-8", errors="replace") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    entry: dict[str, Any] = json.loads(raw)
                except Exception:
                    continue
                instruction = entry.get("instruction", "Improve this code.")
                inp = entry.get("input", entry.get("before", ""))
                out = entry.get("output", entry.get("after", ""))
                s = _emit(instruction, inp, out)
                if s:
                    samples.append(s)
    return samples


# ── Dedup by (instruction, input) key ─────────────────────────────────────────


def _dedup(samples: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for s in samples:
        key = (s["instruction"][:80], s["input"][:80])
        if key not in seen:
            seen.add(key)
            result.append(s)
    return result


# ── Main ──────────────────────────────────────────────────────────────────────


def collect(root: Path, out: Path) -> int:
    """Collect all training samples from *root* and write to *out*.

    Returns the number of samples written.
    """
    samples: list[dict[str, str]] = []

    samples.extend(_from_certificate(root))
    samples.extend(
        _from_markdown_report(
            root / "REBUILD_REPORT.md",
            "Summarize this rebuild report.",
        )
    )
    samples.extend(
        _from_markdown_report(
            root / "NEXT_ENHANCEMENT.md",
            "Suggest the next enhancement for this project based on this report.",
        )
    )
    samples.extend(_from_benchmarks(root / "benchmarks"))
    samples.extend(_from_reports_dir(root / ".ass-ade" / "reports"))

    # conversation history — check common locations
    for conv_path in [
        root / "memory" / "conversation_history.jsonl",
        root / ".ass-ade" / "conversation_history.jsonl",
        Path.home() / ".claude" / "conversation_history.jsonl",
    ]:
        samples.extend(_from_conversation_history(conv_path))

    samples.extend(_from_lora_buffer(root))

    samples = _dedup(samples)
    samples = samples[:SAMPLE_LIMIT]

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"[collect] wrote {len(samples)} samples → {out}", file=sys.stderr)
    return len(samples)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path("."), help="Project root to scan (default: cwd).")
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("training_data/training_data.jsonl"),
        help="Output JSONL path.",
    )
    args = ap.parse_args()
    n = collect(args.root.resolve(), args.out.resolve())
    if n == 0:
        print("[collect] WARNING: zero samples collected — check that project has benchmark/report data.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
