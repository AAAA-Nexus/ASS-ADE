# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testmcpserver.py:43
# Component id: sy.source.ass_ade.test_tools_call_read_file
__version__ = "0.1.0"

    def test_tools_call_read_file(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "read_file", "arguments": {"path": "hello.py"}},
        }
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"]["isError"] is False
        content = resp["result"]["content"][0]["text"]
        assert "print('hi')" in content
