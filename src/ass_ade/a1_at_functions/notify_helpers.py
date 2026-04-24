"""Tier a1 — pure helpers for the notify subsystem."""

from __future__ import annotations

import json

from ass_ade.a0_qk_constants.notify_types import NOTIFY_COLOR, NotifyChannel, NotifyPayload


def build_slack_payload(payload: NotifyPayload) -> dict:
    color_hex = f"#{NOTIFY_COLOR.get(payload['level'], 0x5865F2):06X}"
    return {
        "attachments": [
            {
                "color": color_hex,
                "title": payload["title"] or payload["source"],
                "text": payload["text"],
                "footer": f"ass-ade · {payload['source']}",
            }
        ]
    }


def build_discord_payload(payload: NotifyPayload) -> dict:
    color_int = NOTIFY_COLOR.get(payload["level"], 0x5865F2)
    title = payload["title"] or payload["source"]
    return {
        "embeds": [
            {
                "title": title,
                "description": payload["text"],
                "color": color_int,
                "footer": {"text": f"ass-ade · {payload['source']}"},
            }
        ]
    }


def build_generic_payload(payload: NotifyPayload) -> dict:
    return {
        "title": payload["title"],
        "text": payload["text"],
        "level": payload["level"],
        "source": payload["source"],
    }


def serialize_payload(channel: NotifyChannel, payload: NotifyPayload) -> bytes:
    if channel == NotifyChannel.SLACK:
        data = build_slack_payload(payload)
    elif channel == NotifyChannel.DISCORD:
        data = build_discord_payload(payload)
    else:
        data = build_generic_payload(payload)
    return json.dumps(data).encode()


def format_notify_preview(payload: NotifyPayload) -> str:
    icon = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✗"}.get(payload["level"], "·")
    title = f"[{payload['title']}] " if payload["title"] else ""
    return f"{icon} {title}{payload['text']}"
