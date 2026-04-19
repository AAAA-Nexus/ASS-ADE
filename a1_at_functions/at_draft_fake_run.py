# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_detect_tool_uses_resolved_executable.py:12
# Component id: at.source.a1_at_functions.fake_run
from __future__ import annotations

__version__ = "0.1.0"

def fake_run(args, **kwargs):
    calls.append(args)
    return subprocess.CompletedProcess(args=args, returncode=0, stdout="11.9.0\n", stderr="")
