# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/edee.py:24
# Component id: mo.source.ass_ade.edee
__version__ = "0.1.0"

class EDEE:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._working_dir = config.get("working_dir", ".")
        self._traces = 0
        self._assets = 0
        self._exif = None

    def _get_exif(self):
        if self._exif is None:
            from ass_ade.agent.exif import EXIF
            self._exif = EXIF(self._config, self._nexus)
        return self._exif

    def capture_trace(self, phase: str, data: dict) -> str:
        text = f"[{phase}] {data.get('summary', str(data)[:200])}"
        meta = {"phase": phase, "data": data, "kind": "trace"}
        result = store_vector_memory(
            text=text,
            namespace=EXPERIENCE_NS,
            metadata=meta,
            working_dir=self._working_dir,
        )
        self._traces += 1
        return result.id

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

    def recall(self, task_embedding: Any, k: int = 5) -> list[dict]:
        q = task_embedding if isinstance(task_embedding, str) else str(task_embedding)
        result = query_vector_memory(
            query=q,
            namespace=EXPERIENCE_NS,
            top_k=k,
            working_dir=self._working_dir,
        )
        return [{"id": m.id, "score": m.score, "text": m.text, "metadata": m.metadata} for m in result.matches]

    def distill_principles(self) -> list[Principle]:
        result = query_vector_memory(
            query="principle",
            namespace=EXPERIENCE_NS,
            top_k=10,
            working_dir=self._working_dir,
        )
        return [
            Principle(text=m.text, weight=m.score, source_traces=1)
            for m in result.matches
        ]

    def exif_explore(self, missing_skill: str, env: dict | None = None):
        return self._get_exif().explore(missing_skill, env or {"name": "default"})

    def run(self, ctx: dict) -> dict:
        op = ctx.get("op", "recall")
        if op == "capture":
            return {"id": self.capture_trace(ctx.get("phase", "unknown"), ctx.get("data", {}))}
        if op == "asset":
            return {"id": self.store_asset(ctx.get("asset", {}))}
        if op == "distill":
            return {"principles": [p.__dict__ for p in self.distill_principles()]}
        return {"matches": self.recall(ctx.get("query", ""), int(ctx.get("k", 5)))}

    def report(self) -> dict:
        return {
            "engine": "edee",
            "traces": self._traces,
            "assets": self._assets,
        }
