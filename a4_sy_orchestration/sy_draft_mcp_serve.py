# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1079
# Component id: sy.source.ass_ade.mcp_serve
__version__ = "0.1.0"

def mcp_serve(
    working_dir: Path = typer.Option(
        Path("."), exists=True, file_okay=False, help="Working directory for tools."
    ),
) -> None:
    """Start ASS-ADE as an MCP tool server (stdio transport).

    Exposes all built-in tools over the Model Context Protocol for use
    with VS Code Copilot, Claude Desktop, or any MCP-compatible client.

    Example mcpServers config for VS Code settings.json:
        "ass-ade": { "command": "ass-ade", "args": ["mcp", "serve"] }
    """
    from ass_ade.mcp.server import MCPServer

    server = MCPServer(working_dir=str(working_dir.resolve()))
    server.run()
