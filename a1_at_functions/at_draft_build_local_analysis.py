# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_build_local_analysis.py:5
# Component id: at.source.ass_ade.build_local_analysis
__version__ = "0.1.0"

def build_local_analysis(root: Path) -> dict[str, Any]:
    resolved = root.resolve()
    analysis: dict[str, Any] = {"root": str(resolved)}
    try:
        analysis["languages"] = detect_languages(resolved)
    except Exception:
        analysis["languages"] = {}
    try:
        analysis["metadata"] = load_project_metadata(resolved)
    except Exception:
        analysis["metadata"] = {}
    try:
        analysis["symbols"] = scan_source_symbols(resolved)
    except Exception:
        analysis["symbols"] = []
    try:
        analysis["test_framework"] = detect_test_framework(resolved)
    except Exception:
        analysis["test_framework"] = None
    try:
        analysis["ci"] = detect_ci(resolved)
    except Exception:
        analysis["ci"] = []
    try:
        summary = summarize_repo(resolved)
        analysis["summary"] = {
            "total_files": summary.total_files,
            "total_dirs": summary.total_dirs,
            "file_types": summary.file_types,
            "top_level_entries": summary.top_level_entries,
        }
    except Exception:
        analysis["summary"] = {}
    return analysis
