# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1142
# Component id: at.source.ass_ade.data_validate_json
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
