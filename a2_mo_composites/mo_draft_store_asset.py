# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_edee.py:32
# Component id: mo.source.ass_ade.store_asset
__version__ = "0.1.0"

    def store_asset(self, asset: dict) -> str:
        text = asset.get("summary") or asset.get("name") or str(asset)[:200]
        meta = {"kind": "asset", "asset": asset}
        result = store_vector_memory(
            text=text,
            namespace=ASSET_NS,
            metadata=meta,
            working_dir=self._working_dir,
        )
        self._assets += 1
        return result.id
