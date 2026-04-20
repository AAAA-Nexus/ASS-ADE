from __future__ import annotations

import json
from pathlib import Path

from scripts import ass_ade_local_control as lc


def test_ensure_control_tree_creates_expected_dirs(tmp_path: Path) -> None:
    root = tmp_path / "control"

    doc = lc.ensure_control_tree(root)

    assert doc["schema"] == lc.CONTROL_SCHEMA
    assert (root / "evo" / "worktrees").is_dir()
    assert (root / "evo" / "merge-siblings").is_dir()
    assert (root / "outputs" / "experiments").is_dir()
    assert (root / "inventory").is_dir()
    assert (root / "CONTROL_ROOT.json").is_file()


def test_stamp_and_validate_output(tmp_path: Path) -> None:
    output = tmp_path / "rb"
    output.mkdir()
    (output / "MANIFEST.json").write_text("{}", encoding="utf-8")
    (output / "CERTIFICATE.json").write_text('{"certificate_sha256":"0"}', encoding="utf-8")
    (output / "REBUILD_REPORT.md").write_text(
        "\n".join(
            [
                "# Rebuild Report",
                "**Rebuild tag**: `20260420_000000`",
                "| Components written | 3 |",
                "| `a0_qk_constants` | 1 |",
                "| `a1_at_functions` | 2 |",
                "- **Pass rate**: 100.0%",
            ]
        ),
        encoding="utf-8",
    )

    metadata = lc.build_output_metadata(
        output,
        output_class="experiment",
        lane="quality",
        source=None,
        branch="evo/quality/test",
        slug="unit-test",
        parent_output_id=None,
        pin=False,
    )
    lc.write_json(output / "ASS_ADE_OUTPUT.json", metadata)

    result = lc.validate_output(output)

    assert result["valid"] is True
    assert result["metadata"]["schema"] == lc.OUTPUT_SCHEMA
    assert result["metadata"]["artifacts"]["components_written"] == 3


def test_validate_output_requires_metadata(tmp_path: Path) -> None:
    output = tmp_path / "rb"
    output.mkdir()

    result = lc.validate_output(output)

    assert result["valid"] is False
    assert "missing ASS_ADE_OUTPUT.json" in result["errors"]


def _write_min_repo(root: Path, *, capability_status: str, extra_command: bool = False) -> None:
    (root / "src" / "ass_ade").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "docs").mkdir()
    (root / "capabilities").mkdir()
    (root / "pyproject.toml").write_text('[project]\nversion = "1.0.0"\n', encoding="utf-8")
    (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (root / "src" / "ass_ade" / "__init__.py").write_text('__version__ = "1.0.0"\n', encoding="utf-8")
    cli = [
        "import typer",
        "app = typer.Typer()",
        "",
        "@app.command()",
        "def doctor():",
        "    pass",
    ]
    if extra_command:
        cli.extend(
            [
                "",
                "feature_app = typer.Typer()",
                "app.add_typer(feature_app, name=\"feature\")",
                "",
                "@feature_app.command(\"gain\")",
                "def feature_gain():",
                "    pass",
            ]
        )
    (root / "src" / "ass_ade" / "cli.py").write_text("\n".join(cli), encoding="utf-8")
    registry = {
        "schema": lc.CAPABILITY_SCHEMA,
        "capabilities": [
            {
                "id": "core.public_cli",
                "name": "Public CLI",
                "area": "core",
                "status": "complete",
                "evidence": ["src/ass_ade/cli.py"],
            },
            {
                "id": "agent.durable_memory",
                "name": "Durable memory",
                "area": "agent",
                "status": capability_status,
                "evidence": [],
            },
        ],
    }
    (root / "capabilities" / "registry.json").write_text(json.dumps(registry), encoding="utf-8")
    (root / "tests" / "test_smoke.py").write_text("def test_smoke():\n    assert True\n", encoding="utf-8")
    (root / "docs" / "README.md").write_text("# Docs\n", encoding="utf-8")


def test_stress_gain_detects_added_command_and_capability_improvement(tmp_path: Path) -> None:
    base = tmp_path / "base"
    candidate = tmp_path / "candidate"
    _write_min_repo(base, capability_status="missing")
    _write_min_repo(candidate, capability_status="partial", extra_command=True)

    base_snapshot = lc.feature_snapshot(base)
    candidate_snapshot = lc.feature_snapshot(candidate)
    report = lc.compare_snapshots(base_snapshot, candidate_snapshot)

    assert report["passed"] is True
    assert report["growth_signals"]["capabilities_improved"] == 1
    assert report["growth_signals"]["cli_commands_added"] == 1
    assert report["added"]["cli_commands"] == ["feature gain"]


def test_validate_registry_and_render_capability_matrix(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _write_min_repo(repo, capability_status="partial")

    result = lc.validate_registry(repo)
    markdown = lc.render_capability_matrix(repo)

    assert result["valid"] is True
    assert result["capability_count"] == 2
    assert "`agent.durable_memory`" in markdown
    assert "PARTIAL" in markdown


def test_diff_inventories_reports_role_and_metadata_changes(tmp_path: Path) -> None:
    before = {
        "schema": "ass-ade.local-inventory.v1",
        "siblings": [
            {
                "name": "ass-ade-a",
                "path": "C:/ass-ade-a",
                "role": "unclassified",
                "has_output_metadata": False,
                "git": {"dirty_items": 2},
            }
        ],
    }
    after = {
        "schema": "ass-ade.local-inventory.v1",
        "siblings": [
            {
                "name": "ass-ade-a",
                "path": "C:/ass-ade-a",
                "role": "rebuild-output",
                "has_output_metadata": True,
                "git": {"dirty_items": 0},
            }
        ],
    }
    before_path = tmp_path / "before.json"
    after_path = tmp_path / "after.json"
    before_path.write_text(json.dumps(before), encoding="utf-8")
    after_path.write_text(json.dumps(after), encoding="utf-8")

    report = lc.diff_json_files(before_path, after_path)

    assert report["specialized"]["role_changes"][0]["to"] == "rebuild-output"
    assert report["specialized"]["metadata_changes"][0]["to"] is True
    assert report["specialized"]["dirty_changes"][0]["to"] == 0


def test_ingest_control_json_builds_index_and_docs(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    parent = tmp_path / "parent"
    control = tmp_path / "control"
    output = parent / "ass-ade-output"
    _write_min_repo(repo, capability_status="partial")
    lc.ensure_control_tree(control)
    output.mkdir(parents=True)
    (output / "MANIFEST.json").write_text("{}", encoding="utf-8")
    (output / "CERTIFICATE.json").write_text("{}", encoding="utf-8")
    metadata = lc.build_output_metadata(
        output,
        output_class="candidate",
        lane="features",
        source=repo,
        branch="evo/features/test",
        slug="feature-test",
        parent_output_id=None,
        pin=False,
    )
    lc.write_json(output / "ASS_ADE_OUTPUT.json", metadata)
    inventory = lc.inventory_siblings(parent, control)
    lc.write_json(control / "inventory" / "latest.json", inventory)
    lc.write_json(control / "outputs" / "stress" / "sample-report.json", {"schema": "ass-ade.feature-gain-report.v1", "passed": True})

    index = lc.ingest_control_json(repo, control, parent)
    docs = lc.generate_docs(repo, control)

    assert index["registry"]["valid"] is True
    assert len(index["outputs"]) == 1
    assert len(index["stress"]) == 1
    assert (control / "CONTROL_INDEX.json").is_file()
    assert Path(docs["outputs"]["local_control_status"]).is_file()
    assert Path(docs["outputs"]["mermaid_diagrams"]).is_file()
    assert Path(docs["outputs"]["diagram_local_control"]).read_text(encoding="utf-8").startswith("flowchart")
    assert "capabilities/registry.json" in Path(docs["outputs"]["diagram_capability_status"]).read_text(encoding="utf-8")


def test_mermaid_renderers_use_json_ledgers(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    parent = tmp_path / "parent"
    control = tmp_path / "control"
    _write_min_repo(repo, capability_status="partial")
    lc.ensure_control_tree(control)
    (parent / "ass-ade-output").mkdir(parents=True)
    lc.write_json(control / "inventory" / "latest.json", lc.inventory_siblings(parent, control))
    lc.write_json(control / "CONTROL_INDEX.json", {"schema": "ass-ade.control-index.v1", "outputs": [], "stress": []})

    local = lc.render_local_control_mermaid(control)
    status = lc.render_capability_status_mermaid(repo)
    lifecycle = lc.render_json_lifecycle_mermaid()

    assert "flowchart TD" in local
    assert "flowchart LR" in status
    assert "CONTROL_INDEX.json" in lifecycle
