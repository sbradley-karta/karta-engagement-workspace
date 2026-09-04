"""Gate 1 stub: a minimal remote MCP server for the custom-connector spike.

Purpose
- Prove a published Claude artifact page can call an org custom connector via `mcp`.
- Measure how large a tool result (connector -> page) and a tool argument (page -> connector)
  can be before something truncates or rejects it.

Deliberately has no authentication and touches no data. Do not add either here.
"""
import base64
import hashlib
import os
import random

from fastmcp import FastMCP

mcp = FastMCP("Karta Assembly Test")

MAX_KB = 8192


@mcp.tool
def hello(name: str = "Karta") -> dict:
    """Return a greeting. Confirms the connector is reachable from a page."""
    return {"message": f"Hello, {name}.", "service": "karta-assembly-stub", "version": "0.1.0"}


@mcp.tool
def blob(size_kb: int = 64) -> dict:
    """Return `size_kb` kilobytes of deterministic pseudo-random bytes as base64.

    Measures the connector -> page payload limit. The sha256 lets the page verify
    the bytes arrived intact.
    """
    size_kb = max(1, min(int(size_kb), MAX_KB))
    data = random.Random(size_kb).randbytes(size_kb * 1024)
    return {
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "content_base64": base64.b64encode(data).decode("ascii"),
    }


@mcp.tool
def echo_size(content_base64: str) -> dict:
    """Decode a base64 payload and report its size and sha256.

    Measures the page -> connector argument limit, which is the same direction
    the real service receives approved values and the Microsoft 365 upload
    receives a deck.
    """
    data = base64.b64decode(content_base64, validate=True)
    return {"size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
        path="/mcp",
    )
