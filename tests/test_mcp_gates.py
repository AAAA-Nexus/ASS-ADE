"""Tests for the MCP IDE gates: TCA record, NCB contract, CIE validate, LoRA capture."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ass_ade.mcp.server import MCPServer


def _make_server(tmp_path: Path) -> MCPServer:
    return MCPServer(working_dir=str(tmp_path))


def _mk_args(path: Path, **extra):
    return {"path": str(path), **extra}


# ─────────────────────────────────────────────────────────────────────────────
# TCA record_read fires on MCP read_file
# ─────────────────────────────────────────────────────────────────────────────


class TestTCARecordOnReadFile:
    def test_read_file_records_freshness(self, tmp_path):
        target = tmp_path / "example.py"
        target.write_text("x = 1\n")
        server = _make_server(tmp_path)

        result = MagicMock(success=True, output="x = 1\n")
        server._post_tool_hook("read_file", _mk_args(target), result)

        assert server.tca.ncb_contract(target) is True

    def test_read_file_failure_does_not_record(self, tmp_path):
        target = tmp_path / "missing.py"
        server = _make_server(tmp_path)
        result = MagicMock(success=False, error="not found")
        server._post_tool_hook("read_file", _mk_args(target), result)
        assert server.tca.ncb_contract(target) is False


# ─────────────────────────────────────────────────────────────────────────────
# NCB contract enforcement
# ─────────────────────────────────────────────────────────────────────────────


class TestNCBEnforcement:
    def test_write_without_read_is_allowed_in_warn_mode(self, tmp_path):
        server = _make_server(tmp_path)
        # Default mode is "warn" → returns (True, "")
        allow, reason = server._pre_tool_hook("write_file", _mk_args(tmp_path / "new.py"))
        assert allow is True

    def test_write_without_read_is_blocked_in_block_mode(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        allow, reason = server._pre_tool_hook("write_file", _mk_args(tmp_path / "new.py"))
        assert allow is False
        assert "NCB violation" in reason

    def test_write_after_read_is_allowed_in_block_mode(self, tmp_path):
        target = tmp_path / "existing.py"
        target.write_text("y = 2\n")
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        # Record a read
        server._post_tool_hook("read_file", _mk_args(target), MagicMock(success=True, output="y = 2\n"))
        allow, reason = server._pre_tool_hook("write_file", _mk_args(target))
        assert allow is True

    def test_ncb_check_skipped_for_non_write_tools(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        # list_directory etc. should never be NCB-gated
        allow, _ = server._pre_tool_hook("list_directory", _mk_args(tmp_path))
        assert allow is True


# ─────────────────────────────────────────────────────────────────────────────
# CIE gate on write_file / edit_file
# ─────────────────────────────────────────────────────────────────────────────


class TestCIEGateOnWrite:
    def test_valid_python_passes_cie(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "ok.py"), "content": "def f(): return 1\n"}
        result = MagicMock(success=True, output="wrote 18 bytes")
        out = server._post_tool_hook("write_file", args, result)
        # Valid code → result unchanged
        assert out.success is True

    def test_syntax_error_blocked_by_cie(self, tmp_path):
        server = _make_server(tmp_path)
        target = tmp_path / "broken.py"
        # Pre-write so undo_edit has something to roll back (not strictly needed here)
        target.write_text("")
        args = {"path": str(target), "content": "def broken(:\n    pass\n"}
        original = MagicMock(success=True, output="wrote")
        out = server._post_tool_hook("write_file", args, original)
        assert out.success is False
        assert "CIE REJECTED" in (out.error or "")

    def test_owasp_eval_injection_blocked(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "bad.py"), "content": "result = eval(user_input)\n"}
        out = server._post_tool_hook("write_file", args, MagicMock(success=True, output="ok"))
        assert out.success is False
        assert "CIE REJECTED" in (out.error or "")
        assert "A03_injection_eval" in (out.error or "")

    def test_non_python_skipped_by_cie(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "readme.txt"), "content": "raw text with eval()"}
        result = MagicMock(success=True, output="ok")
        out = server._post_tool_hook("write_file", args, result)
        # Text files aren't AST-validated or OWASP-scanned → pass through
        assert out.success is True

    def test_failed_write_is_not_cie_gated(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "x.py"), "content": "def ok(): pass"}
        result = MagicMock(success=False, error="disk full")
        out = server._post_tool_hook("write_file", args, result)
        # Unchanged — CIE only runs on successful writes
        assert out.success is False
        assert out.error == "disk full"


# ─────────────────────────────────────────────────────────────────────────────
# LoRA capture on accepted edits
# ─────────────────────────────────────────────────────────────────────────────


class TestLoRACaptureOnWrite:
    def test_accepted_write_captures_fix(self, tmp_path, monkeypatch):
        # Isolate LoRA state to tmp_path
        monkeypatch.chdir(tmp_path)
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "module.py"), "content": "def g(): return 42\n"}
        server._post_tool_hook("write_file", args, MagicMock(success=True, output="wrote"))
        # Flywheel should have 1 captured fix
        fly = server.lora_flywheel
        if fly is not None:
            kinds = [c.kind for c in fly._pending]
            assert "fix" in kinds

    def test_rejected_write_captures_rejection(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "bad.py"), "content": "def bad(:\n    pass\n"}
        server._post_tool_hook("write_file", args, MagicMock(success=True, output="wrote"))
        fly = server.lora_flywheel
        if fly is not None:
            kinds = [c.kind for c in fly._pending]
            assert "rejection" in kinds


# ─────────────────────────────────────────────────────────────────────────────
# Smoke: pre+post hooks together on a realistic sequence
# ─────────────────────────────────────────────────────────────────────────────


class TestMCPGateSequence:
    def test_read_then_write_passes_all_gates(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        target = tmp_path / "app.py"
        target.write_text("x = 1\n")

        # 1. read_file → TCA records freshness
        server._post_tool_hook("read_file", _mk_args(target), MagicMock(success=True, output="x = 1\n"))
        # 2. write_file pre-check → NCB passes (we just read it)
        allow, _ = server._pre_tool_hook("write_file", _mk_args(target))
        assert allow is True
        # 3. write_file post-check → CIE accepts clean code
        new_code = "def run():\n    return 2\n"
        out = server._post_tool_hook(
            "write_file",
            {"path": str(target), "content": new_code},
            MagicMock(success=True, output="wrote"),
        )
        assert out.success is True

    def test_write_without_read_blocked_end_to_end(self, tmp_path):
        server = _make_server(tmp_path)
        server._ncb_mode = "block"
        target = tmp_path / "never_read.py"
        allow, reason = server._pre_tool_hook("write_file", _mk_args(target, content="def x(): pass"))
        assert allow is False
        assert "NCB" in reason
