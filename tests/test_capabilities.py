from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from ass_ade import interpreter
from ass_ade.config import AssAdeConfig
from ass_ade.agent.capabilities import (
    build_capability_snapshot,
    build_atomadic_intent_prompt,
    command_path_exists,
    render_atomadic_help,
    render_capability_prompt_section,
    sync_atomadic_prompt_capabilities,
)
from ass_ade.agent.context import build_system_prompt
from ass_ade.interpreter import Atomadic


def test_dynamic_prompt_includes_protocol_evolution_commands(tmp_path: Path) -> None:
    prompt = build_atomadic_intent_prompt(tmp_path)

    assert "Dynamic Capability Inventory" in prompt
    assert "Capability summary" in prompt
    assert "Resolved capability root:" in prompt
    assert "Rebuild-aware artifact map" in prompt
    assert "Detected monadic tiers" in prompt
    assert "Skills" in prompt
    assert "Runtime routing rules" in prompt
    assert "Hosted Nexus MCP tools discovered in this session" in prompt
    assert "`protocol evolution-record`" in prompt
    assert "`protocol evolution-demo`" in prompt
    assert "`protocol version-bump`" in prompt
    assert "`prompt sync-agent`" in prompt
    assert "`prompt_hash`" in prompt
    assert "Generated at:" in prompt


def test_capability_inventory_discovers_repo_skills(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    skills = tmp_path / "skills"
    skills.mkdir()
    (skills / "prompt-governance.skill.md").write_text(
        "# Prompt Governance Skill\n\n## Steps\n\n1. Hash the prompt.\n",
        encoding="utf-8",
    )

    snapshot = build_capability_snapshot(tmp_path)
    rendered = render_capability_prompt_section(tmp_path)

    assert any(item.name == "prompt-governance.skill.md" for item in snapshot.skills)
    assert "Skills: 1" in rendered
    assert "`prompt-governance.skill.md` - Prompt Governance Skill" in rendered


def test_capability_inventory_maps_surfaces_and_monadic_tiers(tmp_path: Path) -> None:
    for dirname in ("agents", "skills", "hooks", "tools", "mcp", "a0_qk_constants", "a4_sy_orchestration"):
        (tmp_path / dirname).mkdir()
    (tmp_path / "hooks" / "pipeline_config.json").write_text("{}", encoding="utf-8")
    nested = tmp_path / "a4_sy_orchestration" / "nested"
    nested.mkdir()

    snapshot = build_capability_snapshot(nested)
    rendered = render_capability_prompt_section(nested)

    assert snapshot.repo_root == str(tmp_path)
    assert any(item.name == "agents/" for item in snapshot.surface_locations)
    assert any(item.name == "hooks/pipeline_config.json" for item in snapshot.surface_locations)
    assert any(item.name == "a0_qk_constants/" for item in snapshot.monadic_tiers)
    assert any(item.name == "a4_sy_orchestration/" for item in snapshot.monadic_tiers)
    assert "Rebuild-aware artifact map" in rendered
    assert "`a4_sy_orchestration/` - ASS-ADE sy orchestration tier" in rendered


def test_capability_inventory_discovers_dynamic_ability_manifests(tmp_path: Path) -> None:
    generated_tool = tmp_path / "src" / "ass_ade" / "tools" / "generated" / "nexus_semgrep_scan.py"
    generated_tool.parent.mkdir(parents=True)
    generated_tool.write_text("# generated placeholder\n", encoding="utf-8")
    ass_ade = tmp_path / ".ass-ade"
    packet = ass_ade / "capability-development" / "generated" / "tools-nexus_semgrep_scan"
    packet.mkdir(parents=True)
    (ass_ade / "assets.json").write_text(
        json.dumps(
            {
                "assets": [
                    {
                        "type": "tools",
                        "name": "nexus_semgrep_scan",
                        "description": "Run Semgrep before merge.",
                        "path": "src/ass_ade/tools/generated/nexus_semgrep_scan.py",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (packet / "manifest.json").write_text(
        json.dumps(
            {
                "task_description": "Run Semgrep before merge.",
                "capability": {
                    "name": "nexus_semgrep_scan",
                    "type": "Tool",
                    "type_key": "tools",
                },
                "repo_asset_path": "src/ass_ade/tools/generated/nexus_semgrep_scan.py",
            }
        ),
        encoding="utf-8",
    )
    (ass_ade / "features.json").write_text(
        json.dumps(
            {
                "features": [
                    {
                        "kind": "feature",
                        "name": "adaptive_router",
                        "summary": "Load rebuild-era routing features dynamically.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    snapshot = build_capability_snapshot(tmp_path)
    rendered = render_capability_prompt_section(tmp_path)
    names = [item.name for item in snapshot.dynamic_abilities]

    assert names.count("tools:nexus_semgrep_scan") == 1
    assert "feature:adaptive_router" in names
    assert "Dynamic abilities: 2" in rendered
    assert "`tools:nexus_semgrep_scan` - Run Semgrep before merge." in rendered
    assert "`feature:adaptive_router` - Load rebuild-era routing features dynamically" in rendered


def test_capability_inventory_recognizes_rebuilt_artifact_mode(tmp_path: Path) -> None:
    for dirname in (
        "a0_qk_constants",
        "a1_at_functions",
        "a2_mo_composites",
        "a3_og_features",
        "a4_sy_orchestration",
    ):
        (tmp_path / dirname).mkdir()
    (tmp_path / "MANIFEST.json").write_text(
        json.dumps(
            {
                "components": [
                    {"tier": "a0_qk_constants", "name": "constant_one"},
                    {"tier": "a1_at_functions", "name": "pure_step"},
                    {"tier": "a1_at_functions", "name": "pure_step_two"},
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "CERTIFICATE.json").write_text('{"ok":true}\n', encoding="utf-8")
    (tmp_path / "REBUILD_REPORT.md").write_text("# Rebuild Report\n", encoding="utf-8")
    (tmp_path / "CHEATSHEET.md").write_text(
        """\
# Cheat Sheet

## Tools (`tools/`)

- `prompt_tool`
- `rebuild_tool`

## Hooks (`hooks/`)

- `pre_prompt_governance.py`

## Agent Definitions (`agents/`)

- `prompt-governor.agent.md`
""",
        encoding="utf-8",
    )
    nested = tmp_path / "a1_at_functions"

    snapshot = build_capability_snapshot(nested)
    rendered = render_capability_prompt_section(nested)
    dynamic_names = [item.name for item in snapshot.dynamic_abilities]

    assert snapshot.repo_root == str(tmp_path)
    assert any(
        item.name == "MANIFEST.json" and "3 components" in item.description
        for item in snapshot.surface_locations
    )
    assert any(item.name == "CHEATSHEET.md" for item in snapshot.surface_locations)
    assert any(
        item.name == "a1_at_functions/" and "2 manifest components" in item.description
        for item in snapshot.monadic_tiers
    )
    assert "rebuild-agent:prompt-governor.agent.md" in dynamic_names
    assert "rebuild-hook:pre_prompt_governance.py" in dynamic_names
    assert "rebuild-tool:prompt_tool" in dynamic_names
    assert "treat the workspace as a rebuilt artifact" in rendered


def test_atomadic_prompt_loads_agent_definition_from_agents_root(tmp_path: Path) -> None:
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "atomadic_interpreter.md").write_text(
        "# Custom Atomadic\n\nDescription: loaded from repo agent definition.\n",
        encoding="utf-8",
    )

    prompt = build_atomadic_intent_prompt(tmp_path)

    assert "# Custom Atomadic" in prompt
    assert "loaded from repo agent definition" in prompt


def test_command_path_exists_accepts_known_subcommand_with_flags(tmp_path: Path) -> None:
    assert command_path_exists(
        ["protocol", "evolution-record", "--summary", "birth"],
        tmp_path,
    )
    assert not command_path_exists(["protocol", "made-up-command"], tmp_path)


def test_agent_loop_system_prompt_uses_dynamic_inventory(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

    prompt = build_system_prompt(str(tmp_path))

    assert "Dynamic Capability Inventory" in prompt
    assert "Capability summary" in prompt
    assert "`protocol evolution-record`" in prompt
    assert "`read_file`" in prompt
    assert "Project type: Python" in prompt


def test_render_atomadic_help_mentions_runtime_inventory(tmp_path: Path) -> None:
    help_text = render_atomadic_help(tmp_path)

    assert "runtime" in help_text
    assert "Capability counts" in help_text
    assert "`protocol evolution-record`" in help_text
    assert "`context pack`" in help_text


def test_fallback_llm_prompt_still_includes_dynamic_inventory(tmp_path: Path) -> None:
    prompt = interpreter._fallback_llm_system_prompt(tmp_path, "preferred_tone=direct")

    assert "preferred_tone=direct" in prompt
    assert "Dynamic Capability Inventory" in prompt
    assert "`protocol evolution-record`" in prompt


def test_llm_router_sends_dynamic_capability_prompt(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, object] = {}

    def fake_post(url: str, **kwargs):
        captured["url"] = url
        captured["json"] = kwargs["json"]
        response = MagicMock()
        response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"type":"command","intent":"help","path":null,'
                            '"output_path":null,"feature_desc":null}'
                        )
                    }
                }
            ]
        }
        response.raise_for_status.return_value = None
        return response

    monkeypatch.setattr(interpreter, "_load_interpreter_config",
                        lambda: AssAdeConfig(llm_providers=["pollinations"]))
    monkeypatch.setattr(interpreter.httpx, "post", fake_post)

    result = interpreter._call_llm(
        "what can you do?",
        working_dir=tmp_path,
        memory_context="preferred_tone=direct",
    )

    assert result and result["intent"] == "help"
    payload = captured["json"]
    assert isinstance(payload, dict)
    system_prompt = payload["messages"][0]["content"]
    assert "Dynamic Capability Inventory" in system_prompt
    assert "Runtime routing rules" in system_prompt
    assert "`mcp serve`" in system_prompt
    assert "preferred_tone=direct" in system_prompt


def test_sync_atomadic_prompt_capabilities_replaces_generated_block(tmp_path: Path) -> None:
    prompt_path = tmp_path / "agents" / "atomadic_interpreter.md"
    prompt_path.parent.mkdir()
    prompt_path.write_text(
        "# Atomadic\n\n---\n\n## Current Capabilities\n\nold stale block\n",
        encoding="utf-8",
    )

    result = sync_atomadic_prompt_capabilities(repo_root=tmp_path, prompt_path=prompt_path)

    assert result == prompt_path
    text = prompt_path.read_text(encoding="utf-8")
    assert "old stale block" not in text
    assert "Runtime routing rules" in text
    assert "`protocol evolution-record`" in text
    assert "`prompt sync-agent`" in text


def test_atomadic_dispatches_dynamic_cli_args(monkeypatch, tmp_path: Path) -> None:
    captured: dict[str, list[str]] = {}

    def fake_call_llm(_text: str, _working_dir: Path | str | None = None, _memory_context: str | None = None) -> dict:
        return {
            "type": "command",
            "intent": "cli",
            "cli_args": ["doctor", "--json"],
            "path": None,
            "output_path": None,
            "feature_desc": None,
        }

    def fake_execute(self: Atomadic, cmd: list[str]) -> str:
        captured["cmd"] = cmd
        return '{"profile":"local"}'

    monkeypatch.setattr(interpreter, "_call_llm", fake_call_llm)
    monkeypatch.setattr(Atomadic, "_execute", fake_execute)

    agent = Atomadic(working_dir=tmp_path)
    response = agent.process("show doctor json")

    assert captured["cmd"][-2:] == ["doctor", "--json"]
    assert "Command complete" in response
