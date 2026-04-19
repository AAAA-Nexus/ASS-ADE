# Extracted from C:/!ass-ade/tests/test_agent.py:64
# Component id: at.source.ass_ade.test_contains_working_dir
from __future__ import annotations

__version__ = "0.1.0"

def test_contains_working_dir(self, tmp_path):
    prompt = build_system_prompt(str(tmp_path))
    assert "ASS-ADE" in prompt
    assert str(tmp_path) in prompt
