# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/protocol/evolution.py:245
# Component id: at.source.ass_ade.collect_certificate_summaries
__version__ = "0.1.0"

def collect_certificate_summaries(root: Path, rebuild_path: Path | None = None) -> list[dict[str, Any]]:
    paths = [root.resolve() / "CERTIFICATE.json"]
    if rebuild_path is not None:
        paths.append(rebuild_path.resolve() / "CERTIFICATE.json")
    summaries: list[dict[str, Any]] = []
    for path in paths:
        if path.exists():
            summary = _certificate_summary(path)
            if summary:
                summaries.append(summary)
    return summaries
