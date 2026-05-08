#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.0.0"]
# ///
"""
ALiveMCP MCP Server - Exposes Ableton Live control to AI agents via Model Context Protocol.

Bridges MCP to the ALiveMCP Remote Script TCP socket on 127.0.0.1:9004.
Ableton Live must be running with the ALiveMCP Remote Script loaded.
"""

import asyncio
import json

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from ableton_client import _call_ableton
from mcp_server_tool_defs import TOOL_DEFS_JSON


def _load_tool_defs() -> list[tuple[str, str, dict]]:
    """Deserialize tool definitions from the compact helper module."""
    raw_defs = json.loads(TOOL_DEFS_JSON)
    return [(name, description, schema) for name, description, schema in raw_defs]


TOOL_DEFS: list[tuple[str, str, dict]] = _load_tool_defs()

server = Server("alivemcp")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=name, description=desc, inputSchema=schema)
        for name, desc, schema in TOOL_DEFS
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    result = await asyncio.get_event_loop().run_in_executor(
        None, _call_ableton, name, arguments or {}
    )
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


async def main() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="alivemcp",
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
