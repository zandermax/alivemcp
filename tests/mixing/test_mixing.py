"""
Tests for MixingMixin core sends, master, return track, and crossfader operations.
"""

from unittest.mock import MagicMock


def test_set_track_send_valid(tools, song):
    send = MagicMock()
    send.value = 0.0
    song.tracks[0].mixer_device.sends = [send]
    result = tools.set_track_send(0, 0, 0.5)
    assert result["ok"] is True
    assert send.value == 0.5


def test_set_track_send_invalid_track(tools):
    result = tools.set_track_send(-1, 0, 0.5)
    assert result["ok"] is False


def test_set_track_send_invalid_send(tools, song):
    song.tracks[0].mixer_device.sends = []
    result = tools.set_track_send(0, 0, 0.5)
    assert result == {"ok": False, "error": "Invalid send index"}


def test_set_track_send_exception(tools, song):
    song.tracks[0].mixer_device.sends = MagicMock(side_effect=Exception("err"))
    result = tools.set_track_send(0, 0, 0.5)
    assert result["ok"] is False


def test_get_track_sends_success(tools, song):
    send = MagicMock()
    send.value = 0.5
    del send.name
    song.tracks[0].mixer_device.sends = [send]
    result = tools.get_track_sends(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_track_sends_with_name_attr(tools, song):
    send = MagicMock()
    send.value = 0.5
    send.name = "Reverb"
    song.tracks[0].mixer_device.sends = [send]
    result = tools.get_track_sends(0)
    assert result["ok"] is True
    assert result["sends"][0]["name"] == "Reverb"


def test_get_track_sends_invalid(tools):
    result = tools.get_track_sends(-1)
    assert result["ok"] is False


def test_get_track_sends_exception(tools, song):
    song.tracks[0].mixer_device.sends = None
    result = tools.get_track_sends(0)
    assert result["ok"] is False


def test_get_master_track_info_success(tools, song):
    result = tools.get_master_track_info()
    assert result["ok"] is True
    assert "name" in result
    assert "volume" in result


def test_get_master_track_info_exception(tools, song):
    song.master_track = None
    result = tools.get_master_track_info()
    assert result["ok"] is False


def test_set_master_volume_with_mixer_device(tools, song):
    result = tools.set_master_volume(0.8)
    assert result["ok"] is True


def test_set_master_volume_without_mixer_device(tools, song):
    del song.master_track.mixer_device
    result = tools.set_master_volume(0.8)
    assert result["ok"] is False


def test_set_master_volume_exception(tools, song):
    song.master_track = None
    result = tools.set_master_volume(0.8)
    assert result["ok"] is False


def test_set_master_pan_with_mixer_device(tools, song):
    result = tools.set_master_pan(0.0)
    assert result["ok"] is True


def test_set_master_pan_without_mixer_device(tools, song):
    del song.master_track.mixer_device
    result = tools.set_master_pan(0.0)
    assert result["ok"] is False


def test_set_master_pan_exception(tools, song):
    song.master_track = None
    result = tools.set_master_pan(0.0)
    assert result["ok"] is False


def test_get_master_devices_with_attr(tools, song):
    dev = MagicMock()
    dev.name = "Limiter"
    dev.class_name = "Limiter"
    dev.is_active = True
    song.master_track.devices = [dev]
    result = tools.get_master_devices()
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_master_devices_without_attr(tools, song):
    del song.master_track.devices
    result = tools.get_master_devices()
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_master_devices_exception(tools, song):
    song.master_track.devices = None
    result = tools.get_master_devices()
    assert result["ok"] is False


def test_get_return_track_count(tools, song):
    song.return_tracks = [MagicMock(), MagicMock()]
    result = tools.get_return_track_count()
    assert result["ok"] is True
    assert result["count"] == 2


def test_get_return_track_count_exception(tools, song):
    song.return_tracks = None
    result = tools.get_return_track_count()
    assert result["ok"] is False


def test_get_return_track_info_valid(tools, song):
    result = tools.get_return_track_info(0)
    assert result["ok"] is True
    assert result["index"] == 0


def test_get_return_track_info_invalid(tools, song):
    result = tools.get_return_track_info(-1)
    assert result["ok"] is False


def test_get_return_track_info_out_of_range(tools, song):
    result = tools.get_return_track_info(len(song.return_tracks))
    assert result["ok"] is False


def test_get_return_track_info_exception(tools, song):
    song.return_tracks = MagicMock(side_effect=Exception("err"))
    result = tools.get_return_track_info(0)
    assert result["ok"] is False


def test_set_return_track_volume_valid(tools, song):
    result = tools.set_return_track_volume(0, 0.7)
    assert result["ok"] is True


def test_set_return_track_volume_invalid(tools, song):
    result = tools.set_return_track_volume(-1, 0.5)
    assert result["ok"] is False


def test_set_return_track_volume_exception(tools, song):
    song.return_tracks = MagicMock(side_effect=Exception("err"))
    result = tools.set_return_track_volume(0, 0.5)
    assert result["ok"] is False


def test_get_crossfader_assignment_with_attr(tools, song):
    song.tracks[0].mixer_device.crossfade_assign = 1
    result = tools.get_crossfader_assignment(0)
    assert result["ok"] is True
    assert result["assignment_name"] == "A"


def test_get_crossfader_assignment_without_attr(tools, song):
    del song.tracks[0].mixer_device.crossfade_assign
    result = tools.get_crossfader_assignment(0)
    assert result["ok"] is False


def test_get_crossfader_assignment_invalid(tools):
    result = tools.get_crossfader_assignment(-1)
    assert result["ok"] is False


def test_get_crossfader_assignment_exception(tools, song):
    song.tracks[0].mixer_device.crossfade_assign = "bad"
    result = tools.get_crossfader_assignment(0)
    assert result["ok"] is False


def test_set_crossfader_assignment_with_attr(tools, song):
    result = tools.set_crossfader_assignment(0, 2)
    assert result["ok"] is True


def test_set_crossfader_assignment_without_attr(tools, song):
    del song.tracks[0].mixer_device.crossfade_assign
    result = tools.set_crossfader_assignment(0, 1)
    assert result["ok"] is False


def test_set_crossfader_assignment_invalid(tools):
    result = tools.set_crossfader_assignment(-1, 1)
    assert result["ok"] is False


def test_get_crossfader_position_with_attr(tools, song):
    song.master_track.mixer_device.crossfader.value = 0.5
    result = tools.get_crossfader_position()
    assert result["ok"] is True
    assert result["position"] == 0.5


def test_get_crossfader_position_without_attr(tools, song):
    del song.master_track.mixer_device.crossfader
    result = tools.get_crossfader_position()
    assert result["ok"] is False


def test_get_crossfader_position_exception(tools, song):
    song.master_track = None
    result = tools.get_crossfader_position()
    assert result["ok"] is False


def test_set_track_send_except_block(tools):
    tools.song = None
    result = tools.set_track_send(0, 0, 0.5)
    assert result["ok"] is False


def test_set_master_volume_except_block(tools):
    tools.song = None
    result = tools.set_master_volume(0.5)
    assert result["ok"] is False


def test_set_master_pan_except_block(tools):
    tools.song = None
    result = tools.set_master_pan(0.0)
    assert result["ok"] is False


def test_get_return_track_info_except_block(tools):
    tools.song = None
    result = tools.get_return_track_info(0)
    assert result["ok"] is False


def test_set_return_track_volume_except_block(tools):
    tools.song = None
    result = tools.set_return_track_volume(0, 0.5)
    assert result["ok"] is False


def test_set_crossfader_assignment_except_block(tools):
    tools.song = None
    result = tools.set_crossfader_assignment(0, 1)
    assert result["ok"] is False


def test_get_crossfader_position_except_block(tools):
    tools.song = None
    result = tools.get_crossfader_position()
    assert result["ok"] is False
