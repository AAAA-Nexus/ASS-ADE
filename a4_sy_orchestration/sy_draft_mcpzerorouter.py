# Extracted from C:/!ass-ade/src/ass_ade/mcp/zero_router.py:16
# Component id: sy.source.ass_ade.mcpzerorouter
from __future__ import annotations

__version__ = "0.1.0"

class MCPZeroRouter:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._catalog: list[ToolRef] = []
        self._calls = 0

    def register(self, tool: ToolRef) -> None:
        self._catalog.append(tool)

    def discover(self, capability_embedding: Any, k: int = 5) -> list[ToolRef]:
        self._calls += 1
        if self._nexus is not None and hasattr(self._nexus, "discovery_search"):
            try:
                cap = capability_embedding if isinstance(capability_embedding, str) else str(capability_embedding)
                result = self._nexus.discovery_search(cap, limit=k)
                tools: list[ToolRef] = []
                items = getattr(result, "results", None) or getattr(result, "tools", None) or []
                for idx, item in enumerate(items[:k]):
                    name = getattr(item, "name", None) or (item.get("name") if isinstance(item, dict) else f"tool_{idx}")
                    score = getattr(item, "score", None) or (item.get("score") if isinstance(item, dict) else 1.0 - idx * 0.1)
                    server = getattr(item, "server", "") or (item.get("server", "") if isinstance(item, dict) else "")
                    tools.append(ToolRef(name=name, score=float(score), server=server))
                if tools:
                    return tools
            except Exception:
                pass
        return self._catalog[:k]

    def route(self, capability_str: str) -> ToolRef | None:
        candidates = self.discover(capability_str, k=1)
        return candidates[0] if candidates else None

    def run(self, ctx: dict) -> dict:
        cap = ctx.get("capability", "")
        k = int(ctx.get("k", 5))
        tools = self.discover(cap, k)
        return {"tools": [{"name": t.name, "score": t.score, "server": t.server} for t in tools]}

    def report(self) -> dict:
        return {
            "engine": "mcp_zero_router",
            "catalog_size": len(self._catalog),
            "calls": self._calls,
        }
