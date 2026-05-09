"""Tests for mcp_server.py and ableton_client.py.

_call_ableton transport tests target ableton_client directly.
MCP tool-wiring tests (list_tools / call_tool) use mcp_server.

The mcp module is an external dependency not available in the test environment,
so we stub it before importing mcp_server.
"""

import json
import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Stub the `mcp` package before importing mcp_server
# ---------------------------------------------------------------------------


def _make_mcp_stub():
    mcp = ModuleType("mcp")
    mcp.server = ModuleType("mcp.server")
    mcp.server.stdio = ModuleType("mcp.server.stdio")
    mcp.types = ModuleType("mcp.types")
    mcp.server.models = ModuleType("mcp.server.models")

    class _TextContent:
        def __init__(self, type, text):
            self.type = type
            self.text = text

    class _Tool:
        def __init__(self, name, description, inputSchema):
            self.name = name
            self.description = description
            self.inputSchema = inputSchema

    class _Server:
        """Minimal stand-in for mcp.server.Server."""

        def __init__(self, name):
            self.name = name
            self._list_tools_handler = None
            self._call_tool_handler = None

        def list_tools(self):
            def decorator(fn):
                self._list_tools_handler = fn
                return fn

            return decorator

        def call_tool(self):
            def decorator(fn):
                self._call_tool_handler = fn
                return fn

            return decorator

        def get_capabilities(self, **_):
            return {}

    class _NotificationOptions:
        pass

    class _InitializationOptions:
        def __init__(self, **_):
            pass

    mcp.types.Tool = _Tool
    mcp.types.TextContent = _TextContent
    mcp.server.Server = _Server
    mcp.server.NotificationOptions = _NotificationOptions
    mcp.server.models.InitializationOptions = _InitializationOptions

    return mcp


_mcp_stub = _make_mcp_stub()
sys.modules.setdefault("mcp", _mcp_stub)
sys.modules.setdefault("mcp.server", _mcp_stub.server)
sys.modules.setdefault("mcp.server.stdio", _mcp_stub.server.stdio)
sys.modules.setdefault("mcp.types", _mcp_stub.types)
sys.modules.setdefault("mcp.server.models", _mcp_stub.server.models)

import ableton_client  # noqa: E402
import mcp_server  # noqa: E402 (import after stub setup)

# ---------------------------------------------------------------------------
# _call_ableton
# ---------------------------------------------------------------------------


def _fake_socket_response(response_dict):
    """Return a context-manager mock socket that yields the given JSON response."""
    raw = (json.dumps(response_dict) + "\n").encode()
    sock = MagicMock()
    sock.recv.side_effect = [raw, b""]  # one chunk then EOF
    ctx = MagicMock()
    ctx.__enter__ = MagicMock(return_value=sock)
    ctx.__exit__ = MagicMock(return_value=False)
    return ctx


def test_call_ableton_success():
    expected = {"ok": True, "bpm": 128.0}
    with patch(
        "ableton_client.socket.create_connection", return_value=_fake_socket_response(expected)
    ):
        result = ableton_client._call_ableton("set_tempo", {"bpm": 128})
    assert result["ok"] is True
    assert result["bpm"] == 128.0


def test_call_ableton_sends_action_in_payload():
    expected = {"ok": True}
    captured = {}

    def fake_create_connection(addr, timeout):
        ctx = _fake_socket_response(expected)
        inner_sock = ctx.__enter__.return_value

        def capture_send(data):
            captured["sent"] = json.loads(data.decode().strip())

        inner_sock.sendall.side_effect = capture_send
        return ctx

    with patch("ableton_client.socket.create_connection", side_effect=fake_create_connection):
        ableton_client._call_ableton("set_tempo", {"bpm": 140})

    assert captured["sent"]["action"] == "set_tempo"
    assert captured["sent"]["bpm"] == 140


def test_call_ableton_connection_refused():
    with patch("ableton_client.socket.create_connection", side_effect=ConnectionRefusedError):
        result = ableton_client._call_ableton("ping", {})
    assert result["ok"] is False
    assert "Cannot connect" in result["error"]
    assert "9004" in result["error"]


def test_call_ableton_generic_exception():
    with patch("ableton_client.socket.create_connection", side_effect=OSError("network failure")):
        result = ableton_client._call_ableton("ping", {})
    assert result["ok"] is False
    assert "network failure" in result["error"]


def test_call_ableton_malformed_json_response():
    sock = MagicMock()
    sock.recv.side_effect = [b"not-valid-json\n", b""]
    ctx = MagicMock()
    ctx.__enter__ = MagicMock(return_value=sock)
    ctx.__exit__ = MagicMock(return_value=False)
    with patch("ableton_client.socket.create_connection", return_value=ctx):
        result = ableton_client._call_ableton("ping", {})
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# list_tools
# ---------------------------------------------------------------------------


def test_list_tools_count_matches_tool_defs():
    """Every entry in TOOL_DEFS appears in the list returned by list_tools."""
    import asyncio

    tools = asyncio.run(mcp_server.server._list_tools_handler())
    assert len(tools) == len(mcp_server.TOOL_DEFS)


def test_list_tools_names_match_tool_defs():
    import asyncio

    tools = asyncio.run(mcp_server.server._list_tools_handler())
    returned_names = {t.name for t in tools}
    expected_names = {name for name, _, _ in mcp_server.TOOL_DEFS}
    assert returned_names == expected_names


# ---------------------------------------------------------------------------
# call_tool
# ---------------------------------------------------------------------------


def test_call_tool_dispatches_correct_payload():
    import asyncio

    expected = {"ok": True, "message": "pong"}
    with patch.object(mcp_server, "_call_ableton", return_value=expected) as mock_ca:
        result = asyncio.run(mcp_server.server._call_tool_handler("ping", {}))
    mock_ca.assert_called_once_with("ping", {})
    assert len(result) == 1
    assert json.loads(result[0].text)["ok"] is True


def test_call_tool_propagates_error_response():
    import asyncio

    error_resp = {"ok": False, "error": "Ableton offline"}
    with patch.object(mcp_server, "_call_ableton", return_value=error_resp):
        result = asyncio.run(mcp_server.server._call_tool_handler("ping", {}))
    parsed = json.loads(result[0].text)
    assert parsed["ok"] is False
    assert "Ableton offline" in parsed["error"]
