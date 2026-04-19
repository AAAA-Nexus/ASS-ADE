# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detect_tool_uses_resolved_executable.py:7
# Component id: at.source.a1_at_functions.test_detect_tool_uses_resolved_executable
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_tool_uses_resolved_executable(monkeypatch) -> None:
    calls = []

    monkeypatch.setattr(system, "which", lambda name: "C:/Program Files/nodejs/npm.CMD")

    def fake_run(args, **kwargs):
        calls.append(args)
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="11.9.0\n", stderr="")

    monkeypatch.setattr(system.subprocess, "run", fake_run)

    status = system.detect_tool("npm")

    assert status.available is True
    assert status.version == "11.9.0"
    assert calls == [["C:/Program Files/nodejs/npm.CMD", "--version"]]
