# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testregistry.py:7
# Component id: og.source.a3_og_features.testregistry
from __future__ import annotations

__version__ = "0.1.0"

class TestRegistry:
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

    def test_execute_unknown(self, workspace: Path):
        reg = default_registry(str(workspace))
        r = reg.execute("no_such_tool")
        assert not r.success
        assert "Unknown tool" in (r.error or "")

    def test_schemas(self, workspace: Path):
        reg = default_registry(str(workspace))
        schemas = reg.schemas()
        assert len(schemas) == len(reg.list_tools())
        assert all(s.name for s in schemas)
