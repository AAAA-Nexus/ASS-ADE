# Extracted from C:/!ass-ade/src/ass_ade/mcp/utils.py:132
# Component id: at.source.ass_ade.validate_payload
from __future__ import annotations

__version__ = "0.1.0"

def validate_payload(schema: dict | None, payload: Any | None) -> tuple[bool, str | None]:
    """Validate the given payload against the provided JSON Schema.

    Returns (True, None) when valid, otherwise (False, error_message).
    """
    if schema is None:
        return True, None

    try:
        # jsonschema expects a concrete instance; use None -> {} for convenience
        instance = payload if payload is not None else {}
        jsonschema.validate(instance=instance, schema=schema)
        return True, None
    except ValidationError as exc:
        return False, str(exc)
    except jsonschema.SchemaError as exc:
        return False, f"schema validation error: {exc}"
