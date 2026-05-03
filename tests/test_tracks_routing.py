"""
Tests for TracksMixin routing and monitoring methods.
"""

from unittest.mock import MagicMock


def test_set_track_input_routing_valid(tools, song):
    result = tools.set_track_input_routing(0, "Ext. In", 1)
    assert result["ok"] is True


def test_set_track_input_routing_invalid(tools):
    result = tools.set_track_input_routing(-1, "x")
    assert result["ok"] is False


def test_set_track_output_routing_valid(tools, song):
    result = tools.set_track_output_routing(0, "Master")
    assert result["ok"] is True


def test_set_track_output_routing_invalid(tools):
    result = tools.set_track_output_routing(-1, "Master")
    assert result["ok"] is False


def test_set_track_current_monitoring_state_can_be_armed(tools, song):
    song.tracks[0].can_be_armed = True
    result = tools.set_track_current_monitoring_state(0, 1)
    assert result["ok"] is True


def test_set_track_current_monitoring_state_cannot_be_armed(tools, song):
    song.tracks[0].can_be_armed = False
    result = tools.set_track_current_monitoring_state(0, 1)
    assert result == {"ok": False, "error": "Track cannot be monitored"}


def test_set_track_current_monitoring_state_invalid(tools):
    result = tools.set_track_current_monitoring_state(-1, 0)
    assert result["ok"] is False


def test_get_track_available_input_routing_types_with_attr(tools, song):
    routing = MagicMock()
    routing.display_name = "Ext. In"
    song.tracks[0].available_input_routing_types = [routing]
    result = tools.get_track_available_input_routing_types(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_track_available_input_routing_types_without_attr(tools, song):
    del song.tracks[0].available_input_routing_types
    result = tools.get_track_available_input_routing_types(0)
    assert result["ok"] is True
    assert result["routing_types"] == []


def test_get_track_available_input_routing_types_invalid(tools):
    result = tools.get_track_available_input_routing_types(-1)
    assert result["ok"] is False


def test_get_track_available_output_routing_types_with_attr(tools, song):
    routing = MagicMock()
    routing.display_name = "Master"
    song.tracks[0].available_output_routing_types = [routing]
    result = tools.get_track_available_output_routing_types(0)
    assert result["ok"] is True


def test_get_track_available_output_routing_types_without_attr(tools, song):
    del song.tracks[0].available_output_routing_types
    result = tools.get_track_available_output_routing_types(0)
    assert result["ok"] is True
    assert result["routing_types"] == []


def test_get_track_available_output_routing_types_invalid(tools):
    result = tools.get_track_available_output_routing_types(-1)
    assert result["ok"] is False


def test_get_track_input_routing_type_with_attr(tools, song):
    result = tools.get_track_input_routing_type(0)
    assert result["ok"] is True


def test_get_track_input_routing_type_without_attr(tools, song):
    del song.tracks[0].input_routing_type
    result = tools.get_track_input_routing_type(0)
    assert result["ok"] is False


def test_get_track_input_routing_type_invalid(tools):
    result = tools.get_track_input_routing_type(-1)
    assert result["ok"] is False


def test_get_track_output_routing_with_attrs(tools, song):
    result = tools.get_track_output_routing(0)
    assert result["ok"] is True


def test_get_track_output_routing_invalid(tools):
    result = tools.get_track_output_routing(-1)
    assert result["ok"] is False


def test_set_track_input_sub_routing_with_attr(tools, song):
    result = tools.set_track_input_sub_routing(0, "ch1")
    assert result["ok"] is True


def test_set_track_input_sub_routing_without_attr(tools, song):
    del song.tracks[0].input_sub_routing
    result = tools.set_track_input_sub_routing(0, "ch1")
    assert result["ok"] is False


def test_set_track_input_sub_routing_invalid(tools):
    result = tools.set_track_input_sub_routing(-1, "ch1")
    assert result["ok"] is False


def test_set_track_output_sub_routing_with_attr(tools, song):
    result = tools.set_track_output_sub_routing(0, "ch1")
    assert result["ok"] is True


def test_set_track_output_sub_routing_without_attr(tools, song):
    del song.tracks[0].output_sub_routing
    result = tools.set_track_output_sub_routing(0, "ch1")
    assert result["ok"] is False


def test_set_track_output_sub_routing_invalid(tools):
    result = tools.set_track_output_sub_routing(-1, "ch1")
    assert result["ok"] is False


def test_set_track_input_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_input_routing(0, "x")
    assert result["ok"] is False


def test_set_track_output_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_output_routing(0, "x")
    assert result["ok"] is False


def test_set_track_current_monitoring_state_except_block(tools):
    tools.song = None
    result = tools.set_track_current_monitoring_state(0, 1)
    assert result["ok"] is False


def test_get_track_available_input_routing_types_except_block(tools):
    tools.song = None
    result = tools.get_track_available_input_routing_types(0)
    assert result["ok"] is False


def test_get_track_available_output_routing_types_except_block(tools):
    tools.song = None
    result = tools.get_track_available_output_routing_types(0)
    assert result["ok"] is False


def test_get_track_input_routing_type_except_block(tools):
    tools.song = None
    result = tools.get_track_input_routing_type(0)
    assert result["ok"] is False


def test_get_track_output_routing_except_block(tools):
    tools.song = None
    result = tools.get_track_output_routing(0)
    assert result["ok"] is False


def test_set_track_input_sub_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_input_sub_routing(0, "x")
    assert result["ok"] is False


def test_set_track_output_sub_routing_except_block(tools):
    tools.song = None
    result = tools.set_track_output_sub_routing(0, "x")
    assert result["ok"] is False
