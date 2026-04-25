"""Tests for a1_at_functions/system_actions.py — pure system action helpers."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ass_ade.a1_at_functions.system_actions import (
    get_system_time,
    open_browser,
    play_audio,
    send_desktop_notification,
    wake_page_path,
    _try_plyer,
    _try_powershell,
)


# ── get_system_time ────────────────────────────────────────────────────────────


def test_get_system_time_returns_utc_datetime():
    t = get_system_time()
    assert isinstance(t, datetime)
    assert t.tzinfo is not None
    assert t.tzinfo == timezone.utc


def test_get_system_time_is_recent():
    import time
    before = datetime.now(timezone.utc).timestamp()
    t = get_system_time()
    after = datetime.now(timezone.utc).timestamp()
    assert before <= t.timestamp() <= after


# ── open_browser ───────────────────────────────────────────────────────────────


def test_open_browser_calls_webbrowser_open(monkeypatch):
    called_with = {}

    def fake_open(url, new=0):
        called_with["url"] = url
        called_with["new"] = new

    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.webbrowser.open", fake_open)
    # Suppress fullscreen subprocess on Windows
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions._request_fullscreen", lambda: None)

    result = open_browser("https://example.com", fullscreen=True)

    assert result is True
    assert called_with["url"] == "https://example.com"
    assert called_with["new"] == 2


def test_open_browser_returns_false_on_exception(monkeypatch):
    def broken_open(url, new=0):
        raise OSError("no browser")

    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.webbrowser.open", broken_open)
    assert open_browser("https://example.com") is False


def test_open_browser_no_fullscreen_skips_request(monkeypatch):
    fullscreen_called = []
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.webbrowser.open", lambda *a, **k: None)
    monkeypatch.setattr(
        "ass_ade.a1_at_functions.system_actions._request_fullscreen",
        lambda: fullscreen_called.append(1),
    )

    open_browser("https://example.com", fullscreen=False)
    assert fullscreen_called == []


# ── play_audio ─────────────────────────────────────────────────────────────────


def test_play_audio_delegates_to_open_browser(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "ass_ade.a1_at_functions.system_actions.open_browser",
        lambda url, fullscreen=True: calls.append((url, fullscreen)) or True,
    )
    result = play_audio("https://www.youtube.com/watch?v=aQUlA8GCMjo")
    assert result is True
    assert calls == [("https://www.youtube.com/watch?v=aQUlA8GCMjo", False)]


# ── send_desktop_notification ──────────────────────────────────────────────────


def test_send_desktop_notification_uses_plyer_when_available(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "ass_ade.a1_at_functions.system_actions._try_plyer",
        lambda t, b: calls.append((t, b)) or True,
    )
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions._try_powershell", lambda t, b: False)

    result = send_desktop_notification("Title", "Body")
    assert result is True
    assert calls == [("Title", "Body")]


def test_send_desktop_notification_falls_back_to_powershell(monkeypatch):
    calls = []
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions._try_plyer", lambda t, b: False)
    monkeypatch.setattr(
        "ass_ade.a1_at_functions.system_actions._try_powershell",
        lambda t, b: calls.append((t, b)) or True,
    )

    result = send_desktop_notification("Title", "Body")
    assert result is True
    assert calls == [("Title", "Body")]


def test_send_desktop_notification_returns_false_when_all_fail(monkeypatch):
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions._try_plyer", lambda t, b: False)
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions._try_powershell", lambda t, b: False)
    assert send_desktop_notification("T", "B") is False


# ── _try_plyer ─────────────────────────────────────────────────────────────────


def test_try_plyer_returns_false_when_import_fails(monkeypatch):
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "plyer":
            raise ImportError("no plyer")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    assert _try_plyer("T", "B") is False


# ── _try_powershell ────────────────────────────────────────────────────────────


def test_try_powershell_returns_false_on_non_windows(monkeypatch):
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.sys.platform", "linux")
    assert _try_powershell("T", "B") is False


def test_try_powershell_returns_true_on_windows(monkeypatch):
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.sys.platform", "win32")
    popen_calls = []

    def fake_popen(args, **kwargs):
        popen_calls.append(args)
        return MagicMock()

    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.subprocess.Popen", fake_popen)
    result = _try_powershell("Hello", "World")
    assert result is True
    assert len(popen_calls) == 1


def test_try_powershell_sanitises_quotes(monkeypatch):
    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.sys.platform", "win32")
    captured = {}

    def fake_popen(args, **kwargs):
        captured["cmd"] = " ".join(args)
        return MagicMock()

    monkeypatch.setattr("ass_ade.a1_at_functions.system_actions.subprocess.Popen", fake_popen)
    _try_powershell("It's alive", "Say 'hello'")
    # Single-quotes must be doubled, not left raw
    assert "It''s alive" in captured["cmd"]
    assert "Say ''hello''" in captured["cmd"]


# ── wake_page_path ─────────────────────────────────────────────────────────────


def test_wake_page_path_returns_path_object():
    p = wake_page_path()
    assert isinstance(p, Path)
    assert p.name == "wake.html"
    assert p.parent.name == "assets"
