"""
Tests for TracksMixin core track creation and basic controls.
"""

from unittest.mock import MagicMock


def test_create_midi_track_no_name(tools, song):
    song.tracks = MagicMock()
    result = tools.create_midi_track()
    assert result["ok"] is True
    song.create_midi_track.assert_called_once()


def test_create_midi_track_with_name(tools, song):
    song.tracks = MagicMock()
    result = tools.create_midi_track(name="Synth")
    assert result["ok"] is True


def test_create_midi_track_exception(tools, song):
    song.create_midi_track.side_effect = Exception("err")
    result = tools.create_midi_track()
    assert result == {"ok": False, "error": "err"}


def test_create_audio_track_no_name(tools, song):
    song.tracks = MagicMock()
    result = tools.create_audio_track()
    assert result["ok"] is True


def test_create_audio_track_with_name(tools, song):
    song.tracks = MagicMock()
    result = tools.create_audio_track(name="Drums")
    assert result["ok"] is True


def test_create_audio_track_exception(tools, song):
    song.create_audio_track.side_effect = Exception("err")
    result = tools.create_audio_track()
    assert result["ok"] is False


def test_create_return_track(tools, song):
    result = tools.create_return_track()
    assert result["ok"] is True
    song.create_return_track.assert_called_once()


def test_create_return_track_exception(tools, song):
    song.create_return_track.side_effect = Exception("err")
    result = tools.create_return_track()
    assert result["ok"] is False


def test_delete_track_valid(tools, song):
    result = tools.delete_track(0)
    assert result["ok"] is True
    song.delete_track.assert_called_once_with(0)


def test_delete_track_negative_index(tools):
    result = tools.delete_track(-1)
    assert result == {"ok": False, "error": "Invalid track index"}


def test_delete_track_out_of_range(tools, song):
    result = tools.delete_track(len(song.tracks))
    assert result["ok"] is False


def test_delete_track_exception(tools, song):
    song.delete_track.side_effect = Exception("err")
    result = tools.delete_track(0)
    assert result["ok"] is False


def test_duplicate_track_valid(tools, song):
    result = tools.duplicate_track(0)
    assert result["ok"] is True
    assert result["new_index"] == 1


def test_duplicate_track_invalid(tools, song):
    result = tools.duplicate_track(5)
    assert result["ok"] is False


def test_duplicate_track_exception(tools, song):
    song.duplicate_track.side_effect = Exception("err")
    result = tools.duplicate_track(0)
    assert result["ok"] is False


def test_rename_track_valid(tools, song):
    result = tools.rename_track(0, "Bass")
    assert result["ok"] is True
    assert result["name"] == "Bass"


def test_rename_track_invalid(tools, song):
    result = tools.rename_track(99, "x")
    assert result["ok"] is False


def test_rename_track_exception(tools, song):
    song.tracks[0].name = MagicMock(side_effect=Exception("err"))
    result = tools.rename_track(0, "Bass")
    assert result["ok"] is True


def test_set_track_volume_valid(tools, song):
    result = tools.set_track_volume(0, 0.8)
    assert result["ok"] is True


def test_set_track_volume_negative_index(tools):
    result = tools.set_track_volume(-1, 0.5)
    assert result["ok"] is False


def test_set_track_volume_invalid_index(tools, song):
    result = tools.set_track_volume(10, 0.5)
    assert result["ok"] is False


def test_set_track_volume_too_low(tools, song):
    result = tools.set_track_volume(0, -0.1)
    assert result == {"ok": False, "error": "Volume must be between 0.0 and 1.0"}


def test_set_track_volume_too_high(tools, song):
    result = tools.set_track_volume(0, 1.1)
    assert result["ok"] is False


def test_set_track_volume_exception(tools, song):
    song.tracks[0].mixer_device.volume.value = MagicMock(side_effect=Exception("err"))
    result = tools.set_track_volume(0, "bad")
    assert result["ok"] is False


def test_set_track_pan_valid(tools, song):
    result = tools.set_track_pan(0, 0.5)
    assert result["ok"] is True


def test_set_track_pan_invalid_index(tools):
    result = tools.set_track_pan(-1, 0)
    assert result["ok"] is False


def test_set_track_pan_too_low(tools, song):
    result = tools.set_track_pan(0, -1.5)
    assert result == {"ok": False, "error": "Pan must be between -1.0 and 1.0"}


def test_set_track_pan_too_high(tools, song):
    result = tools.set_track_pan(0, 1.5)
    assert result["ok"] is False


def test_set_track_pan_exception(tools):
    result = tools.set_track_pan(0, "bad")
    assert result["ok"] is False


def test_arm_track_can_be_armed(tools, song):
    song.tracks[0].can_be_armed = True
    result = tools.arm_track(0, armed=True)
    assert result["ok"] is True


def test_arm_track_cannot_be_armed(tools, song):
    song.tracks[0].can_be_armed = False
    result = tools.arm_track(0, armed=True)
    assert result == {"ok": False, "error": "Track cannot be armed"}


def test_arm_track_invalid_index(tools):
    result = tools.arm_track(-1)
    assert result["ok"] is False


def test_arm_track_exception(tools, song):
    del song.tracks[0].can_be_armed
    result = tools.arm_track(0)
    assert result["ok"] is False


def test_solo_track_valid(tools, song):
    result = tools.solo_track(0, solo=True)
    assert result["ok"] is True


def test_solo_track_invalid(tools):
    result = tools.solo_track(-1)
    assert result["ok"] is False


def test_solo_track_exception(tools, song):
    song.tracks[0].solo = MagicMock(side_effect=Exception("x"))
    result = tools.solo_track(0)
    assert result["ok"] is True


def test_mute_track_valid(tools, song):
    result = tools.mute_track(0, mute=True)
    assert result["ok"] is True


def test_mute_track_invalid(tools):
    result = tools.mute_track(99)
    assert result["ok"] is False


def test_mute_track_exception(tools, song):
    song.tracks[0].mute = MagicMock(side_effect=Exception("x"))
    result = tools.mute_track(0)
    assert result["ok"] is True


def test_get_track_info_valid(tools, song):
    track = song.tracks[0]
    track.can_be_armed = True
    clip_slot = MagicMock()
    clip_slot.has_clip = True
    track.clip_slots = [clip_slot]
    track.devices = [MagicMock()]
    result = tools.get_track_info(0)
    assert result["ok"] is True
    assert result["track_index"] == 0


def test_get_track_info_invalid(tools):
    result = tools.get_track_info(-1)
    assert result["ok"] is False


def test_get_track_info_exception(tools, song):
    song.tracks = None
    result = tools.get_track_info(0)
    assert result["ok"] is False


def test_set_track_color_with_color_attr(tools, song):
    result = tools.set_track_color(0, 5)
    assert result["ok"] is True


def test_set_track_color_without_color_attr(tools, song):
    del song.tracks[0].color
    result = tools.set_track_color(0, 5)
    assert result == {"ok": False, "error": "Track color not supported"}


def test_set_track_color_invalid_index(tools):
    result = tools.set_track_color(-1, 5)
    assert result["ok"] is False


def test_set_track_color_exception(tools, song):
    song.tracks[0].color = MagicMock(side_effect=Exception("x"))
    result = tools.set_track_color(0, "bad")
    assert result["ok"] is False


def test_set_track_fold_state_foldable(tools, song):
    song.tracks[0].is_foldable = True
    result = tools.set_track_fold_state(0, True)
    assert result["ok"] is True


def test_set_track_fold_state_not_foldable(tools, song):
    song.tracks[0].is_foldable = False
    result = tools.set_track_fold_state(0, True)
    assert result == {"ok": False, "error": "Track is not foldable"}


def test_set_track_fold_state_invalid(tools):
    result = tools.set_track_fold_state(-1, True)
    assert result["ok"] is False


def test_set_track_fold_state_exception(tools, song):
    song.tracks = None
    result = tools.set_track_fold_state(0, True)
    assert result["ok"] is False
