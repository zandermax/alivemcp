"""
Tests for ALiveMCP core lifecycle, command dispatch, and queue processing.
"""

import queue
from unittest.mock import MagicMock, patch

import pytest

from ALiveMCP_Remote import ALiveMCP, __version__, create_instance


@pytest.fixture
def mcp(c_instance):
    with patch("ALiveMCP_Remote.socket.socket"), patch("ALiveMCP_Remote.threading.Thread"):
        instance = ALiveMCP(c_instance)
    return instance


def test_init_sets_c_instance_and_song(c_instance):
    with patch("ALiveMCP_Remote.socket.socket"), patch("ALiveMCP_Remote.threading.Thread"):
        instance = ALiveMCP(c_instance)
    assert instance.c_instance is c_instance
    assert instance.song is c_instance.song()


def test_init_creates_tools(mcp):
    from ALiveMCP_Remote.liveapi_tools import LiveAPITools

    assert isinstance(mcp.tools, LiveAPITools)


def test_init_creates_queues(mcp):
    assert isinstance(mcp.command_queue, queue.Queue)
    assert isinstance(mcp.response_queues, dict)
    assert mcp.request_counter == 0


def test_init_starts_socket_server(c_instance):
    with patch("ALiveMCP_Remote.socket.socket") as mock_sock_cls, patch(
        "ALiveMCP_Remote.threading.Thread"
    ) as mock_thread_cls:
        ALiveMCP(c_instance)
    mock_sock_cls.assert_called_once()
    mock_thread_cls.assert_called_once()


def test_start_socket_server_logs_error_on_exception(c_instance):
    with patch("ALiveMCP_Remote.socket.socket") as mock_sock_cls, patch(
        "ALiveMCP_Remote.threading.Thread"
    ):
        mock_sock_cls.return_value.bind.side_effect = OSError("address in use")
        instance = ALiveMCP(c_instance)
    assert instance is not None
    c_instance.log_message.assert_called()


def test_log_prefixes_message(mcp, c_instance):
    mcp.log("test message")
    c_instance.log_message.assert_called_with("[ALiveMCP] test message")


def test_log_converts_non_string(mcp, c_instance):
    mcp.log(42)
    c_instance.log_message.assert_called_with("[ALiveMCP] 42")


def test_process_command_ping(mcp):
    result = mcp._process_command({"action": "ping"})
    assert result["ok"] is True
    assert result["message"] == "pong (queue-based, thread-safe)"
    assert result["script"] == "ALiveMCP_Remote"
    assert result["version"] == __version__


def test_process_command_health_check(mcp):
    result = mcp._process_command({"action": "health_check"})
    assert result["ok"] is True
    assert result["version"] == __version__
    assert "tool_count" in result
    assert "queue_size" in result
    assert "ableton_version" in result


def test_process_command_unknown_action(mcp):
    result = mcp._process_command({"action": "nonexistent_action"})
    assert result["ok"] is False
    assert "Unknown action" in result["error"]
    assert isinstance(result["available_actions"], list)


def test_process_command_dispatches_to_tools(mcp):
    mcp.tools.ping = MagicMock(return_value={"ok": True, "custom": "value"})
    result = mcp._process_command({"action": "ping"})
    assert result["ok"] is True

    mcp.tools.start_playback = MagicMock(return_value={"ok": True, "dispatched": True})
    result = mcp._process_command({"action": "start_playback"})
    mcp.tools.start_playback.assert_called_once_with()
    assert result["dispatched"] is True


def test_process_command_passes_params_to_tool(mcp):
    mcp.tools.set_tempo = MagicMock(return_value={"ok": True})
    mcp._process_command({"action": "set_tempo", "bpm": 120})
    mcp.tools.set_tempo.assert_called_once_with(bpm=120)


def test_process_command_exception_returns_error_with_traceback(mcp):
    mcp.tools.start_playback = MagicMock(side_effect=RuntimeError("boom"))
    result = mcp._process_command({"action": "start_playback"})
    assert result["ok"] is False
    assert "boom" in result["error"]
    assert "traceback" in result


def _put_command(mcp, request_id, command):
    mcp.response_queues[request_id] = queue.Queue()
    mcp.command_queue.put((request_id, command))


def test_update_display_empty_queue_is_noop(mcp):
    mcp.update_display()


def test_update_display_processes_single_command(mcp):
    _put_command(mcp, 0, {"action": "ping"})
    mcp.update_display()
    response = mcp.response_queues[0].get_nowait()
    assert response["ok"] is True


def test_update_display_puts_response_in_correct_queue(mcp):
    _put_command(mcp, 7, {"action": "ping"})
    _put_command(mcp, 8, {"action": "ping"})
    mcp.update_display()
    assert not mcp.response_queues[7].empty()
    assert not mcp.response_queues[8].empty()


def test_update_display_caps_at_five_commands_per_tick(mcp):
    for i in range(6):
        _put_command(mcp, i, {"action": "ping"})
    mcp.update_display()
    assert mcp.command_queue.qsize() == 1


def test_update_display_skips_missing_response_queue(mcp):
    mcp.command_queue.put((999, {"action": "ping"}))
    mcp.update_display()


def test_update_display_handles_exception_in_processing(mcp):
    _put_command(mcp, 0, {"action": "ping"})
    mcp._process_command = MagicMock(side_effect=RuntimeError("unexpected"))
    mcp.update_display()


def test_connect_script_instances_returns_none(mcp):
    assert mcp.connect_script_instances([]) is None


def test_can_lock_to_devices_returns_false(mcp):
    assert mcp.can_lock_to_devices() is False


def test_refresh_state_returns_none(mcp):
    assert mcp.refresh_state() is None


def test_build_midi_map_returns_none(mcp):
    assert mcp.build_midi_map(MagicMock()) is None


def test_disconnect_sets_running_false(mcp):
    assert mcp.running is True
    mcp.disconnect()
    assert mcp.running is False


def test_disconnect_closes_socket(mcp):
    mock_server = MagicMock()
    mcp.socket_server = mock_server
    mcp.disconnect()
    mock_server.close.assert_called_once()


def test_disconnect_handles_socket_close_error(mcp):
    mock_server = MagicMock()
    mock_server.close.side_effect = OSError("already closed")
    mcp.socket_server = mock_server
    mcp.disconnect()
    assert mcp.running is False


def test_create_instance_returns_claude_mcp(c_instance):
    with patch("ALiveMCP_Remote.socket.socket"), patch("ALiveMCP_Remote.threading.Thread"):
        instance = create_instance(c_instance)
    assert isinstance(instance, ALiveMCP)
