# Extracted from C:/!ass-ade/tests/test_system.py:11
# Component id: sy.source.ass_ade.fake_run
from __future__ import annotations

__version__ = "0.1.0"

def fake_run(args, **kwargs):
    calls.append(args)
    return subprocess.CompletedProcess(args=args, returncode=0, stdout="11.9.0\n", stderr="")
