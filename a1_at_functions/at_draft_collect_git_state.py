# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_collect_git_state.py:5
# Component id: at.source.ass_ade.collect_git_state
__version__ = "0.1.0"

def collect_git_state(root: Path) -> EvolutionGitState:
    root = root.resolve()
    ok_status, status_text = _run_git(root, ["status", "--short"])
    ok_branch, branch = _run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    ok_commit, commit = _run_git(root, ["rev-parse", "--short", "HEAD"])
    if not ok_status:
        return EvolutionGitState(available=False)

    lines = [line for line in status_text.splitlines() if line.strip()]
    staged = 0
    unstaged = 0
    untracked = 0
    for line in lines:
        marker = line[:2]
        if marker == "??":
            untracked += 1
            continue
        if marker[:1].strip():
            staged += 1
        if len(marker) > 1 and marker[1:2].strip():
            unstaged += 1

    return EvolutionGitState(
        available=True,
        branch=branch if ok_branch and branch else "unknown",
        commit=commit if ok_commit and commit else "unknown",
        dirty=bool(lines),
        staged=staged,
        unstaged=unstaged,
        untracked=untracked,
        status=lines[:200],
    )
