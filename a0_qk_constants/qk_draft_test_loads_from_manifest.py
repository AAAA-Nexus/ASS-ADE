# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testloadprevversions.py:12
# Component id: qk.source.ass_ade.test_loads_from_manifest
__version__ = "0.1.0"

    def test_loads_from_manifest(self, tmp_path: Path):
        manifest = {
            "components": [
                {
                    "id": "at.foo",
                    "version": "0.2.1",
                    "body_hash": "abc123",
                    "body": "def foo(): pass",
                }
            ]
        }
        p = tmp_path / "MANIFEST.json"
        p.write_text(json.dumps(manifest), encoding="utf-8")
        result = load_prev_versions(p)
        assert "at.foo" in result
        assert result["at.foo"]["version"] == "0.2.1"
        assert result["at.foo"]["body_hash"] == "abc123"
