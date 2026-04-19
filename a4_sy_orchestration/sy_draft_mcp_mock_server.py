# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1063
# Component id: sy.source.ass_ade.mcp_mock_server
__version__ = "0.1.0"

def mcp_mock_server(
    port: int = typer.Option(8787, help="TCP port to listen on."),
    manifest: Path | None = typer.Option(None, help="Path to a JSON manifest file to serve."),
) -> None:
    """Start a local mock MCP server for development and integration testing.

    Serves the manifest at http://localhost:<port>/.well-known/mcp.json and
    echoes POST payloads back. No remote access required.
    """
    console.print(f"Starting mock MCP server on http://127.0.0.1:{port} (Ctrl+C to stop)")
    if manifest is not None:
        console.print(f"Serving manifest from {manifest}")
    _mock_server.start_server(port=port, manifest_path=manifest, block=True)
