# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_stubs_created_list.py:7
# Component id: at.source.a1_at_functions.test_stubs_created_list
from __future__ import annotations

__version__ = "0.1.0"

def test_stubs_created_list(self, tmp_path):
    from ass_ade.map_terrain import active_terrain_gate
    result = active_terrain_gate(
        ["missing_engine_alpha"],
        working_dir=str(tmp_path),
        write_stubs=False,  # don't write to disk in tests
    )
    assert len(result.stubs_created) == 1
    assert result.stubs_created[0].capability_name == "missing_engine_alpha"
