# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/scripts/lora_training/collect_training_data.py:264
# Component id: at.source.ass_ade.collect
__version__ = "0.1.0"

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
