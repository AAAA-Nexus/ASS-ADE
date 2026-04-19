# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_data_validate_json.py:7
# Component id: at.source.a1_at_functions.data_validate_json
from __future__ import annotations

__version__ = "0.1.0"

def data_validate_json(
    self,
    data: dict | None = None,
    schema: dict | None = None,
    *,
    payload: dict | None = None,
    **kwargs: Any,
) -> DataValidation:
    """/v1/data/validate-json — JSON schema validation with error paths. $0.012/request"""
    return self._post_model("/v1/data/validate-json", DataValidation, {"data": data or payload or {}, "schema": schema or {}, **kwargs})
