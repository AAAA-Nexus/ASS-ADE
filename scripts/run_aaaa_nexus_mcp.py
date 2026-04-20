"""Launch the direct AAAA-Nexus MCP server with workspace secret loading.

This keeps API keys out of ``.mcp.json`` while still letting editor MCP clients
start the worker-backed AAAA-Nexus tool server directly.
"""

from __future__ import annotations

import asyncio
import os
import runpy
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NEXUS_MCP_SRC = Path(r"C:\!aaaa-nexus-mcp\src")


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and not os.environ.get(key):
            os.environ[key] = value


def _prepare_environment() -> Path:
    _load_env_file(ROOT / ".env")
    os.environ.setdefault("AAAA_NEXUS_BASE_URL", "https://atomadic.tech")
    os.environ.setdefault("AAAA_NEXUS_TIMEOUT", "5.0")
    os.environ.setdefault("AAAA_NEXUS_AUTOGUARD", "false")

    src = Path(os.environ.get("AAAA_NEXUS_MCP_SRC", str(DEFAULT_NEXUS_MCP_SRC)))
    if src.exists():
        sys.path.insert(0, str(src))
    return src


async def _probe() -> None:
    from aaaa_nexus_mcp.client import NexusAPIClient

    base_url = os.environ["AAAA_NEXUS_BASE_URL"]
    timeout = float(os.environ["AAAA_NEXUS_TIMEOUT"])
    api_key = os.environ.get("AAAA_NEXUS_API_KEY") or None
    autoguard = os.environ.get("AAAA_NEXUS_AUTOGUARD", "false").lower() not in (
        "0",
        "false",
        "no",
    )

    async with NexusAPIClient(
        base_url=base_url,
        api_key=api_key,
        timeout=timeout,
        autoguard=autoguard,
    ) as client:
        for path in ("/health", "/v1/payments/fee", "/.well-known/mcp.json"):
            t0 = time.perf_counter()
            payload = await client.get(path)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            label = payload.get("status") or payload.get("name") or payload.get("product") or "ok"
            print(f"{path}: {label} ({elapsed_ms:.1f} ms)")
    print(f"base_url={base_url}")
    print(f"api_key={'set' if api_key else 'missing'}")
    print(f"autoguard={autoguard}")


def main() -> None:
    _prepare_environment()
    if "--probe" in sys.argv:
        asyncio.run(_probe())
        return
    runpy.run_module("aaaa_nexus_mcp", run_name="__main__")


if __name__ == "__main__":
    main()
