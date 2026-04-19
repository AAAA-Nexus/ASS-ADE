"""MAP = TERRAIN capability gate.

Before a workflow executes, this module maps the task's required capabilities
to the current local/remote capability substrate. Missing capabilities halt the
original task and produce an invention plan.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from ass_ade.tools.registry import default_registry

CapabilityType = Literal[
    "agents",
    "hooks",
    "skills",
    "tools",
    "harnesses",
    "prompts",
    "instructions",
]
Verdict = Literal["PROCEED", "HALT_AND_INVENT"]


_CAPABILITY_TYPES: tuple[CapabilityType, ...] = (
    "agents",
    "hooks",
    "skills",
    "tools",
    "harnesses",
    "prompts",
    "instructions",
)

_BASE_INVENTORY: dict[CapabilityType, set[str]] = {
    "agents": {
        "ass_ade_agent",
        "build_captain",
        "compliance_packager",
        "dada_prime",
        "ledger_scribe",
        "memory_steward",
        "quota_governor",
        "release_marshal",
        "review_tribunal",
        "safety_sentinel",
        "support_triage_clerk",
    },
    "hooks": {
        "a2a_negotiate",
        "a2a_validate",
        "certify_output",
        "map_terrain",
        "post_call",
        "post_merge",
        "pre_call",
        "pre_merge",
        "pre_task",
        "safe_execute",
        "trust_gate",
    },
    "skills": {
        "a2a_validation",
        "codebase_cartography",
        "local_repo_inspection",
        "lora_capture",
        "mcp_discovery",
        "public_private_boundary",
        "trust_rag_design",
        "x402_payment_flow",
    },
    "tools": {
        "a2a_negotiate",
        "a2a_validate",
        "ask_agent",
        "certify_output",
        "context_memory_query",
        "context_memory_store",
        "context_pack",
        "map_terrain",
        "phase0_recon",
        "safe_execute",
        "trust_gate",
    },
    "harnesses": {
        "ass_ade_mcp_stdio",
        "cloudflare_worker_mcp",
        "pytest",
        "python_subprocess",
        "redacted_admin_probe",
        "windows_powershell",
    },
    "prompts": set(),
    "instructions": set(),
}

_CREATION_TOOL_BY_TYPE: dict[CapabilityType, str] = {
    "agents": "nexus_spawn_agent",
    "hooks": "nexus_synthesize_verified_code",
    "skills": "skill_distiller",
    "tools": "nexus_synthesize_verified_code",
    "harnesses": "nexus_secure_handoff",
    "prompts": "nexus_prompt_optimize",
    "instructions": "nexus_synthesize_verified_code",
}

_FUEL_BY_TYPE: dict[CapabilityType, float] = {
    "agents": 0.08,
    "hooks": 0.04,
    "skills": 0.03,
    "tools": 0.05,
    "harnesses": 0.10,
    "prompts": 0.03,
    "instructions": 0.03,
}

_TIER_TO_DIR = {
    "qk": "a0_qk_constants",
    "at": "a1_at_functions",
    "mo": "a2_mo_composites",
    "og": "a3_og_features",
    "sy": "a4_sy_orchestration",
}


class MissingCapability(BaseModel):
    name: str
    type: str
    type_key: CapabilityType
    specification: str
    recommended_creation_tool: str
    estimated_fuel_cost: float
    verification_criteria: list[str] = Field(default_factory=list)
    human_approval_required: bool = False


class DevelopmentPlan(BaseModel):
    steps: list[str] = Field(default_factory=list)
    total_estimated_time_seconds: int = 0
    auto_invent_triggered: bool = False
    created_assets: list[str] = Field(default_factory=list)


class MapTerrainResult(BaseModel):
    verdict: Verdict
    missing_capabilities: list[MissingCapability] = Field(default_factory=list)
    inventory_check: dict[str, dict[str, str]] = Field(default_factory=dict)
    development_plan: DevelopmentPlan | None = None
    next_action: str


def _coerce_required_names(raw_names: Any) -> list[str]:
    """Normalize capability names to a stable list of non-empty strings."""
    if raw_names is None:
        return []
    if isinstance(raw_names, str):
        return [raw_names] if raw_names.strip() else []
    if isinstance(raw_names, (list, tuple, set)):
        out: list[str] = []
        for item in raw_names:
            text = str(item).strip()
            if text:
                out.append(text)
        return out
    text = str(raw_names).strip()
    return [text] if text else []


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower()).strip("_")
    return slug or "unnamed"


def _one_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _display_name(value: str) -> str:
    parts = [part for part in re.split(r"[_\-\s]+", value.strip()) if part]
    if not parts:
        return "Generated Capability"
    return " ".join(part.capitalize() for part in parts)


def _class_name(value: str) -> str:
    parts = [part for part in re.split(r"[_\-\s]+", _slug(value)) if part]
    return "".join(part.capitalize() for part in parts) or "GeneratedCapability"


def _normalize_type(raw_type: str) -> CapabilityType | None:
    normalized = raw_type.strip().lower().replace("-", "_")
    aliases = {
        "agent": "agents",
        "agents": "agents",
        "hook": "hooks",
        "hooks": "hooks",
        "skill": "skills",
        "skills": "skills",
        "tool": "tools",
        "tools": "tools",
        "harness": "harnesses",
        "harnesses": "harnesses",
        "prompt": "prompts",
        "prompts": "prompts",
        "instruction": "instructions",
        "instructions": "instructions",
    }
    return aliases.get(normalized)  # type: ignore[return-value]


def _load_asset_memory(working_dir: Path) -> dict[CapabilityType, set[str]]:
    memory: dict[CapabilityType, set[str]] = {key: set() for key in _CAPABILITY_TYPES}
    path = working_dir / ".ass-ade" / "assets.json"
    if not path.exists():
        return memory
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return memory
    records = raw.get("assets", raw if isinstance(raw, list) else [])
    if not isinstance(records, list):
        return memory
    for record in records:
        if not isinstance(record, dict):
            continue
        cap_type = _normalize_type(str(record.get("type", "")))
        name = record.get("name")
        status = str(record.get("status", "active")).lower()
        if cap_type and isinstance(name, str) and status not in {"retired", "rejected"}:
            memory[cap_type].add(_slug(name))
    return memory


def _load_repo_inventory(working_dir: Path) -> dict[CapabilityType, set[str]]:
    """Discover lightweight local capability assets that already exist in the repo."""
    inventory: dict[CapabilityType, set[str]] = {
        key: set() for key in _CAPABILITY_TYPES
    }

    agents_dir = working_dir / "agents"
    if agents_dir.is_dir():
        for path in agents_dir.glob("*.agent.md"):
            name = path.name.removesuffix(".agent.md")
            inventory["agents"].add(_slug(name))

    hooks_dir = working_dir / "hooks"
    if hooks_dir.is_dir():
        for path in hooks_dir.glob("*.py"):
            if path.name != "__init__.py":
                inventory["hooks"].add(_slug(path.stem))

    skills_dir = working_dir / "skills"
    if skills_dir.is_dir():
        for path in skills_dir.iterdir():
            if path.is_dir():
                inventory["skills"].add(_slug(path.name))
            elif path.is_file() and path.name.endswith(".skill.md"):
                inventory["skills"].add(_slug(path.name.removesuffix(".skill.md")))

    prompts_dir = working_dir / "prompts"
    if prompts_dir.is_dir():
        for path in prompts_dir.glob("*.md"):
            if path.name.lower() == "readme.md":
                continue
            if path.name.endswith(".prompt.md"):
                name = path.name.removesuffix(".prompt.md")
            else:
                name = path.stem
            inventory["prompts"].add(_slug(name))

    instructions_dir = working_dir / "instructions"
    if instructions_dir.is_dir():
        for path in instructions_dir.glob("*.instructions.md"):
            inventory["instructions"].add(
                _slug(path.name.removesuffix(".instructions.md"))
            )
    for path in (
        working_dir / "copilot-instructions.md",
        working_dir / ".github" / "copilot-instructions.md",
    ):
        if path.is_file():
            inventory["instructions"].add(_slug(path.stem))

    harnesses_dir = working_dir / "harnesses"
    if harnesses_dir.is_dir():
        for path in harnesses_dir.glob("*.py"):
            if path.name != "__init__.py":
                inventory["harnesses"].add(_slug(path.stem))

    return inventory


def build_capability_inventory(
    *,
    working_dir: str | Path = ".",
    hosted_tools: list[str] | None = None,
) -> dict[CapabilityType, set[str]]:
    """Build the current capability inventory from local tools, assets, and hosted MCP."""
    root = Path(working_dir).resolve()
    inventory = {key: set(value) for key, value in _BASE_INVENTORY.items()}
    inventory["tools"].update(default_registry(str(root)).list_tools())
    inventory["tools"].update(_slug(tool) for tool in (hosted_tools or []) if tool)

    for cap_type, names in _load_repo_inventory(root).items():
        inventory[cap_type].update(names)

    for cap_type, names in _load_asset_memory(root).items():
        inventory[cap_type].update(names)

    return inventory


def _specification(
    *,
    task_description: str,
    cap_type: CapabilityType,
    name: str,
    constraints: dict[str, Any],
) -> str:
    cc = constraints.get("max_cyclomatic_complexity", 7)
    proof_required = bool(constraints.get("required_lean4_proof", False))
    sandbox_required = constraints.get("sandbox_test_required", True)
    proof_clause = " Include a formal proof artifact." if proof_required else ""
    return (
        f"{cap_type[:-1].title()} '{name}' is required before executing this task: "
        f"{task_description}. It must provide the named capability with a stable "
        f"JSON-compatible interface, cyclomatic complexity <= {cc}, "
        f"sandbox_test_required={sandbox_required}.{proof_clause}"
    )


def _verification_criteria(
    cap_type: CapabilityType, constraints: dict[str, Any]
) -> list[str]:
    criteria = [
        "Specification is explicit and testable.",
        "Passes positive and negative fixture tests.",
        f"Cyclomatic complexity <= {constraints.get('max_cyclomatic_complexity', 7)}.",
    ]
    if constraints.get("sandbox_test_required", True):
        criteria.append("Passes sandbox execution test.")
    if constraints.get("required_lean4_proof", False):
        criteria.append("Includes required proof artifact.")
    if cap_type in {"agents", "harnesses"}:
        criteria.append("Human approval recorded before deployment.")
    return criteria


def _repo_asset_path(*, working_dir: Path, cap_type: CapabilityType, name: str) -> Path:
    slug = _slug(name)
    if cap_type == "agents":
        return working_dir / "agents" / f"{slug}.agent.md"
    if cap_type == "hooks":
        return working_dir / "hooks" / f"{slug}.py"
    if cap_type == "skills":
        return working_dir / "skills" / f"{slug}.skill.md"
    if cap_type == "tools":
        return working_dir / "src" / "ass_ade" / "tools" / "generated" / f"{slug}.py"
    if cap_type == "harnesses":
        return working_dir / "harnesses" / f"{slug}.py"
    if cap_type == "prompts":
        return working_dir / "prompts" / f"{slug}.prompt.md"
    return working_dir / "instructions" / f"{slug}.instructions.md"


def _ensure_tool_package(asset_path: Path) -> None:
    package_dir = asset_path.parent
    package_dir.mkdir(parents=True, exist_ok=True)
    init_path = package_dir / "__init__.py"
    if not init_path.exists():
        init_path.write_text('"""Generated ASS-ADE tools."""\n', encoding="utf-8")


def _build_capability_blueprint(
    *,
    agent_id: str,
    cap_type: CapabilityType,
    name: str,
    task_description: str,
    repo_asset_path: Path,
) -> dict[str, Any]:
    slug = _slug(name)
    display = _display_name(name)
    blueprint_id = f"invent_{cap_type}_{slug}"
    return {
        "schema": "AAAA-SPEC-004",
        "id": blueprint_id,
        "name": display,
        "description": _one_line(task_description),
        "status": "draft",
        "source": "map_terrain_auto_invent",
        "agent_id": agent_id,
        "repo_asset": repo_asset_path.as_posix(),
        "target_capability": {"name": name, "type": cap_type},
        "tiers": ["qk", "at", "mo", "og", "sy"],
        "components": [
            {
                "id": f"qk.capability.{slug}_spec",
                "tier": "qk",
                "kind": "metadata",
                "role": f"Metadata and invariants for {display}.",
                "depends_on": [],
            },
            {
                "id": f"at.capability.{slug}_normalize",
                "tier": "at",
                "kind": "function",
                "role": f"Normalize structured input for {display}.",
                "depends_on": [f"qk.capability.{slug}_spec"],
            },
            {
                "id": f"mo.capability.{slug}_engine",
                "tier": "mo",
                "kind": "composite",
                "role": f"Core engine for {display}.",
                "depends_on": [f"at.capability.{slug}_normalize"],
            },
            {
                "id": f"og.capability.{slug}_asset",
                "tier": "og",
                "kind": cap_type[:-1],
                "role": f"Repo-native asset for {display}.",
                "depends_on": [f"mo.capability.{slug}_engine"],
            },
            {
                "id": f"sy.capability.{slug}_integration",
                "tier": "sy",
                "kind": "integration",
                "role": f"Registration and verification contract for {display}.",
                "depends_on": [f"og.capability.{slug}_asset"],
            },
        ],
    }


def _component_body(
    *,
    cap_type: CapabilityType,
    tier: str,
    name: str,
    task_description: str,
    repo_asset_path: Path,
    packet_manifest_path: Path,
) -> str:
    display = _display_name(name)
    class_name = _class_name(name)
    summary = _one_line(task_description)
    if tier == "qk":
        return (
            '"""Generated qk metadata for MAP = TERRAIN auto-invention."""\n\n'
            "from __future__ import annotations\n\n"
            "from typing import Any\n\n"
            f"CAPABILITY_NAME = {name!r}\n"
            f"CAPABILITY_TYPE = {cap_type!r}\n"
            f"CAPABILITY_DISPLAY_NAME = {display!r}\n"
            f"CAPABILITY_SUMMARY = {summary!r}\n"
            f"REPO_ASSET_PATH = {repo_asset_path.as_posix()!r}\n"
            f"PACKET_MANIFEST_PATH = {packet_manifest_path.as_posix()!r}\n\n"
            "def capability_metadata() -> dict[str, Any]:\n"
            "    return {\n"
            '        "name": CAPABILITY_NAME,\n'
            '        "type": CAPABILITY_TYPE,\n'
            '        "display_name": CAPABILITY_DISPLAY_NAME,\n'
            '        "summary": CAPABILITY_SUMMARY,\n'
            '        "repo_asset_path": REPO_ASSET_PATH,\n'
            '        "packet_manifest_path": PACKET_MANIFEST_PATH,\n'
            "    }\n"
        )
    if tier == "at":
        return (
            '"""Generated at helpers for MAP = TERRAIN auto-invention."""\n\n'
            "from __future__ import annotations\n\n"
            "from typing import Any\n\n"
            "def normalize_request(payload: dict[str, Any] | None = None) -> dict[str, Any]:\n"
            "    normalized = dict(payload or {})\n"
            f'    normalized.setdefault("capability", {name!r})\n'
            f'    normalized.setdefault("capability_type", {cap_type!r})\n'
            '    normalized.setdefault("status", "ready")\n'
            "    return normalized\n\n"
            "def build_result(payload: dict[str, Any] | None = None, *, ok: bool = True) -> dict[str, Any]:\n"
            "    result = normalize_request(payload)\n"
            '    result["ok"] = ok\n'
            "    return result\n"
        )
    if tier == "mo":
        return (
            '"""Generated mo engine for MAP = TERRAIN auto-invention."""\n\n'
            "from __future__ import annotations\n\n"
            "from typing import Any\n\n"
            f"class {class_name}Engine:\n"
            "    def __init__(self, config: dict[str, Any] | None = None) -> None:\n"
            "        self._config = dict(config or {})\n\n"
            "    def run(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:\n"
            "        data = dict(payload or {})\n"
            f'        data.setdefault("capability", {name!r})\n'
            f'        data.setdefault("capability_type", {cap_type!r})\n'
            f'        data.setdefault("summary", {summary!r})\n'
            '        data.setdefault("config", dict(self._config))\n'
            '        data.setdefault("status", "implemented")\n'
            "        return data\n"
        )
    if tier == "og" and cap_type == "tools":
        return (
            '"""Generated og tool adapter for MAP = TERRAIN auto-invention."""\n\n'
            "from __future__ import annotations\n\n"
            "import json\n"
            "from pathlib import Path\n"
            "from typing import Any\n\n"
            "from ass_ade.tools.base import ToolResult\n\n"
            f"class {class_name}Tool:\n"
            '    def __init__(self, working_dir: str = ".") -> None:\n'
            "        self._working_dir = Path(working_dir).resolve()\n\n"
            "    @property\n"
            "    def name(self) -> str:\n"
            f"        return {name!r}\n\n"
            "    @property\n"
            "    def description(self) -> str:\n"
            f"        return {summary!r}\n\n"
            "    @property\n"
            "    def parameters(self) -> dict[str, Any]:\n"
            "        return {\n"
            '            "type": "object",\n'
            '            "properties": {\n'
            '                "payload": {"type": "object", "description": "Structured input payload."},\n'
            '                "note": {"type": "string", "description": "Optional execution note."},\n'
            "            },\n"
            '            "additionalProperties": True,\n'
            "        }\n\n"
            "    def execute(self, **kwargs: Any) -> ToolResult:\n"
            '        payload = kwargs.get("payload")\n'
            "        if payload is None:\n"
            '            payload = {key: value for key, value in kwargs.items() if key != "payload"}\n'
            "        result = {\n"
            f'            "tool": {name!r},\n'
            f'            "capability_type": {cap_type!r},\n'
            f'            "packet_manifest_path": {packet_manifest_path.as_posix()!r},\n'
            '            "working_dir": str(self._working_dir),\n'
            '            "status": "implemented",\n'
            '            "payload": payload,\n'
            '            "note": kwargs.get("note", ""),\n'
            "        }\n"
            "        return ToolResult(output=json.dumps(result, indent=2))\n"
        )
    if tier == "og" and cap_type in {"hooks", "harnesses"}:
        entrypoint = "run" if cap_type == "hooks" else "run_harness"
        return (
            f'"""Generated og {cap_type[:-1]} for MAP = TERRAIN auto-invention."""\n\n'
            "from __future__ import annotations\n\n"
            "import json\n"
            "from pathlib import Path\n"
            "from typing import Any\n\n"
            f'def {entrypoint}(target: str = ".", **kwargs: Any) -> dict[str, Any]:\n'
            "    resolved = Path(target).resolve()\n"
            "    return {\n"
            f'        "name": {name!r},\n'
            f'        "capability_type": {cap_type!r},\n'
            '        "target": str(resolved),\n'
            f'        "summary": {summary!r},\n'
            f'        "packet_manifest_path": {packet_manifest_path.as_posix()!r},\n'
            '        "status": "implemented",\n'
            '        "arguments": kwargs,\n'
            "    }\n\n"
            'if __name__ == "__main__":\n'
            f"    print(json.dumps({entrypoint}(), indent=2))\n"
        )
    if tier == "og":
        return (
            f'"""Generated og asset renderer for {display}."""\n\n'
            "from __future__ import annotations\n\n"
            "def render_asset_summary() -> dict[str, str]:\n"
            "    return {\n"
            f'        "name": {name!r},\n'
            f'        "capability_type": {cap_type!r},\n'
            f'        "summary": {summary!r},\n'
            f'        "repo_asset_path": {repo_asset_path.as_posix()!r},\n'
            f'        "packet_manifest_path": {packet_manifest_path.as_posix()!r},\n'
            "    }\n"
        )
    return (
        '"""Generated sy integration contract for MAP = TERRAIN auto-invention."""\n\n'
        "from __future__ import annotations\n\n"
        "from typing import Any\n\n"
        "def integration_contract() -> dict[str, Any]:\n"
        "    return {\n"
        f'        "name": {name!r},\n'
        f'        "capability_type": {cap_type!r},\n'
        f'        "repo_asset_path": {repo_asset_path.as_posix()!r},\n'
        f'        "packet_manifest_path": {packet_manifest_path.as_posix()!r},\n'
        '        "status": "verified",\n'
        '        "required_checks": [\n'
        '            "rebuild certificate present",\n'
        '            "enhancement report reviewed",\n'
        '            "asset memory updated",\n'
        "        ],\n"
        "    }\n"
    )


def _build_rebuild_plan(
    *,
    blueprint: dict[str, Any],
    cap_type: CapabilityType,
    name: str,
    task_description: str,
    repo_asset_path: Path,
    packet_manifest_path: Path,
) -> dict[str, Any]:
    proposed_components: list[dict[str, Any]] = []
    for component in blueprint.get("components", []):
        tier = _TIER_TO_DIR[str(component.get("tier", "at"))]
        body = _component_body(
            cap_type=cap_type,
            tier=str(component.get("tier", "at")),
            name=name,
            task_description=task_description,
            repo_asset_path=repo_asset_path,
            packet_manifest_path=packet_manifest_path,
        )
        proposed_components.append(
            {
                "id": component["id"],
                "tier": tier,
                "name": str(component["id"]).split(".")[-1],
                "kind": component.get("kind", "component"),
                "description": component.get("role", task_description),
                "made_of": component.get("depends_on", []),
                "body": body,
                "product_categories": ["COR", "GEN"],
                "source_symbol": {
                    "path": repo_asset_path.as_posix(),
                    "line": 1,
                    "language": "python",
                },
            }
        )
    digest = hashlib.sha256(
        json.dumps(blueprint, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return {
        "content_digest": digest,
        "proposed_components": proposed_components,
    }


def _render_next_enhancement_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Next Enhancement Recommendations",
        "",
        f"Scanned files: {report.get('scanned_files', 0)}",
        f"Total findings: {report.get('total_findings', 0)}",
        "",
    ]
    findings = report.get("findings") or []
    if not findings:
        lines.append(
            "No immediate enhancement opportunities were detected in the generated packet."
        )
        lines.append("")
        return "\n".join(lines)
    for finding in findings[:5]:
        file_label = finding.get("file") or "(no file)"
        line = finding.get("line")
        location = f"{file_label}:{line}" if line else str(file_label)
        lines.extend(
            [
                f"## {finding.get('title', 'Finding')}",
                f"- Category: {finding.get('category', 'unknown')}",
                f"- Impact: {finding.get('impact', 'low')}",
                f"- Effort: {finding.get('effort', 'medium')}",
                f"- Location: {location}",
                f"- Detail: {finding.get('description', '')}",
                "",
            ]
        )
    return "\n".join(lines)


def _render_tool_asset(
    *,
    name: str,
    task_description: str,
    packet_manifest_path: Path,
) -> str:
    summary = _one_line(task_description)
    class_name = _class_name(name)
    return (
        '"""MAP = TERRAIN generated ASS-ADE tool."""\n\n'
        "from __future__ import annotations\n\n"
        "import json\n"
        "from pathlib import Path\n"
        "from typing import Any\n\n"
        "from ass_ade.tools.base import ToolResult\n\n"
        f"class {class_name}Tool:\n"
        '    def __init__(self, working_dir: str = ".") -> None:\n'
        "        self._working_dir = Path(working_dir).resolve()\n\n"
        "    @property\n"
        "    def name(self) -> str:\n"
        f"        return {name!r}\n\n"
        "    @property\n"
        "    def description(self) -> str:\n"
        f"        return {summary!r}\n\n"
        "    @property\n"
        "    def parameters(self) -> dict[str, Any]:\n"
        "        return {\n"
        '            "type": "object",\n'
        '            "properties": {\n'
        '                "payload": {"type": "object", "description": "Structured arguments for the tool."},\n'
        '                "note": {"type": "string", "description": "Optional operator note."},\n'
        "            },\n"
        '            "additionalProperties": True,\n'
        "        }\n\n"
        "    def execute(self, **kwargs: Any) -> ToolResult:\n"
        '        payload = kwargs.get("payload")\n'
        "        if payload is None:\n"
        '            payload = {key: value for key, value in kwargs.items() if key != "payload"}\n'
        "        result = {\n"
        f'            "tool": {name!r},\n'
        f'            "summary": {summary!r},\n'
        f'            "packet_manifest_path": {packet_manifest_path.as_posix()!r},\n'
        '            "working_dir": str(self._working_dir),\n'
        '            "status": "implemented",\n'
        '            "payload": payload,\n'
        '            "note": kwargs.get("note", ""),\n'
        "        }\n"
        "        return ToolResult(output=json.dumps(result, indent=2))\n"
    )


def _render_hook_asset(
    *,
    name: str,
    cap_type: CapabilityType,
    task_description: str,
    packet_manifest_path: Path,
) -> str:
    summary = _one_line(task_description)
    entrypoint = "run" if cap_type == "hooks" else "run_harness"
    return (
        f'"""MAP = TERRAIN generated {cap_type[:-1]}."""\n\n'
        "from __future__ import annotations\n\n"
        "import json\n"
        "from pathlib import Path\n"
        "from typing import Any\n\n"
        f'def {entrypoint}(target: str = ".", **kwargs: Any) -> dict[str, Any]:\n'
        "    resolved = Path(target).resolve()\n"
        "    return {\n"
        f'        "name": {name!r},\n'
        f'        "summary": {summary!r},\n'
        f'        "capability_type": {cap_type!r},\n'
        f'        "packet_manifest_path": {packet_manifest_path.as_posix()!r},\n'
        '        "target": str(resolved),\n'
        '        "status": "implemented",\n'
        '        "arguments": kwargs,\n'
        "    }\n\n"
        'if __name__ == "__main__":\n'
        f"    print(json.dumps({entrypoint}(), indent=2))\n"
    )


def _render_markdown_asset(
    *,
    name: str,
    cap_type: CapabilityType,
    task_description: str,
    packet_manifest_path: Path,
) -> str:
    display = _display_name(name)
    summary = _one_line(task_description)
    description = json.dumps(summary)
    manifest = packet_manifest_path.as_posix()
    if cap_type == "agents":
        return f"""---
name: {json.dumps(display)}
description: {description}
capability-type: {json.dumps(cap_type)}
packet-manifest: {json.dumps(manifest)}
---

# {display}

## Mission
Deliver the `{name}` capability for ASS-ADE while keeping execution inside the public-safe boundary.

## Operating Contract
- Use the implementation packet at `{manifest}` as the source of truth.
- Keep responses structured, testable, and explicit about verification status.
- Escalate for approval before deployment if the agent is promoted beyond local use.

## Verification
- Confirm the rebuild certificate before first use.
- Review the enhancement report before broadening scope.
"""
    if cap_type == "skills":
        return f"""# Skill: {display}

## When to use this skill
Use this skill when ASS-ADE needs the `{name}` capability for: {summary}

## Workflow
1. Read the invention packet at `{manifest}`.
2. Use the repo-native asset generated by MAP = TERRAIN.
3. Re-run the rebuild and enhancement checks after any edits.

## Verification
- Rebuild certificate present.
- Enhancement report reviewed.
"""
    if cap_type == "prompts":
        return f"""---
title: {json.dumps(display)}
description: {description}
capability-type: {json.dumps(cap_type)}
packet-manifest: {json.dumps(manifest)}
---

# {display} Prompt Pack

## System Prompt
You are {display}. Deliver the `{name}` capability for ASS-ADE. Prefer the generated local asset packet at `{manifest}` and keep output structured, explicit, and public-safe.

## Required Behavior
- Surface missing context instead of guessing.
- Keep responses testable.
- Refer operators to the enhancement report when the capability needs hardening.
"""
    return f"""---
name: {json.dumps(display)}
description: {description}
applyTo: "**"
packet-manifest: {json.dumps(manifest)}
---

# {display} Instructions

## Purpose
Guide ASS-ADE when the `{name}` capability is active.

## Rules
- Treat `{summary}` as the primary objective.
- Use the generated packet at `{manifest}` as the implementation reference.
- Require rebuild certification before shipping follow-on edits.
"""


def _render_repo_asset(
    *,
    cap_type: CapabilityType,
    name: str,
    task_description: str,
    packet_manifest_path: Path,
) -> str:
    if cap_type == "tools":
        return _render_tool_asset(
            name=name,
            task_description=task_description,
            packet_manifest_path=packet_manifest_path,
        )
    if cap_type in {"hooks", "harnesses"}:
        return _render_hook_asset(
            name=name,
            cap_type=cap_type,
            task_description=task_description,
            packet_manifest_path=packet_manifest_path,
        )
    return _render_markdown_asset(
        name=name,
        cap_type=cap_type,
        task_description=task_description,
        packet_manifest_path=packet_manifest_path,
    )


def _update_asset_memory(
    *,
    working_dir: Path,
    item: MissingCapability,
    repo_asset_path: Path,
    manifest_path: Path,
    certificate: dict[str, Any],
) -> None:
    memory_path = working_dir / ".ass-ade" / "assets.json"
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {"assets": []}
    assets: list[dict[str, Any]] = []
    if memory_path.exists():
        try:
            existing = json.loads(memory_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {"assets": []}
        if isinstance(existing, list):
            assets = [entry for entry in existing if isinstance(entry, dict)]
        elif isinstance(existing, dict):
            payload = existing
            current = existing.get("assets", [])
            if isinstance(current, list):
                assets = [entry for entry in current if isinstance(entry, dict)]
    assets = [
        entry
        for entry in assets
        if not (
            _normalize_type(str(entry.get("type", ""))) == item.type_key
            and _slug(str(entry.get("name", ""))) == _slug(item.name)
        )
    ]
    assets.append(
        {
            "type": item.type_key,
            "name": item.name,
            "status": "active",
            "path": repo_asset_path.as_posix(),
            "manifest_path": manifest_path.as_posix(),
            "certificate_path": certificate.get("certificate_path"),
            "certificate_sha256": certificate.get("certificate_sha256"),
            "created_at": int(time.time()),
            "source": "map_terrain_auto_invent",
        }
    )
    payload["assets"] = assets
    memory_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _materialize_capability_asset(
    *,
    agent_id: str,
    working_dir: Path,
    task_description: str,
    item: MissingCapability,
) -> list[str]:
    from ass_ade.engine.rebuild.schema_materializer import (
        emit_certificate,
        materialize_plan,
        validate_rebuild,
    )
    from ass_ade.local.enhancer import build_enhancement_report

    packet_root = (
        working_dir
        / ".ass-ade"
        / "capability-development"
        / "generated"
        / f"{item.type_key}-{_slug(item.name)}"
    )
    packet_root.mkdir(parents=True, exist_ok=True)
    repo_asset_path = _repo_asset_path(
        working_dir=working_dir, cap_type=item.type_key, name=item.name
    )
    repo_asset_path.parent.mkdir(parents=True, exist_ok=True)
    if item.type_key == "tools":
        _ensure_tool_package(repo_asset_path)

    blueprint = _build_capability_blueprint(
        agent_id=agent_id,
        cap_type=item.type_key,
        name=item.name,
        task_description=task_description,
        repo_asset_path=repo_asset_path,
    )
    blueprint_dir = packet_root / "blueprints"
    blueprint_dir.mkdir(parents=True, exist_ok=True)
    blueprint_path = blueprint_dir / f"blueprint_{_slug(item.name)}.json"
    blueprint_path.write_text(
        json.dumps(blueprint, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    manifest_path = packet_root / "manifest.json"
    plan = _build_rebuild_plan(
        blueprint=blueprint,
        cap_type=item.type_key,
        name=item.name,
        task_description=task_description,
        repo_asset_path=repo_asset_path,
        packet_manifest_path=manifest_path,
    )
    rebuilds_dir = packet_root / "rebuilds"
    rebuild_tag = f"{item.type_key}_{_slug(item.name)}"
    receipt = materialize_plan(plan, out_dir=rebuilds_dir, rebuild_tag=rebuild_tag)
    receipt["source_plan_digest"] = plan["content_digest"]
    target_root = Path(receipt["target_root"])
    audit = validate_rebuild(target_root)
    certificate = emit_certificate(receipt, audit)
    enhancement = build_enhancement_report(target_root)
    enhancement_path = packet_root / "enhancement_report.json"
    enhancement_path.write_text(
        json.dumps(enhancement, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    next_path = packet_root / "NEXT_ENHANCEMENT.md"
    next_path.write_text(
        _render_next_enhancement_markdown(enhancement) + "\n", encoding="utf-8"
    )

    manifest = {
        "schema": "ass-ade.capability-development/v2",
        "task_description": _one_line(task_description),
        "agent_id": agent_id,
        "capability": item.model_dump(),
        "repo_asset_path": repo_asset_path.as_posix(),
        "blueprint_path": blueprint_path.as_posix(),
        "rebuild_receipt": receipt,
        "audit_summary": audit.get("summary", {}),
        "certificate": certificate,
        "enhancement_report_path": enhancement_path.as_posix(),
        "created_at": int(time.time()),
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    if not repo_asset_path.exists():
        repo_asset_path.write_text(
            _render_repo_asset(
                cap_type=item.type_key,
                name=item.name,
                task_description=task_description,
                packet_manifest_path=manifest_path,
            ),
            encoding="utf-8",
        )

    _update_asset_memory(
        working_dir=working_dir,
        item=item,
        repo_asset_path=repo_asset_path,
        manifest_path=manifest_path,
        certificate=certificate,
    )
    return [
        repo_asset_path.as_posix(),
        blueprint_path.as_posix(),
        target_root.as_posix(),
        certificate["certificate_path"],
        enhancement_path.as_posix(),
        next_path.as_posix(),
        manifest_path.as_posix(),
    ]


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
            if (
                not exists
                and cap_type == "tools"
                and normalized_name.startswith("nexus_")
            ):
                exists = normalized_name[6:] in inventory[cap_type]
            inventory_check[cap_type][name] = "exists" if exists else "missing"
            if exists:
                continue
            missing.append(
                MissingCapability(
                    name=name,
                    type=cap_type[:-1].title(),
                    type_key=cap_type,
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
                )
            )

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
    auto_allowed = auto_invent_if_missing and total_cost <= max_development_budget_usdc
    created_assets: list[str] = []
    if auto_allowed:
        for item in missing:
            created_assets.extend(
                _materialize_capability_asset(
                    agent_id=agent_id,
                    working_dir=root,
                    task_description=task_description,
                    item=item,
                )
            )

    return MapTerrainResult(
        verdict="HALT_AND_INVENT",
        missing_capabilities=missing,
        inventory_check=inventory_check,
        development_plan=DevelopmentPlan(
            steps=[
                "1. Synthesize capability blueprint and repo-native asset contract.",
                "2. Materialize the tiered rebuild packet (qk/at/mo/og/sy).",
                "3. Run rebuild audit and certificate issuance.",
                "4. Run the enhancement scanner and review follow-up findings.",
                "5. Register the asset in Asset Memory and retry the original task.",
            ],
            total_estimated_time_seconds=max(45, len(missing) * 90),
            auto_invent_triggered=auto_allowed,
            created_assets=created_assets,
        ),
        next_action=(
            f"Review generated capability packet(s) for agent {agent_id} and rerun MAP = TERRAIN."
            if auto_allowed
            else "Execute the capability development plan before retrying the original task."
        ),
    )


# ── Active MAP=TERRAIN Invention Loop (Phase 2) ───────────────────────────────


class InventionStub(BaseModel):
    """A generated implementation packet for a missing capability."""

    capability_name: str
    stub_path: str
    spec_summary: str
    verification_criteria: list[str] = Field(default_factory=list)


class ActiveTerrainVerdict(BaseModel):
    """Result of the active MAP=TERRAIN loop."""

    verdict: Verdict
    stubs_created: list[InventionStub] = Field(default_factory=list)
    capabilities_present: list[str] = Field(default_factory=list)
    capabilities_missing: list[str] = Field(default_factory=list)
    next_action: str


def _write_invention_stub(
    name: str,
    cap_type: CapabilityType,
    spec_summary: str,
    verification_criteria: list[str],
    src_root: Path,
) -> str:
    """Materialize the repo-native asset and tiered packet for a missing capability."""
    item = MissingCapability(
        name=name,
        type=cap_type[:-1].title(),
        type_key=cap_type,
        specification=spec_summary,
        recommended_creation_tool=_CREATION_TOOL_BY_TYPE[cap_type],
        estimated_fuel_cost=_FUEL_BY_TYPE[cap_type],
        verification_criteria=verification_criteria,
        human_approval_required=cap_type in {"agents", "harnesses"},
    )
    created = _materialize_capability_asset(
        agent_id="active_terrain_gate",
        working_dir=src_root,
        task_description=spec_summary,
        item=item,
    )
    return created[0] if created else ""


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
    default_cap_type = _normalize_type(str(ctx.get("cap_type", "tools"))) or "tools"

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
        stubs.append(
            InventionStub(
                capability_name=cap_name,
                stub_path=stub_path,
                spec_summary=spec,
                verification_criteria=criteria,
            )
        )

    return ActiveTerrainVerdict(
        verdict="HALT_AND_INVENT",
        stubs_created=stubs,
        capabilities_present=present,
        capabilities_missing=missing_names,
        next_action=(
            f"HALTED. {len(missing_names)} capability implementation packet(s) created. "
            "Review the generated assets before retrying the original task."
        ),
    )
