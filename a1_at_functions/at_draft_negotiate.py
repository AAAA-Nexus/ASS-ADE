# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/a2a/__init__.py:261
# Component id: at.source.ass_ade.negotiate
__version__ = "0.1.0"

def negotiate(local: A2AAgentCard, remote: A2AAgentCard) -> NegotiationResult:
    """Compare two agent cards and assess interoperability.

    Checks:
      - Skill overlap (by skill id)
      - Authentication compatibility
      - Input/output mode compatibility
    """
    local_skill_ids = {s.id for s in local.skills}
    remote_skill_ids = {s.id for s in remote.skills}

    shared = sorted(local_skill_ids & remote_skill_ids)
    local_only = sorted(local_skill_ids - remote_skill_ids)
    remote_only = sorted(remote_skill_ids - local_skill_ids)

    # Auth compat: if remote requires auth, check local can provide it
    auth_ok = True
    notes: list[str] = []

    if remote.authentication and remote.authentication.schemes:
        local_schemes = set(local.authentication.schemes) if local.authentication else set()
        required = set(remote.authentication.schemes)
        if not required & local_schemes:
            auth_ok = False
            notes.append(
                f"Auth mismatch: remote requires {required}, local has {local_schemes or 'none'}"
            )

    # I/O mode compat
    local_in = set(local.defaultInputModes)
    remote_out = set(remote.defaultOutputModes)
    if not local_in & remote_out:
        notes.append(f"Output format mismatch: remote outputs {remote_out}, local accepts {local_in}")

    compatible = bool(shared) and auth_ok

    return NegotiationResult(
        compatible=compatible,
        shared_skills=shared,
        local_only=local_only,
        remote_only=remote_only,
        auth_compatible=auth_ok,
        notes=notes,
    )
