"""Tier a2 — HTTP webhook client for the notify subsystem."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from ass_ade.a0_qk_constants.notify_types import (
    NOTIFY_CONFIG_FILENAME,
    NOTIFY_DIR_NAME,
    NotifyChannel,
    NotifyPayload,
)
from ass_ade.a1_at_functions.notify_helpers import serialize_payload


def _config_path() -> Path:
    return Path.home() / NOTIFY_DIR_NAME / NOTIFY_CONFIG_FILENAME


class NotifyClient:
    """Sends webhook notifications to Slack, Discord, or arbitrary endpoints."""

    def __init__(self, config_path: Path | None = None) -> None:
        self._config_path = config_path or _config_path()
        self._config: dict = {}
        self._load()

    def _load(self) -> None:
        if self._config_path.exists():
            self._config = json.loads(self._config_path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(json.dumps(self._config, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # Config helpers
    # ------------------------------------------------------------------
    def set_webhook(self, channel: NotifyChannel, url: str) -> None:
        self._config[channel.value] = url
        self._save()

    def get_webhook(self, channel: NotifyChannel) -> str | None:
        return self._config.get(channel.value)

    def configured_channels(self) -> list[str]:
        return [k for k in self._config if k in {c.value for c in NotifyChannel}]

    # ------------------------------------------------------------------
    # Send
    # ------------------------------------------------------------------
    def send(self, channel: NotifyChannel, payload: NotifyPayload, timeout: int = 10) -> None:
        if channel == NotifyChannel.STDOUT:
            from ass_ade.a1_at_functions.notify_helpers import format_notify_preview
            print(format_notify_preview(payload))
            return

        url = self.get_webhook(channel)
        if not url:
            raise ValueError(
                f"No webhook URL configured for {channel.value!r}. "
                f"Run: ass-ade notify config --{channel.value} <URL>"
            )
        body = serialize_payload(channel, payload)
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                _ = resp.read()
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Webhook HTTP {exc.code}: {exc.reason}") from exc
        except OSError as exc:
            raise RuntimeError(f"Webhook network error: {exc}") from exc
