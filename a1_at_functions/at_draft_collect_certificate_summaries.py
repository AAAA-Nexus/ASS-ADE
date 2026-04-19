# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_collect_certificate_summaries.py:7
# Component id: at.source.a1_at_functions.collect_certificate_summaries
from __future__ import annotations

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
