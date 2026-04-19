# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testbumpversion.py:7
# Component id: mo.source.a2_mo_composites.testbumpversion
from __future__ import annotations

__version__ = "0.1.0"

class TestBumpVersion:
    def test_patch(self):
        assert bump_version("0.1.3", "patch") == "0.1.4"

    def test_minor(self):
        assert bump_version("0.1.3", "minor") == "0.2.0"

    def test_major(self):
        assert bump_version("0.1.3", "major") == "1.0.0"

    def test_invalid_falls_back_to_initial(self):
        assert bump_version("not-semver", "patch") == INITIAL_VERSION

    def test_minor_resets_patch(self):
        assert bump_version("1.2.9", "minor") == "1.3.0"

    def test_major_resets_minor_and_patch(self):
        assert bump_version("2.5.7", "major") == "3.0.0"
