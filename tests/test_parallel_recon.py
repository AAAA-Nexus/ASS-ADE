"""Tests for the parallel recon system (5 agents + ReconReport)."""
from __future__ import annotations

import ast
import textwrap
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.recon import (
    ReconReport,
    _classify_tier,
    _count_test_functions,
    _dependency_agent,
    _doc_agent,
    _iter_files,
    _scout_agent,
    _test_agent,
    _tier_agent,
    run_parallel_recon,
)

runner = CliRunner()


# ── fixtures ──────────────────────────────────────────────────────────────────


def _seed_full_repo(root: Path) -> None:
    """Seed a representative repo for recon tests."""
    src = root / "src" / "myproject"
    tests = root / "tests"
    docs = root / "docs"
    src.mkdir(parents=True)
    tests.mkdir()
    docs.mkdir()

    # README
    (root / "README.md").write_text("# My Project\n\nA demo repo.\n", encoding="utf-8")

    # qk: constants only
    (src / "constants.py").write_text(
        "MAX_RETRIES = 3\nTIMEOUT = 30\nVERSION = '1.0.0'\n",
        encoding="utf-8",
    )

    # at: pure functions, no classes
    (src / "utils.py").write_text(
        textwrap.dedent("""\
        def add(a, b):
            return a + b

        def subtract(a, b):
            return a - b
        """),
        encoding="utf-8",
    )

    # mo: stateful class
    (src / "session.py").write_text(
        textwrap.dedent("""\
        class Session:
            def __init__(self, user_id):
                self.user_id = user_id
                self.active = False

            def start(self):
                self.active = True
        """),
        encoding="utf-8",
    )

    # og: feature module — classes + functions + state
    (src / "manager.py").write_text(
        textwrap.dedent("""\
        from myproject.session import Session

        class Manager:
            def __init__(self):
                self.sessions = {}

            def create(self, uid):
                s = Session(uid)
                self.sessions[uid] = s
                return s

        def get_count(manager):
            return len(manager.sessions)
        """),
        encoding="utf-8",
    )

    # sy: orchestration
    (src / "app.py").write_text(
        textwrap.dedent("""\
        from myproject.manager import Manager
        from myproject.session import Session
        from myproject.utils import add
        from myproject.constants import MAX_RETRIES

        def main():
            m = Manager()
            m.create('user1')

        if __name__ == '__main__':
            main()
        """),
        encoding="utf-8",
    )

    # __init__
    (src / "__init__.py").write_text("", encoding="utf-8")

    # test file
    (tests / "test_utils.py").write_text(
        textwrap.dedent("""\
        import pytest
        from myproject.utils import add, subtract

        def test_add():
            assert add(1, 2) == 3

        def test_subtract():
            assert subtract(5, 3) == 2
        """),
        encoding="utf-8",
    )

    # doc file
    (docs / "guide.md").write_text("# Guide\n\nUsage details.\n", encoding="utf-8")


# ── _iter_files ───────────────────────────────────────────────────────────────


def test_iter_files_respects_limit(tmp_path: Path) -> None:
    for i in range(20):
        (tmp_path / f"f{i}.py").write_text("x=1", encoding="utf-8")
    files = _iter_files(tmp_path, limit=10)
    assert len(files) == 10


def test_iter_files_skips_ignored_dirs(tmp_path: Path) -> None:
    venv = tmp_path / ".venv"
    venv.mkdir()
    (venv / "pkg.py").write_text("x=1", encoding="utf-8")
    (tmp_path / "main.py").write_text("x=1", encoding="utf-8")
    files = _iter_files(tmp_path)
    names = [f.name for f in files]
    assert "main.py" in names
    assert "pkg.py" not in names


# ── ScoutAgent ────────────────────────────────────────────────────────────────


def test_scout_basic_counts(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _scout_agent(tmp_path, files)

    assert result["total_files"] > 0
    assert result["total_size_kb"] > 0
    assert result["max_depth"] >= 1
    assert isinstance(result["top_level"], list)
    assert ".py" in result["by_extension"]
    assert result["source_files"] > 0


def test_scout_empty_dir(tmp_path: Path) -> None:
    result = _scout_agent(tmp_path, [])
    assert result["total_files"] == 0
    assert result["total_size_kb"] == 0


# ── DependencyAgent ───────────────────────────────────────────────────────────


def test_dependency_finds_external_deps(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)

    assert result["python_files"] > 0
    assert isinstance(result["unique_external_deps"], int)
    assert isinstance(result["circular_deps"], list)
    assert isinstance(result["max_import_depth"], int)


def test_dependency_detects_circular(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("from b import x\n", encoding="utf-8")
    (tmp_path / "b.py").write_text("from a import y\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)
    assert result["has_circular_deps"] is True


def test_dependency_no_circular_clean_repo(tmp_path: Path) -> None:
    (tmp_path / "utils.py").write_text("def add(a, b): return a + b\n", encoding="utf-8")
    (tmp_path / "main.py").write_text("from utils import add\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _dependency_agent(tmp_path, files)
    assert result["has_circular_deps"] is False


# ── TierAgent ─────────────────────────────────────────────────────────────────


def test_classify_tier_qk(tmp_path: Path) -> None:
    f = tmp_path / "constants.py"
    f.write_text("MAX = 3\nTIMEOUT = 30\n", encoding="utf-8")
    assert _classify_tier(f) == "qk"


def test_classify_tier_at(tmp_path: Path) -> None:
    f = tmp_path / "utils.py"
    f.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    assert _classify_tier(f) == "at"


def test_classify_tier_mo(tmp_path: Path) -> None:
    f = tmp_path / "session.py"
    f.write_text(
        "class Session:\n"
        "    def __init__(self, uid):\n"
        "        self.uid = uid\n",
        encoding="utf-8",
    )
    assert _classify_tier(f) == "mo"


def test_classify_tier_sy(tmp_path: Path) -> None:
    f = tmp_path / "app.py"
    f.write_text(
        "import os\nimport sys\nimport json\n"
        "def main(): pass\n"
        "if __name__ == '__main__':\n    main()\n",
        encoding="utf-8",
    )
    assert _classify_tier(f) == "sy"


def test_tier_agent_counts(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _tier_agent(tmp_path, files)

    assert result["total_py_files"] > 0
    assert sum(result["tier_distribution"].values()) == result["total_py_files"]
    assert result["dominant_tier"] in ("qk", "at", "mo", "og", "sy")


# ── TestAgent ─────────────────────────────────────────────────────────────────


def test_count_test_functions(tmp_path: Path) -> None:
    f = tmp_path / "test_utils.py"
    f.write_text(
        "def test_add(): assert True\ndef test_sub(): assert True\ndef helper(): pass\n",
        encoding="utf-8",
    )
    assert _count_test_functions(f) == 2


def test_test_agent_finds_tests(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _test_agent(tmp_path, files)

    assert result["test_files"] >= 1
    assert result["test_functions"] >= 2
    assert "pytest" in result["frameworks"]
    assert isinstance(result["coverage_ratio"], float)


def test_test_agent_empty(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("def run(): pass\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _test_agent(tmp_path, files)
    assert result["test_files"] == 0
    assert result["test_functions"] == 0
    assert result["coverage_ratio"] == 0.0


# ── DocAgent ──────────────────────────────────────────────────────────────────


def test_doc_agent_finds_readme(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["has_readme"] is True


def test_doc_agent_no_readme(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("def run(): pass\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["has_readme"] is False


def test_doc_agent_coverage(tmp_path: Path) -> None:
    f = tmp_path / "module.py"
    f.write_text(
        'def good():\n    """Docs here."""\n    pass\n'
        "def bad():\n    pass\n",
        encoding="utf-8",
    )
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["doc_coverage"] == 0.5
    assert result["total_public_callables"] == 2


# ── run_parallel_recon ────────────────────────────────────────────────────────


def test_run_parallel_recon_returns_report(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)

    assert isinstance(report, ReconReport)
    assert report.root == str(tmp_path)
    assert report.duration_ms >= 0
    assert report.scout["total_files"] > 0
    assert isinstance(report.recommendations, list)
    assert len(report.recommendations) > 0
    assert report.next_action


def test_run_parallel_recon_completes_fast(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    import time
    t0 = time.monotonic()
    run_parallel_recon(tmp_path)
    elapsed = time.monotonic() - t0
    assert elapsed < 5.0, f"Recon took {elapsed:.2f}s — exceeded 5s budget"


def test_run_parallel_recon_summary_is_string(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)
    assert isinstance(report.summary, str)
    assert len(report.summary) > 20


def test_run_parallel_recon_to_markdown(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)
    md = report.to_markdown()
    assert "# RECON_REPORT" in md
    assert "## Scout" in md
    assert "## Dependencies" in md
    assert "## Tier Distribution" in md
    assert "## Tests" in md
    assert "## Documentation" in md


def test_run_parallel_recon_to_dict(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)
    d = report.to_dict()
    assert "scout" in d
    assert "dependency" in d
    assert "tier" in d
    assert "test" in d
    assert "doc" in d
    assert "summary" in d


def test_run_parallel_recon_empty_dir(tmp_path: Path) -> None:
    report = run_parallel_recon(tmp_path)
    assert report.scout["total_files"] == 0
    assert report.test["test_files"] == 0
    assert not report.doc["has_readme"]


# ── CLI command ───────────────────────────────────────────────────────────────


def test_cli_recon_default_markdown(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    result = runner.invoke(app, ["recon", str(tmp_path)])
    assert result.exit_code == 0
    assert "RECON_REPORT" in result.output


def test_cli_recon_json_flag(tmp_path: Path) -> None:
    import json
    _seed_full_repo(tmp_path)
    result = runner.invoke(app, ["recon", str(tmp_path), "--json"])
    assert result.exit_code == 0
    # JSON output should be parseable
    # The output may be Rich-rendered; extract the JSON block
    lines = result.output.strip().splitlines()
    # Find the first line that looks like JSON
    json_start = next((i for i, l in enumerate(lines) if l.strip().startswith("{")), None)
    assert json_start is not None, "No JSON block found in output"
    json_text = "\n".join(lines[json_start:])
    # Remove any trailing non-JSON lines
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        # Try to find the closing brace
        depth = 0
        end = 0
        for i, ch in enumerate(json_text):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        data = json.loads(json_text[:end])
    assert "scout" in data
    assert "test" in data


def test_cli_recon_out_flag(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    out_file = tmp_path / "report.md"
    result = runner.invoke(app, ["recon", str(tmp_path), "--out", str(out_file)])
    assert result.exit_code == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "RECON_REPORT" in content


def test_cli_recon_missing_path(tmp_path: Path) -> None:
    nonexistent = tmp_path / "does_not_exist"
    result = runner.invoke(app, ["recon", str(nonexistent)])
    assert result.exit_code != 0
