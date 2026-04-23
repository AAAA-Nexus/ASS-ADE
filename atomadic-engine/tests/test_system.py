import subprocess

from ass_ade import system


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
