# Extracted from C:/!ass-ade/src/ass_ade/agent/proofbridge.py:32
# Component id: qk.source.ass_ade.translate
from __future__ import annotations

__version__ = "0.1.0"

def translate(self, task_description: str) -> Lean4Spec:
    self._translations += 1
    if self._nexus is not None and hasattr(self._nexus, "synthesize_verified_code"):
        try:
            result = self._nexus.synthesize_verified_code(
                description=task_description, language="lean4"
            )
            source = getattr(result, "source", None) or getattr(result, "code", None)
            if source:
                return Lean4Spec(
                    name=self._spec_name(task_description),
                    source=str(source),
                    has_sorry="sorry" in str(source),
                )
        except Exception:
            pass
    name = self._spec_name(task_description)
    src = (
        f"-- spec: {task_description}\n"
        f"theorem {name} : True := by\n"
        f"  sorry\n"
    )
    return Lean4Spec(name=name, source=src, has_sorry=True)
