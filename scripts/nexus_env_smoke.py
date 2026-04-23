#!/usr/bin/env python3
"""Verify repo .env is loadable and AAAA-Nexus HTTP accepts the API key (smoke).

Does not call paid MCP tools; uses a simple GET so you can confirm the key
reaches atomadic.tech before relying on hallucination_oracle / full §11 chain.

Usage (repo root):
  python scripts/nexus_env_smoke.py
"""
from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        k = key.strip()
        v = val.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def _mask(s: str, keep: int = 6) -> str:
    if len(s) <= keep:
        return "***"
    return s[:keep] + "…" + s[-4:] if len(s) > keep + 4 else s[:keep] + "…"


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    _load_dotenv(root / ".env")
    key = (os.environ.get("AAAA_NEXUS_API_KEY") or "").strip()
    if not key:
        print("AAAA_NEXUS_API_KEY not set (add to .env or environment).", file=sys.stderr)
        return 2

    base = os.environ.get("AAAA_NEXUS_BASE_URL", "https://atomadic.tech").rstrip("/")
    url = f"{base}/health"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {key}",
            "Accept": "application/json",
        },
        method="GET",
    )
    print(f"API key (masked): {_mask(key)}")
    print(f"GET {url}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read(8000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 1

    print("Response OK (first 500 chars):")
    print(body[:500])
    print(
        "\nNext: ensure Cursor MCP `user-aaaa-nexus` uses "
        "`Authorization: Bearer ${env:AAAA_NEXUS_API_KEY}` and restart Cursor "
        "if the MCP process was started before the variable existed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
