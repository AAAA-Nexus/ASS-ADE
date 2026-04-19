# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_for_model.py:7
# Component id: qk.source.a0_qk_constants.for_model
from __future__ import annotations

__version__ = "0.1.0"

def for_model(cls, model: str | None) -> TokenBudget:
    return cls(context_window=context_window_for(model))
