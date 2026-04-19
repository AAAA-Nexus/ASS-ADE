# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/map_terrain.py:299
# Component id: at.source.ass_ade.map_terrain
__version__ = "0.1.0"

def map_terrain(
    *,
    task_description: str,
    required_capabilities: dict[str, list[str]],
    agent_id: str = "ass-ade-local",
    max_development_budget_usdc: float = 1.0,
    auto_invent_if_missing: bool = False,
    invention_constraints: dict[str, Any] | None = None,
    working_dir: str | Path = ".",
    hosted_tools: list[str] | None = None,
) -> MapTerrainResult:
    """Apply the MAP = TERRAIN gate for one task."""
    constraints = invention_constraints or {}
    root = Path(working_dir).resolve()
    inventory = build_capability_inventory(working_dir=root, hosted_tools=hosted_tools)
    inventory_check: dict[str, dict[str, str]] = {key: {} for key in _CAPABILITY_TYPES}
    invalid_requirements: dict[str, str] = {}
    missing: list[MissingCapability] = []

    for raw_type, names in required_capabilities.items():
        cap_type = _normalize_type(raw_type)
        if cap_type is None:
            invalid_requirements[str(raw_type)] = "unsupported capability type"
            continue
        normalized_names = _coerce_required_names(names)
        if not normalized_names:
            # Empty groups mean "no requirements" for that type.
            continue
        for raw_name in normalized_names:
            name = str(raw_name)
            normalized_name = _slug(name)
            exists = normalized_name in inventory[cap_type]
            if not exists and cap_type == "tools" and normalized_name.startswith("nexus_"):
                exists = normalized_name[6:] in inventory[cap_type]
            inventory_check[cap_type][name] = "exists" if exists else "missing"
            if exists:
                continue
            missing.append(MissingCapability(
                name=name,
                type=cap_type[:-1].title(),
                specification=_specification(
                    task_description=task_description,
                    cap_type=cap_type,
                    name=name,
                    constraints=constraints,
                ),
                recommended_creation_tool=_CREATION_TOOL_BY_TYPE[cap_type],
                estimated_fuel_cost=_FUEL_BY_TYPE[cap_type],
                verification_criteria=_verification_criteria(cap_type, constraints),
                human_approval_required=cap_type in {"agents", "harnesses"},
            ))

    if invalid_requirements:
        inventory_check["requirements"] = invalid_requirements
        return MapTerrainResult(
            verdict="HALT_AND_INVENT",
            missing_capabilities=missing,
            inventory_check=inventory_check,
            development_plan=DevelopmentPlan(
                steps=[
                    "1. Fix required_capabilities schema and capability types.",
                    "2. Re-run MAP = TERRAIN gate.",
                ],
                total_estimated_time_seconds=30,
                auto_invent_triggered=False,
            ),
            next_action="Correct capability requirements before retrying original task.",
        )

    if not missing:
        return MapTerrainResult(
            verdict="PROCEED",
            inventory_check=inventory_check,
            next_action="Continue to Phase 3 synthesis.",
        )

    total_cost = sum(item.estimated_fuel_cost for item in missing)
    auto_allowed = (
        auto_invent_if_missing
        and total_cost <= max_development_budget_usdc
        and all(item.type.lower() in {"tool", "skill"} for item in missing)
    )
    created_assets: list[str] = []
    if auto_allowed:
        created_assets = _persist_development_plan(
            working_dir=root,
            task_description=task_description,
            missing=missing,
        )

    return MapTerrainResult(
        verdict="HALT_AND_INVENT",
        missing_capabilities=missing,
        inventory_check=inventory_check,
        development_plan=DevelopmentPlan(
            steps=[
                "1. Synthesize capability specification.",
                "2. Generate implementation candidate.",
                "3. Run sandbox and fixture verification.",
                "4. Register verified asset in Asset Memory.",
                "5. Retry original task from Phase 2.",
            ],
            total_estimated_time_seconds=max(30, len(missing) * 60),
            auto_invent_triggered=auto_allowed,
            created_assets=created_assets,
        ),
        next_action="Execute development plan before retrying original task.",
    )
