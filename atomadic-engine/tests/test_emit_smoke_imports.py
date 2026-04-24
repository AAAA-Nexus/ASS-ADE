"""Auto-emitted import smoke tests (fail fast on missing runtime deps)."""


def test_jsonschema_importable() -> None:
    import jsonschema  # noqa: F401


def test_mcp_utils_importable() -> None:
    import ass_ade.mcp.utils  # noqa: F401


def test_cli_module_importable() -> None:
    import ass_ade.cli  # noqa: F401
