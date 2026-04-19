# Extracted from C:/!ass-ade/src/ass_ade/protocol/cycle.py:52
# Component id: at.source.ass_ade.build_assessment
from __future__ import annotations

__version__ = "0.1.0"

def build_assessment(root: Path, settings: AssAdeConfig) -> ProtocolAssessment:
    repo_summary: RepoSummary = summarize_repo(root)
    toolchain = collect_tool_status()

    return ProtocolAssessment(
        root=str(repo_summary.root),
        total_files=repo_summary.total_files,
        total_dirs=repo_summary.total_dirs,
        top_level_entries=repo_summary.top_level_entries,
        file_types=repo_summary.file_types,
        toolchain=_tool_status_payload(toolchain),
        profile=settings.profile,
        local_mode_default=settings.profile == "local",
    )
