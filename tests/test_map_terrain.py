from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.map_terrain import map_terrain
from ass_ade.mcp.server import MCPServer

runner = CliRunner()


def _dispatch(server: MCPServer, request: dict[str, object]) -> object:
    handler = getattr(server, "_handle")
    return handler(request)


def _initialize_server(server: MCPServer) -> None:
    response = _dispatch(
        server,
        {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "initialize",
            "params": {},
        },
    )
    assert response is not None
    _dispatch(server, {"method": "notifications/initialized", "params": {}})


def test_map_terrain_proceed_for_existing_local_and_hosted_tool(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Read a file and authorize the action.",
        required_capabilities={
            "tools": ["read_file", "authorize_action"],
            "harnesses": ["pytest"],
        },
        working_dir=tmp_path,
        hosted_tools=["authorize_action"],
    )

    assert result.verdict == "PROCEED"
    assert result.missing_capabilities == []
    assert result.inventory_check["tools"]["read_file"] == "exists"
    assert result.inventory_check["tools"]["authorize_action"] == "exists"


def test_map_terrain_halts_and_builds_invention_plan(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Scan Python code for OWASP findings.",
        required_capabilities={"agents": ["security_scanner"]},
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.missing_capabilities[0].name == "security_scanner"
    assert (
        result.missing_capabilities[0].recommended_creation_tool == "nexus_spawn_agent"
    )
    assert result.development_plan is not None
    assert result.development_plan.auto_invent_triggered is False


def test_map_terrain_auto_invent_materializes_tool_packet(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Run Semgrep before merge.",
        required_capabilities={"tools": ["nexus_semgrep_scan"]},
        auto_invent_if_missing=True,
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.development_plan is not None
    assert result.development_plan.auto_invent_triggered is True
    tool_path = (
        tmp_path / "src" / "ass_ade" / "tools" / "generated" / "nexus_semgrep_scan.py"
    )
    packet_root = (
        tmp_path
        / ".ass-ade"
        / "capability-development"
        / "generated"
        / "tools-nexus_semgrep_scan"
    )
    manifest_path = packet_root / "manifest.json"
    assert tool_path.exists()
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["capability"]["name"] == "nexus_semgrep_scan"
    follow_up = map_terrain(
        task_description="Run Semgrep before merge.",
        required_capabilities={"tools": ["nexus_semgrep_scan"]},
        working_dir=tmp_path,
    )
    assert follow_up.verdict == "PROCEED"


def test_map_terrain_accepts_single_string_capability_name(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Read one file.",
        required_capabilities={"tools": "read_file"},
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["tools"]["read_file"] == "exists"


def test_map_terrain_sees_extended_mcp_workflow_tools(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Store and query context through MCP.",
        required_capabilities={
            "tools": [
                "phase0_recon",
                "context_memory_store",
                "context_memory_query",
                "map_terrain",
            ],
        },
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["tools"]["phase0_recon"] == "exists"
    assert result.inventory_check["tools"]["context_memory_store"] == "exists"


def test_map_terrain_discovers_repo_agent_registry(tmp_path: Path) -> None:
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "certifier.agent.md").write_text("# Certifier\n", encoding="utf-8")
    (agents / "blueprint-architect.agent.md").write_text(
        "# Blueprint Architect\n", encoding="utf-8"
    )

    result = map_terrain(
        task_description="Certify the package.",
        required_capabilities={"agents": ["certifier", "blueprint_architect"]},
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["agents"]["certifier"] == "exists"
    assert result.inventory_check["agents"]["blueprint_architect"] == "exists"


def test_map_terrain_discovers_repo_asset_conventions(tmp_path: Path) -> None:
    skills = tmp_path / "skills"
    skills.mkdir()
    (skills / "design.skill.md").write_text("# Design\n", encoding="utf-8")

    prompts = tmp_path / "prompts"
    prompts.mkdir()
    (prompts / "blueprint-architect.md").write_text(
        "# Blueprint Architect\n", encoding="utf-8"
    )
    (prompts / "router_pack.prompt.md").write_text("# Router Pack\n", encoding="utf-8")

    instructions = tmp_path / "instructions"
    instructions.mkdir()
    (instructions / "router_rules.instructions.md").write_text(
        "# Router Rules\n", encoding="utf-8"
    )

    harnesses = tmp_path / "harnesses"
    harnesses.mkdir()
    (harnesses / "smoke_runner.py").write_text(
        "def run_harness():\n    return {}\n", encoding="utf-8"
    )

    result = map_terrain(
        task_description="Load generated repo assets.",
        required_capabilities={
            "skills": ["design"],
            "prompts": ["blueprint_architect", "router_pack"],
            "instructions": ["router_rules"],
            "harnesses": ["smoke_runner"],
        },
        working_dir=tmp_path,
    )

    assert result.verdict == "PROCEED"
    assert result.inventory_check["skills"]["design"] == "exists"
    assert result.inventory_check["prompts"]["blueprint_architect"] == "exists"
    assert result.inventory_check["instructions"]["router_rules"] == "exists"


def test_map_terrain_auto_invent_supports_prompts_and_instructions(
    tmp_path: Path,
) -> None:
    result = map_terrain(
        task_description="Create routing prompts and instructions.",
        required_capabilities={
            "prompts": ["router_pack"],
            "instructions": ["router_rules"],
        },
        auto_invent_if_missing=True,
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.development_plan is not None
    assert result.development_plan.auto_invent_triggered is True
    assert (tmp_path / "prompts" / "router_pack.prompt.md").exists()
    assert (tmp_path / "instructions" / "router_rules.instructions.md").exists()
    follow_up = map_terrain(
        task_description="Create routing prompts and instructions.",
        required_capabilities={
            "prompts": ["router_pack"],
            "instructions": ["router_rules"],
        },
        working_dir=tmp_path,
    )
    assert follow_up.verdict == "PROCEED"


def test_map_terrain_halts_for_invalid_requirement_type(tmp_path: Path) -> None:
    result = map_terrain(
        task_description="Run a guarded action.",
        required_capabilities={"unknown_type": ["x"]},
        working_dir=tmp_path,
    )

    assert result.verdict == "HALT_AND_INVENT"
    assert result.development_plan is not None
    assert (
        result.inventory_check["requirements"]["unknown_type"]
        == "unsupported capability type"
    )


def test_mcp_map_terrain_tool_halts_for_missing_tool(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_server(server)
    response = _dispatch(
        server,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "map_terrain",
                "arguments": {
                    "task_description": "Need a missing scanner.",
                    "required_capabilities": {"tools": ["nexus_semgrep_scan"]},
                },
            },
        },
    )

    assert response is not None
    assert response["result"]["isError"] is True
    text = response["result"]["content"][0]["text"]
    assert '"verdict": "HALT_AND_INVENT"' in text


def test_mcp_map_terrain_tool_proceeds_for_existing_tool(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_server(server)
    response = _dispatch(
        server,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "map_terrain",
                "arguments": {
                    "task_description": "Need an existing reader.",
                    "required_capabilities": {"tools": ["read_file"]},
                },
            },
        },
    )

    assert response is not None
    assert response["result"]["isError"] is False
    text = response["result"]["content"][0]["text"]
    assert '"verdict": "PROCEED"' in text


def test_mcp_tools_list_includes_map_terrain(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_server(server)
    response = _dispatch(
        server,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        },
    )

    assert response is not None
    tools = response["result"]["tools"]
    assert any(tool["name"] == "map_terrain" for tool in tools)


def test_cli_map_terrain_json(tmp_path: Path) -> None:
    req = tmp_path / "requirements.json"
    req.write_text(json.dumps({"tools": ["read_file"]}), encoding="utf-8")
    result = runner.invoke(
        app,
        [
            "workflow",
            "map-terrain",
            "Read a file",
            "--requirements-file",
            str(req),
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert '"verdict": "PROCEED"' in result.stdout


def test_cli_map_terrain_accepts_string_requirement(tmp_path: Path) -> None:
    req = tmp_path / "requirements.json"
    req.write_text(json.dumps({"tools": "read_file"}), encoding="utf-8")
    result = runner.invoke(
        app,
        [
            "workflow",
            "map-terrain",
            "Read a file",
            "--requirements-file",
            str(req),
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert '"verdict": "PROCEED"' in result.stdout
