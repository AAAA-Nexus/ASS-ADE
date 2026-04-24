from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.config import AssAdeConfig
from ass_ade.local import scout as scout_mod
from ass_ade.local.scout import scout_repo


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_scout_repo_static_report_with_benefit_mapping(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    repo = tmp_path / "candidate"
    _write(primary / "pkg.py", "def existing(value):\n    return value\n")
    _write(
        repo / "pyproject.toml",
        '[project]\nname = "candidate"\ndependencies = ["httpx"]\n',
    )
    _write(
        repo / "candidate.py",
        '''
def existing(value):
    """Improve existing behavior."""
    return value.strip()


def useful_feature(value):
    """Useful feature."""
    return value.upper()
''',
    )
    _write(repo / "tests" / "test_candidate.py", "def test_useful_feature():\n    assert True\n")

    report = scout_repo(repo, benefit_root=primary, use_llm=False)

    assert report["schema_version"] == "ass-ade.scout/v1"
    assert report["llm"]["status"] == "skipped"
    assert report["symbol_summary"]["symbols"] >= 2
    assert report["target_map"]["action_counts"]["enhance"] >= 1
    assert report["target_map"]["action_counts"]["assimilate"] >= 1
    assert report["static_recommendations"]


def test_cli_scout_writes_json_without_llm(tmp_path: Path) -> None:
    repo = tmp_path / "candidate"
    out = tmp_path / "scout.json"
    _write(repo / "README.md", "# Candidate\n")
    _write(repo / "app.py", "def run() -> int:\n    return 1\n")

    result = CliRunner().invoke(
        app,
        ["scout", str(repo), "--no-llm", "--json-out", str(out)],
    )

    assert result.exit_code == 0, result.stdout + (result.stderr or "")
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["repo"] == str(repo.resolve())
    assert payload["llm"]["status"] == "skipped"
    assert payload["traits"]["docs"] == ["README.md"]


def test_local_grounding_guard_flags_unsupported_opportunity() -> None:
    report = {
        "traits": {},
        "dependencies": {},
        "target_map": {"targets": [{"symbol": {"qualname": "known_feature"}}]},
        "enhancement": {},
        "symbol_summary": {},
    }
    analysis = {
        "opportunities": [
            {
                "action": "assimilate",
                "target": "unknown_feature",
                "reason": "sounds useful",
                "confidence": 0.9,
                "evidence": "not in evidence",
            }
        ]
    }

    result = scout_mod._local_grounding_guard(report, analysis)

    assert result["status"] == "caution"
    assert result["unsupported"]


def test_nexus_guard_synthesis_uses_trust_hallucination_cert_and_drift(
    monkeypatch,
) -> None:
    calls: list[str] = []

    class FakeModel:
        def __init__(self, **payload):
            self.payload = payload

        def model_dump(self):
            return dict(self.payload)

    class FakeClient:
        def trust_score(self, agent_id: str):
            calls.append(f"trust:{agent_id}")
            return FakeModel(score=0.9, tier="gold")

        def hallucination_oracle(self, text: str):
            calls.append("hallucination")
            return FakeModel(verdict="safe", confidence=0.91)

        def certify_output(self, output: str, rubric: list[str]):
            calls.append("certify")
            return FakeModel(rubric_passed=True, score=0.88, certificate_id="cert_1")

        def drift_check(self, model_id: str, reference_data: dict, current_data: dict):
            calls.append(f"drift:{model_id}")
            return FakeModel(drift_detected=False, psi_score=0.02, bound=0.2)

        def close(self):
            calls.append("close")

    monkeypatch.setattr(scout_mod, "_nexus_client_for_guards", lambda settings: FakeClient())
    report = {
        "target_map": {"action_counts": {"assimilate": 1}},
        "static_recommendations": [{"type": "assimilate"}],
    }
    analysis = {
        "summary": "ok",
        "opportunities": [
            {"action": "assimilate", "target": "known_feature", "evidence": "target-map"}
        ],
    }

    result = scout_mod._nexus_guard_synthesis(
        report=report,
        analysis=analysis,
        settings=AssAdeConfig(agent_id="agent-test"),
        model_id="model-test",
    )

    assert result["status"] == "ok"
    assert result["passed"] is True
    assert calls == ["trust:agent-test", "hallucination", "certify", "drift:model-test", "close"]
