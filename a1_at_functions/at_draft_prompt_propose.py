# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/prompt_toolkit.py:310
# Component id: at.source.ass_ade.prompt_propose
__version__ = "0.1.0"

def prompt_propose(
    *,
    objective: str,
    working_dir: str | Path = ".",
    prompt_text: str | None = None,
    prompt_path: str | Path | None = None,
) -> PromptProposalResult:
    artifact = load_prompt_artifact(
        working_dir=working_dir,
        prompt_text=prompt_text,
        prompt_path=prompt_path,
    )
    digest = hashlib.sha256(artifact.text.encode()).hexdigest()

    recommended = [
        "Add or refresh a source-boundary section that says the prompt artifact "
        "must not expose hidden runtime prompts or private credentials.",
        "Add a verification section requiring prompt_hash and prompt_validate "
        "before deployment.",
        "Add a drift-control section requiring prompt_diff against the approved "
        "baseline before activation.",
        "Add a rollback section naming the prior prompt hash and restore path.",
    ]
    if objective.strip():
        recommended.insert(0, f"Address objective: {objective.strip()}")

    proposal_id = hashlib.sha256(f"{digest}\0{objective}".encode()).hexdigest()[:24]
    return PromptProposalResult(
        proposal_id=proposal_id,
        source=artifact.source,
        prompt_sha256=digest,
        objective=objective,
        recommended_changes=recommended,
        verification_criteria=[
            "New prompt hash is recorded in a manifest.",
            "prompt_validate passes against the intended manifest.",
            "prompt_diff is reviewed with redaction enabled.",
            "Human approval is recorded before deployment.",
        ],
        next_action="Review the proposal, edit the prompt artifact, then validate against manifest.",
    )
