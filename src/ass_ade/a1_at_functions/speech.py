"""Tier a1 — pure helpers for text-to-speech output via edge-tts (Microsoft, free, no API key)."""

from __future__ import annotations

import asyncio
import os
import subprocess
import tempfile
from pathlib import Path


# Default voice — warm, clear, natural-sounding US English male.
_DEFAULT_VOICE = "en-US-GuyNeural"


def _play_mp3(audio_file: str) -> None:
    """Play an MP3 file on Windows via Windows.Media.MediaPlayer (no extra deps)."""
    ps_cmd = (
        "Add-Type -AssemblyName presentationCore; "
        "$p = New-Object System.Windows.Media.MediaPlayer; "
        f'$p.Open("{audio_file}"); '
        "Start-Sleep 1; "
        "$p.Play(); "
        "Start-Sleep 20"
    )
    subprocess.Popen(["powershell", "-c", ps_cmd], shell=False)


async def _speak_async(text: str, voice: str) -> bool:
    try:
        import edge_tts  # type: ignore[import]
    except ImportError:
        return False

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        audio_path = f.name

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(audio_path)
        _play_mp3(audio_path)
        return True
    except Exception:
        return False


def speak(text: str, voice: str = _DEFAULT_VOICE) -> bool:
    """Synthesise text to speech and play it asynchronously.

    Uses edge-tts (Microsoft Azure TTS, free, no API key, no rate limits).
    Falls back silently if edge-tts is not installed.

    Returns True if synthesis was started, False if edge-tts is unavailable.
    """
    try:
        return asyncio.run(_speak_async(text, voice))
    except RuntimeError:
        # Already inside a running event loop — schedule as a task instead.
        loop = asyncio.get_event_loop()
        future = loop.run_until_complete(_speak_async(text, voice))
        return bool(future)


def speak_greeting(name: str = "Thomas and Jessica") -> bool:
    """Speak Atomadic's standard morning greeting."""
    text = (
        f"Good morning, {name}. "
        "Atomadic is awake. "
        "Systems are green. "
        "Ready when you are."
    )
    return speak(text)
