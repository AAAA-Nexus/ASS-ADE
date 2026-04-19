# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testbuildsystemprompt.py:8
# Component id: sy.source.a4_sy_orchestration.test_contains_working_dir
from __future__ import annotations

__version__ = "0.1.0"

def test_contains_working_dir(self, tmp_path):
    prompt = build_system_prompt(str(tmp_path))
    assert "ASS-ADE" in prompt
    assert str(tmp_path) in prompt
