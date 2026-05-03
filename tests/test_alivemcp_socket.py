"""
Tests for ALiveMCP socket listener and client handling behavior.
"""

import json
import queue
from unittest.mock import MagicMock, patch

import pytest

from ALiveMCP_Remote import ALiveMCP


@pytest.fixture
def mcp(c_instance):
    with patch("ALiveMCP_Remote.socket.socket"), patch("ALiveMCP_Remote.threading.Thread"):
        instance = ALiveMCP(c_instance)
    return instance


def test_socket_listener_exits_immediately_when_not_running(mcp):
    mcp.running = False
    mcp.socket_server = MagicMock()
    mcp._socket_listener()
    mcp.socket_server.accept.assert_not_called()


def test_socket_listener_spawns_thread_per_connection(mcp):
    mock_client = MagicMock()
    call_count = 0

    def accept_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return mock_client, ("127.0.0.1", 12345)
        mcp.running = False
        raise OSError("server closed")

    mcp.socket_server = MagicMock()
    mcp.socket_server.accept.side_effect = accept_side_effect

    with patch("ALiveMCP_Remote.threading.Thread") as mock_thread_cls:
        mock_thread_cls.return_value = MagicMock()
        mcp._socket_listener()

    mock_thread_cls.assert_called_once()


def test_socket_listener_logs_error_when_running(mcp):
    call_count = 0

    def accept_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RuntimeError("random error")
        mcp.running = False
        raise RuntimeError("stop")

    mcp.socket_server = MagicMock()
    mcp.socket_server.accept.side_effect = accept_side_effect
    mcp._socket_listener()
    mcp.c_instance.log_message.assert_called()


def _make_intercept(mcp):
    original_put = mcp.command_queue.put

    def intercept(item):
        request_id, command = item
        original_put(item)
        response = mcp._process_command(command)
        if request_id in mcp.response_queues:
            mcp.response_queues[request_id].put(response)

    return intercept


def test_handle_client_success(mcp):
    mock_client = MagicMock()
    json_message = json.dumps({"action": "ping"}) + "\n"
    mock_client.recv.side_effect = [json_message.encode(), b""]
    mcp.command_queue.put = _make_intercept(mcp)

    mcp._handle_client(mock_client)

    mock_client.sendall.assert_called_once()
    raw = mock_client.sendall.call_args[0][0]
    response = json.loads(raw.decode().strip())
    assert response["ok"] is True
    assert response["message"] == "pong (queue-based, thread-safe)"


def test_handle_client_json_parse_error(mcp):
    mock_client = MagicMock()
    mock_client.recv.side_effect = [b"not valid json\n", b""]

    mcp._handle_client(mock_client)

    mock_client.sendall.assert_called_once()
    raw = mock_client.sendall.call_args[0][0]
    response = json.loads(raw.decode().strip())
    assert response["ok"] is False


def test_handle_client_response_timeout(mcp):
    mock_client = MagicMock()
    json_message = json.dumps({"action": "ping"}) + "\n"
    mock_client.recv.side_effect = [json_message.encode(), b""]

    with patch("ALiveMCP_Remote.queue.Queue.get", side_effect=queue.Empty):
        mcp._handle_client(mock_client)

    mock_client.sendall.assert_called_once()
    raw = mock_client.sendall.call_args[0][0]
    response = json.loads(raw.decode().strip())
    assert response["ok"] is False
    assert "timeout" in response["error"].lower()


def test_handle_client_closes_socket_on_exit(mcp):
    mock_client = MagicMock()
    mock_client.recv.return_value = b""
    mcp._handle_client(mock_client)
    mock_client.close.assert_called_once()


def test_handle_client_socket_timeout_continues(mcp):
    import socket as socket_mod

    mock_client = MagicMock()
    mock_client.recv.side_effect = [socket_mod.timeout, b""]
    mcp._handle_client(mock_client)


def test_handle_client_exits_when_not_running(mcp):
    mock_client = MagicMock()
    mcp.running = False
    mock_client.recv.return_value = b"irrelevant"
    mcp._handle_client(mock_client)
    mock_client.close.assert_called_once()


def test_handle_client_multiple_messages_in_buffer(mcp):
    mock_client = MagicMock()
    msg1 = json.dumps({"action": "ping"})
    msg2 = json.dumps({"action": "ping"})
    payload = (msg1 + "\n" + msg2 + "\n").encode()
    mock_client.recv.side_effect = [payload, b""]
    mcp.command_queue.put = _make_intercept(mcp)

    mcp._handle_client(mock_client)

    assert mock_client.sendall.call_count == 2
