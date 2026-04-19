# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testaggregateversion.py:7
# Component id: mo.source.a2_mo_composites.testaggregateversion
from __future__ import annotations

__version__ = "0.1.0"

class TestAggregateVersion:
    def test_picks_highest(self):
        assert _aggregate_version(["0.1.0", "0.2.0", "0.1.5"]) == "0.2.0"

    def test_empty_list_returns_initial(self):
        assert _aggregate_version([]) == INITIAL_VERSION

    def test_single(self):
        assert _aggregate_version(["1.3.7"]) == "1.3.7"

    def test_major_wins(self):
        assert _aggregate_version(["0.9.9", "1.0.0", "0.9.8"]) == "1.0.0"
