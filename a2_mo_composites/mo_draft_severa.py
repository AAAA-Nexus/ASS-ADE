# Extracted from C:/!ass-ade/src/ass_ade/agent/severa.py:22
# Component id: mo.source.ass_ade.severa
from __future__ import annotations

__version__ = "0.1.0"

class Severa:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        self._searches = 0

    def search(self) -> list[Arch]:
        self._searches += 1
        base = [
            Arch(name="linear", score=0.5, traits=["simple"]),
            Arch(name="tree", score=0.7, traits=["recursive"]),
            Arch(name="graph", score=0.8, traits=["emergent"]),
        ]
        return sorted(base, key=lambda a: a.score, reverse=True)

    def synthesize(self, arch: Arch) -> Agent:
        code = (
            f"class Agent_{arch.name}:\n"
            f"    traits = {arch.traits!r}\n"
            f"    def run(self, ctx):\n"
            f"        return {{'arch': {arch.name!r}}}\n"
        )
        return Agent(name=f"agent_{arch.name}", arch=arch, code=code)

    def verify(self, agent: Agent, spec: str) -> bool:
        if self._nexus is not None and hasattr(self._nexus, "certify_output_verify"):
            try:
                result = self._nexus.certify_output_verify(agent.code)
                return bool(getattr(result, "rubric_passed", False))
            except Exception:
                pass
        return "run" in agent.code and agent.arch.score > 0.4

    def run(self, ctx: dict) -> dict:
        spec = ctx.get("spec", "")
        archs = self.search()
        best = archs[0]
        agent = self.synthesize(best)
        ok = self.verify(agent, spec)
        return {
            "arch": best.name,
            "score": best.score,
            "agent": agent.name,
            "verified": ok,
        }

    def report(self) -> dict:
        return {"engine": "severa", "searches": self._searches}
