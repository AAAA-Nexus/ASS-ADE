# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_compliance_oversight_history_happy_path.py:9
# Component id: at.source.a1_at_functions.handler
from __future__ import annotations

__version__ = "0.1.0"

def handler(request):
    return httpx.Response(200, json={"history": [{"reviewer": "rev1", "decision": "approved"}]})
