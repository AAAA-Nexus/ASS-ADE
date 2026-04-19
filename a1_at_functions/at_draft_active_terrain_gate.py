# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/map_terrain.py:477
# Component id: at.source.ass_ade.active_terrain_gate
__version__ = "0.1.0"

def active_terrain_gate(
    required_capabilities: list[str],
    context: dict[str, Any] | None = None,
    working_dir: str | Path = ".",
    write_stubs: bool = True,
) -> ActiveTerrainVerdict:
    """Active MAP=TERRAIN loop: check capabilities, HALT and invent stubs for missing ones.

    For each missing capability:
      1. Generate a Python invention stub (raises NotImplementedError with spec)
      2. Return HALT_AND_INVENT with stub paths

    Args:
        required_capabilities: List of capability names needed for the task.
        context: Optional dict with 'task_description' and 'cap_type' hints.
        working_dir: Project root for stub placement.
        write_stubs: If True, write stub files to disk. Set False in tests.

    Returns:
        ActiveTerrainVerdict with verdict PROCEED or HALT_AND_INVENT.
    """
    ctx = context or {}
    root = Path(working_dir).resolve()
    task_description = ctx.get("task_description", "unknown task")
    default_cap_type: CapabilityType = "tools"

    # Build current inventory
    inventory = build_capability_inventory(working_dir=root)
    all_known: set[str] = set()
    for names in inventory.values():
        all_known.update(names)

    present: list[str] = []
    missing_names: list[str] = []
    for cap in required_capabilities:
        slug = _slug(cap)
        if slug in all_known:
            present.append(cap)
        else:
            missing_names.append(cap)

    if not missing_names:
        return ActiveTerrainVerdict(
            verdict="PROCEED",
            capabilities_present=present,
            capabilities_missing=[],
            next_action="All required capabilities present. Proceed to synthesis.",
        )

    stubs: list[InventionStub] = []
    for cap_name in missing_names:
        spec = (
            f"Capability '{cap_name}' required for: {task_description}. "
            "Must provide a stable Python interface with fail-open design."
        )
        criteria = [
            "Stable __init__(config, nexus) signature.",
            "Returns structured dataclass or dict.",
            "Fail-open: exceptions are caught and logged.",
            "Unit tests pass in local mode without Nexus.",
        ]
        stub_path = ""
        if write_stubs:
            stub_path = _write_invention_stub(
                name=cap_name,
                cap_type=default_cap_type,
                spec_summary=spec,
                verification_criteria=criteria,
                src_root=root,
            )
        stubs.append(InventionStub(
            capability_name=cap_name,
            stub_path=stub_path,
            spec_summary=spec,
            verification_criteria=criteria,
        ))

    return ActiveTerrainVerdict(
        verdict="HALT_AND_INVENT",
        stubs_created=stubs,
        capabilities_present=present,
        capabilities_missing=missing_names,
        next_action=(
            f"HALTED. {len(missing_names)} capability stub(s) created. "
            "Implement each stub before retrying the original task."
        ),
    )
