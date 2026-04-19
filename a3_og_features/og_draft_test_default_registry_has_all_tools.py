# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:186
# Component id: og.source.ass_ade.test_default_registry_has_all_tools
from __future__ import annotations

__version__ = "0.1.0"

def test_default_registry_has_all_tools(self, workspace: Path):
    reg = default_registry(str(workspace))
    names = reg.list_tools()
    assert "read_file" in names
    assert "write_file" in names
    assert "edit_file" in names
    assert "run_command" in names
    assert "list_directory" in names
    assert "search_files" in names
    assert "grep_search" in names
