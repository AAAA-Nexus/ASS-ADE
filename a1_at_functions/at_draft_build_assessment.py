# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_build_assessment.py:5
# Component id: at.source.ass_ade.build_assessment
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
