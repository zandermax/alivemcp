"""
Tests for ClipsMixin core clip operations.
"""

from unittest.mock import MagicMock


def test_create_midi_clip_success(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.create_midi_clip(0, 0, length=4.0)
    assert result["ok"] is True
    assert result["length"] == 4.0


def test_create_midi_clip_invalid_track(tools):
    result = tools.create_midi_clip(-1, 0)
    assert result["ok"] is False


def test_create_midi_clip_invalid_scene(tools, song):
    result = tools.create_midi_clip(0, 99)
    assert result["ok"] is False


def test_create_midi_clip_not_midi_track(tools, song):
    song.tracks[0].has_midi_input = False
    result = tools.create_midi_clip(0, 0)
    assert result == {"ok": False, "error": "Track is not a MIDI track"}


def test_create_midi_clip_slot_already_has_clip(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    result = tools.create_midi_clip(0, 0)
    assert result == {"ok": False, "error": "Clip slot already has a clip"}


def test_create_midi_clip_exception(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = False
    song.tracks[0].clip_slots[0].create_clip.side_effect = Exception("err")
    result = tools.create_midi_clip(0, 0)
    assert result["ok"] is False


def test_delete_clip_success(tools, song):
    result = tools.delete_clip(0, 0)
    assert result["ok"] is True
    song.tracks[0].clip_slots[0].delete_clip.assert_called_once()


def test_delete_clip_invalid_track(tools):
    result = tools.delete_clip(-1, 0)
    assert result["ok"] is False


def test_delete_clip_invalid_scene(tools, song):
    result = tools.delete_clip(0, 99)
    assert result["ok"] is False


def test_delete_clip_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.delete_clip(0, 0)
    assert result == {"ok": False, "error": "No clip in slot"}


def test_delete_clip_exception(tools, song):
    song.tracks[0].clip_slots[0].delete_clip.side_effect = Exception("err")
    result = tools.delete_clip(0, 0)
    assert result["ok"] is False


def test_duplicate_clip_success(tools, song):
    empty_slot = MagicMock()
    empty_slot.has_clip = False
    song.tracks[0].clip_slots = [song.tracks[0].clip_slots[0], empty_slot]
    song.scenes = [MagicMock(), MagicMock()]
    result = tools.duplicate_clip(0, 0)
    assert result["ok"] is True
    assert result["destination_clip_index"] == 1
    song.tracks[0].clip_slots[0].duplicate_clip_to.assert_called_once_with(empty_slot)


def test_duplicate_clip_no_empty_slot(tools, song):
    result = tools.duplicate_clip(0, 0)
    assert result["ok"] is False
    assert "No empty slot" in result["error"]


def test_duplicate_clip_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.duplicate_clip(0, 0)
    assert result["ok"] is False


def test_duplicate_clip_invalid_track(tools):
    result = tools.duplicate_clip(-1, 0)
    assert result["ok"] is False


def test_duplicate_clip_exception(tools, song):
    empty_slot = MagicMock()
    empty_slot.has_clip = False
    song.tracks[0].clip_slots = [song.tracks[0].clip_slots[0], empty_slot]
    song.scenes = [MagicMock(), MagicMock()]
    song.tracks[0].clip_slots[0].duplicate_clip_to.side_effect = Exception("err")
    result = tools.duplicate_clip(0, 0)
    assert result["ok"] is False


def test_launch_clip_success(tools, song):
    result = tools.launch_clip(0, 0)
    assert result["ok"] is True
    song.tracks[0].clip_slots[0].fire.assert_called_once()


def test_launch_clip_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.launch_clip(0, 0)
    assert result["ok"] is False


def test_launch_clip_invalid_track(tools):
    result = tools.launch_clip(-1, 0)
    assert result["ok"] is False


def test_launch_clip_exception(tools, song):
    song.tracks[0].clip_slots[0].fire.side_effect = Exception("err")
    result = tools.launch_clip(0, 0)
    assert result["ok"] is False


def test_stop_clip_success(tools, song):
    result = tools.stop_clip(0, 0)
    assert result["ok"] is True
    song.tracks[0].clip_slots[0].stop.assert_called_once()


def test_stop_clip_invalid_track(tools):
    result = tools.stop_clip(-1, 0)
    assert result["ok"] is False


def test_stop_clip_invalid_scene(tools, song):
    result = tools.stop_clip(0, 99)
    assert result["ok"] is False


def test_stop_clip_exception(tools, song):
    song.tracks[0].clip_slots[0].stop.side_effect = Exception("err")
    result = tools.stop_clip(0, 0)
    assert result["ok"] is False


def test_stop_all_clips_success(tools, song):
    result = tools.stop_all_clips()
    assert result["ok"] is True
    song.stop_all_clips.assert_called_once()


def test_stop_all_clips_exception(tools, song):
    song.stop_all_clips.side_effect = Exception("err")
    result = tools.stop_all_clips()
    assert result["ok"] is False


def test_get_clip_info_success(tools, song):
    result = tools.get_clip_info(0, 0)
    assert result["ok"] is True
    assert "name" in result
    assert "length" in result


def test_get_clip_info_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_info(0, 0)
    assert result["ok"] is False


def test_get_clip_info_invalid_track(tools):
    result = tools.get_clip_info(-1, 0)
    assert result["ok"] is False


def test_get_clip_info_exception(tools, song):
    song.tracks = None
    result = tools.get_clip_info(0, 0)
    assert result["ok"] is False


def test_set_clip_name_success(tools, song):
    result = tools.set_clip_name(0, 0, "My Clip")
    assert result["ok"] is True


def test_set_clip_name_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_name(0, 0, "x")
    assert result["ok"] is False


def test_set_clip_name_invalid_track(tools):
    result = tools.set_clip_name(-1, 0, "x")
    assert result["ok"] is False


def test_set_clip_name_exception(tools, song):
    song.tracks[0].clip_slots[0].clip.name = MagicMock(side_effect=Exception("err"))
    result = tools.set_clip_name(0, 0, "x")
    assert result["ok"] is True


def test_duplicate_clip_invalid_scene(tools, song):
    result = tools.duplicate_clip(0, 99)
    assert result["ok"] is False


def test_launch_clip_invalid_scene(tools, song):
    result = tools.launch_clip(0, 99)
    assert result["ok"] is False


def test_get_clip_info_invalid_scene(tools, song):
    result = tools.get_clip_info(0, 99)
    assert result["ok"] is False


def test_set_clip_name_invalid_scene(tools, song):
    result = tools.set_clip_name(0, 99, "x")
    assert result["ok"] is False


def test_set_clip_name_except_block(tools):
    tools.song = None
    result = tools.set_clip_name(0, 0, "x")
    assert result["ok"] is False


def test_create_midi_clip_keyword_clip_index(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.create_midi_clip(track_index=0, clip_index=0, length=2.0)
    assert result["ok"] is True
    assert result["clip_index"] == 0


def test_delete_clip_keyword_clip_index(tools, song):
    result = tools.delete_clip(track_index=0, clip_index=0)
    assert result["ok"] is True


def test_launch_clip_keyword_clip_index(tools, song):
    result = tools.launch_clip(track_index=0, clip_index=0)
    assert result["ok"] is True


def test_stop_clip_keyword_clip_index(tools, song):
    result = tools.stop_clip(track_index=0, clip_index=0)
    assert result["ok"] is True


def test_get_clip_info_keyword_clip_index(tools, song):
    result = tools.get_clip_info(track_index=0, clip_index=0)
    assert result["ok"] is True


def test_set_clip_name_keyword_clip_index(tools, song):
    result = tools.set_clip_name(track_index=0, clip_index=0, name="Test")
    assert result["ok"] is True
