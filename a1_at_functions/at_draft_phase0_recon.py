# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_phase0_recon.py:7
# Component id: at.source.a1_at_functions.phase0_recon
from __future__ import annotations

__version__ = "0.1.0"

def phase0_recon(
    *,
    task_description: str,
    working_dir: str | Path = ".",
    provided_sources: list[str] | None = None,
    max_relevant_files: int = 20,
) -> Phase0ReconResult:
    """Run Phase 0 recon and return whether later phases may proceed."""
    if not task_description.strip():
        raise ValueError("task_description must not be empty")

    root = Path(working_dir).resolve()
    summary = summarize_repo(root)
    task_tokens = _tokens(task_description)
    files = _walk_files(root)
    scored = sorted(
        ((path, _score_file(path.relative_to(root), task_tokens)) for path in files),
        key=lambda item: (-item[1], str(item[0])),
    )
    relevant = [
        _rel(root, path)
        for path, score in scored
        if score > 0
    ][:max_relevant_files]
    tests = [
        _rel(root, path)
        for path in files
        if "test" in str(path.relative_to(root)).replace("\\", "/").lower()
    ][:max_relevant_files]
    docs = [
        _rel(root, path)
        for path in files
        if path.suffix.lower() == ".md" or "docs" in path.parts
    ][:max_relevant_files]
    configs = [
        _rel(root, path)
        for path in files
        if path.name in _IMPORTANT_NAMES or path.suffix.lower() in {".toml", ".yaml", ".yml"}
    ][:max_relevant_files]

    sources = [source for source in (provided_sources or []) if source.strip()]
    research_targets = _suggest_research(task_description)
    required_actions: list[str] = []
    verdict: ReconVerdict = "READY_FOR_PHASE_1"

    if not relevant:
        verdict = "RECON_REQUIRED"
        required_actions.append("Inspect the repository enough to identify relevant files.")

    if _is_technical(task_description) and research_targets and not sources:
        verdict = "RECON_REQUIRED"
        required_actions.append(
            "Perform latest technical-document research and attach source URLs before coding."
        )

    return Phase0ReconResult(
        verdict=verdict,
        task_description=task_description,
        codebase=CodebaseRecon(
            root=str(root),
            total_files=summary.total_files,
            total_dirs=summary.total_dirs,
            file_types=summary.file_types,
            top_level_entries=summary.top_level_entries,
            relevant_files=relevant,
            test_files=tests,
            docs_files=docs,
            config_files=configs,
        ),
        research_targets=research_targets,
        provided_sources=sources,
        required_actions=required_actions,
        next_action=(
            "Continue to Phase 1 context analysis."
            if verdict == "READY_FOR_PHASE_1"
            else "Complete required recon before MAP = TERRAIN or code changes."
        ),
    )
