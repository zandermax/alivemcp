"""
Tests for ClipsMixin: clip operations, extras, color, annotations, fades,
RAM mode, and follow actions.
"""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _song_with_clip(has_clip=True, is_midi=True, is_audio=False):
    """Build a minimal song mock with one track/scene containing a clip slot."""
    clip = MagicMock()
    clip.is_midi_clip = is_midi
    clip.is_audio_clip = is_audio

    clip_slot = MagicMock()
    clip_slot.has_clip = has_clip
    clip_slot.clip = clip

    track = MagicMock()
    track.has_midi_input = is_midi
    track.clip_slots = [clip_slot]
    track.devices = [MagicMock()]

    s = MagicMock()
    s.tracks = [track]
    s.scenes = [MagicMock()]
    s.return_tracks = [MagicMock()]
    return s


# ---------------------------------------------------------------------------
# create_midi_clip
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# delete_clip
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# duplicate_clip
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# launch_clip / stop_clip / stop_all_clips
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# get_clip_info
# ---------------------------------------------------------------------------


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
    song.tracks = None  # len(None) → TypeError → ok=False
    result = tools.get_clip_info(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_clip_name
# ---------------------------------------------------------------------------


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
    assert result["ok"] is True  # MagicMock assignment doesn't raise


# ---------------------------------------------------------------------------
# Clip extras: looping, loop_start, loop_end, markers, muted, gain, pitch, sig
# ---------------------------------------------------------------------------


def _clip_extras_setup(song, has_clip=True):
    """Configure clip_slots so extras tests find a clip."""
    song.tracks[0].clip_slots[0].has_clip = has_clip


def test_set_clip_looping_success(tools, song):
    result = tools.set_clip_looping(0, 0, True)
    assert result["ok"] is True


def test_set_clip_looping_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_looping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_looping_invalid_track(tools):
    result = tools.set_clip_looping(-1, 0, True)
    assert result["ok"] is False


def test_set_clip_looping_invalid_clip_index(tools, song):
    result = tools.set_clip_looping(0, 99, True)
    assert result["ok"] is False


def test_set_clip_looping_exception(tools, song):
    song.tracks[0].clip_slots[0].clip.looping = MagicMock(side_effect=Exception("x"))
    result = tools.set_clip_looping(0, 0, True)
    assert result["ok"] is True


def test_set_clip_loop_start_success(tools, song):
    result = tools.set_clip_loop_start(0, 0, 2.0)
    assert result["ok"] is True


def test_set_clip_loop_start_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_loop_start(0, 0, 2.0)
    assert result["ok"] is False


def test_set_clip_loop_start_exception(tools):
    result = tools.set_clip_loop_start(0, 0, "bad")
    assert result["ok"] is False


def test_set_clip_loop_end_success(tools, song):
    result = tools.set_clip_loop_end(0, 0, 4.0)
    assert result["ok"] is True


def test_set_clip_loop_end_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_loop_end(0, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_start_marker_success(tools, song):
    result = tools.set_clip_start_marker(0, 0, 0.0)
    assert result["ok"] is True


def test_set_clip_start_marker_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_start_marker(0, 0, 0.0)
    assert result["ok"] is False


def test_set_clip_end_marker_success(tools, song):
    result = tools.set_clip_end_marker(0, 0, 4.0)
    assert result["ok"] is True


def test_set_clip_end_marker_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_end_marker(0, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_muted_success(tools, song):
    result = tools.set_clip_muted(0, 0, True)
    assert result["ok"] is True


def test_set_clip_muted_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_muted(0, 0, True)
    assert result["ok"] is False


def test_set_clip_gain_with_attr(tools, song):
    result = tools.set_clip_gain(0, 0, 0.8)
    assert result["ok"] is True


def test_set_clip_gain_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.gain
    result = tools.set_clip_gain(0, 0, 0.8)
    assert result["ok"] is False


def test_set_clip_gain_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_gain(0, 0, 0.8)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_with_attr(tools, song):
    result = tools.set_clip_pitch_coarse(0, 0, 3)
    assert result["ok"] is True


def test_set_clip_pitch_coarse_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.pitch_coarse
    result = tools.set_clip_pitch_coarse(0, 0, 3)
    assert result["ok"] is False


def test_set_clip_pitch_fine_with_attr(tools, song):
    result = tools.set_clip_pitch_fine(0, 0, 50)
    assert result["ok"] is True


def test_set_clip_pitch_fine_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.pitch_fine
    result = tools.set_clip_pitch_fine(0, 0, 50)
    assert result["ok"] is False


def test_set_clip_signature_numerator_success(tools, song):
    result = tools.set_clip_signature_numerator(0, 0, 3)
    assert result["ok"] is True


def test_set_clip_signature_numerator_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_signature_numerator(0, 0, 3)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Clip color
# ---------------------------------------------------------------------------


def test_set_clip_color_via_color_index(tools, song):
    result = tools.set_clip_color(0, 0, 12)
    assert result["ok"] is True


def test_set_clip_color_via_color(tools, song):
    del song.tracks[0].clip_slots[0].clip.color_index
    result = tools.set_clip_color(0, 0, 12)
    assert result["ok"] is True


def test_set_clip_color_no_color_attrs(tools, song):
    del song.tracks[0].clip_slots[0].clip.color_index
    del song.tracks[0].clip_slots[0].clip.color
    result = tools.set_clip_color(0, 0, 12)
    assert result["ok"] is False


def test_set_clip_color_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_color(0, 0, 12)
    assert result["ok"] is False


def test_set_clip_color_invalid_track(tools):
    result = tools.set_clip_color(-1, 0, 12)
    assert result["ok"] is False


def test_set_clip_color_invalid_clip(tools, song):
    result = tools.set_clip_color(0, 99, 12)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Annotations
# ---------------------------------------------------------------------------


def test_get_clip_annotation_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.annotation = "hello"
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is True
    assert result["annotation"] == "hello"


def test_get_clip_annotation_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.annotation
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is False


def test_get_clip_annotation_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is False


def test_set_clip_annotation_with_attr(tools, song):
    result = tools.set_clip_annotation(0, 0, "note")
    assert result["ok"] is True


def test_set_clip_annotation_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.annotation
    result = tools.set_clip_annotation(0, 0, "note")
    assert result["ok"] is False


def test_set_clip_annotation_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_annotation(0, 0, "note")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Fade in/out
# ---------------------------------------------------------------------------


def test_get_clip_fade_in_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.fade_in_time = 1.0
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is True
    assert result["fade_in_time"] == 1.0


def test_get_clip_fade_in_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_in_time
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is False


def test_get_clip_fade_in_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_in_with_attr(tools, song):
    result = tools.set_clip_fade_in(0, 0, 0.5)
    assert result["ok"] is True


def test_set_clip_fade_in_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_in_time
    result = tools.set_clip_fade_in(0, 0, 0.5)
    assert result["ok"] is False


def test_set_clip_fade_in_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_fade_in(0, 0, 0.5)
    assert result["ok"] is False


def test_get_clip_fade_out_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.fade_out_time = 2.0
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is True


def test_get_clip_fade_out_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_out_time
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is False


def test_get_clip_fade_out_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_out_with_attr(tools, song):
    result = tools.set_clip_fade_out(0, 0, 1.0)
    assert result["ok"] is True


def test_set_clip_fade_out_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.fade_out_time
    result = tools.set_clip_fade_out(0, 0, 1.0)
    assert result["ok"] is False


def test_set_clip_fade_out_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_fade_out(0, 0, 1.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# RAM mode
# ---------------------------------------------------------------------------


def test_get_clip_ram_mode_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.ram_mode = True
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is True
    assert result["ram_mode"] is True


def test_get_clip_ram_mode_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.ram_mode
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is False


def test_get_clip_ram_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is False


def test_set_clip_ram_mode_with_attr(tools, song):
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is True


def test_set_clip_ram_mode_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.ram_mode
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is False


def test_set_clip_ram_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Follow actions
# ---------------------------------------------------------------------------


def test_get_clip_follow_action_success(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.follow_action_A = 1
    clip.follow_action_B = 0
    clip.follow_action_time = 4.0
    clip.follow_action_chance_A = 1.0
    clip.follow_action_chance_B = 0.0
    result = tools.get_clip_follow_action(0, 0)
    assert result["ok"] is True


def test_get_clip_follow_action_invalid_track(tools):
    result = tools.get_clip_follow_action(-1, 0)
    assert result["ok"] is False


def test_get_clip_follow_action_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_follow_action(0, 0)
    assert result["ok"] is False


def test_get_clip_follow_action_exception(tools, song):
    song.tracks = None  # len(None) → TypeError → ok=False
    result = tools.get_clip_follow_action(0, 0)
    assert result["ok"] is False


def test_set_clip_follow_action_success(tools, song):
    result = tools.set_clip_follow_action(0, 0, 3, 0, chance_A=0.8)
    assert result["ok"] is True


def test_set_clip_follow_action_invalid_track(tools):
    result = tools.set_clip_follow_action(-1, 0, 1, 0)
    assert result["ok"] is False


def test_set_clip_follow_action_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_follow_action(0, 0, 1, 0)
    assert result["ok"] is False


def test_set_clip_follow_action_exception(tools, song):
    song.tracks = None  # len(None) → TypeError → ok=False
    result = tools.set_clip_follow_action(0, 0, 1, 0)
    assert result["ok"] is False


def test_set_follow_action_time_with_attr(tools, song):
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is True


def test_set_follow_action_time_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.follow_action_time
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is False


def test_set_follow_action_time_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is False


def test_set_follow_action_time_invalid_track(tools):
    result = tools.set_follow_action_time(-1, 0, 2.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Additional coverage: invalid scene/clip index branches and except blocks
# ---------------------------------------------------------------------------


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


def test_set_clip_looping_except_block(tools):
    tools.song = None
    result = tools.set_clip_looping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_loop_start_invalid_track(tools):
    result = tools.set_clip_loop_start(-1, 0, 0.0)
    assert result["ok"] is False


def test_set_clip_loop_start_invalid_clip(tools, song):
    result = tools.set_clip_loop_start(0, 99, 0.0)
    assert result["ok"] is False


def test_set_clip_loop_end_invalid_track(tools):
    result = tools.set_clip_loop_end(-1, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_loop_end_invalid_clip(tools, song):
    result = tools.set_clip_loop_end(0, 99, 4.0)
    assert result["ok"] is False


def test_set_clip_loop_end_except_block(tools):
    tools.song = None
    result = tools.set_clip_loop_end(0, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_start_marker_invalid_track(tools):
    result = tools.set_clip_start_marker(-1, 0, 0.0)
    assert result["ok"] is False


def test_set_clip_start_marker_invalid_clip(tools, song):
    result = tools.set_clip_start_marker(0, 99, 0.0)
    assert result["ok"] is False


def test_set_clip_start_marker_except_block(tools):
    tools.song = None
    result = tools.set_clip_start_marker(0, 0, 0.0)
    assert result["ok"] is False


def test_set_clip_end_marker_invalid_track(tools):
    result = tools.set_clip_end_marker(-1, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_end_marker_invalid_clip(tools, song):
    result = tools.set_clip_end_marker(0, 99, 4.0)
    assert result["ok"] is False


def test_set_clip_end_marker_except_block(tools):
    tools.song = None
    result = tools.set_clip_end_marker(0, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_muted_invalid_track(tools):
    result = tools.set_clip_muted(-1, 0, True)
    assert result["ok"] is False


def test_set_clip_muted_invalid_clip(tools, song):
    result = tools.set_clip_muted(0, 99, True)
    assert result["ok"] is False


def test_set_clip_muted_except_block(tools):
    tools.song = None
    result = tools.set_clip_muted(0, 0, True)
    assert result["ok"] is False


def test_set_clip_gain_invalid_track(tools):
    result = tools.set_clip_gain(-1, 0, 0.5)
    assert result["ok"] is False


def test_set_clip_gain_invalid_clip(tools, song):
    result = tools.set_clip_gain(0, 99, 0.5)
    assert result["ok"] is False


def test_set_clip_gain_except_block(tools):
    tools.song = None
    result = tools.set_clip_gain(0, 0, 0.5)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_invalid_track(tools):
    result = tools.set_clip_pitch_coarse(-1, 0, 3)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_invalid_clip(tools, song):
    result = tools.set_clip_pitch_coarse(0, 99, 3)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_pitch_coarse(0, 0, 3)
    assert result["ok"] is False


def test_set_clip_pitch_fine_invalid_track(tools):
    result = tools.set_clip_pitch_fine(-1, 0, 50)
    assert result["ok"] is False


def test_set_clip_pitch_fine_invalid_clip(tools, song):
    result = tools.set_clip_pitch_fine(0, 99, 50)
    assert result["ok"] is False


def test_set_clip_pitch_fine_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_pitch_fine(0, 0, 50)
    assert result["ok"] is False


def test_set_clip_pitch_fine_except_block(tools):
    tools.song = None
    result = tools.set_clip_pitch_fine(0, 0, 50)
    assert result["ok"] is False


def test_set_clip_signature_numerator_invalid_track(tools):
    result = tools.set_clip_signature_numerator(-1, 0, 4)
    assert result["ok"] is False


def test_set_clip_signature_numerator_invalid_clip(tools, song):
    result = tools.set_clip_signature_numerator(0, 99, 4)
    assert result["ok"] is False


def test_set_clip_signature_numerator_except_block(tools):
    tools.song = None
    result = tools.set_clip_signature_numerator(0, 0, 4)
    assert result["ok"] is False


def test_set_clip_color_except_block(tools):
    tools.song = None
    result = tools.set_clip_color(0, 0, 5)
    assert result["ok"] is False


def test_set_clip_pitch_coarse_except_block(tools):
    tools.song = None
    result = tools.set_clip_pitch_coarse(0, 0, 3)
    assert result["ok"] is False


def test_get_clip_annotation_except_block(tools):
    tools.song = None
    result = tools.get_clip_annotation(0, 0)
    assert result["ok"] is False


def test_set_clip_annotation_except_block(tools):
    tools.song = None
    result = tools.set_clip_annotation(0, 0, "x")
    assert result["ok"] is False


def test_get_clip_fade_in_except_block(tools):
    tools.song = None
    result = tools.get_clip_fade_in(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_in_except_block(tools):
    tools.song = None
    result = tools.set_clip_fade_in(0, 0, 0.1)
    assert result["ok"] is False


def test_get_clip_fade_out_except_block(tools):
    tools.song = None
    result = tools.get_clip_fade_out(0, 0)
    assert result["ok"] is False


def test_set_clip_fade_out_except_block(tools):
    tools.song = None
    result = tools.set_clip_fade_out(0, 0, 0.1)
    assert result["ok"] is False


def test_get_clip_ram_mode_except_block(tools):
    tools.song = None
    result = tools.get_clip_ram_mode(0, 0)
    assert result["ok"] is False


def test_set_clip_ram_mode_except_block(tools):
    tools.song = None
    result = tools.set_clip_ram_mode(0, 0, True)
    assert result["ok"] is False


def test_get_clip_follow_action_invalid_clip(tools, song):
    result = tools.get_clip_follow_action(0, 99)
    assert result["ok"] is False


def test_set_clip_follow_action_invalid_clip(tools, song):
    result = tools.set_clip_follow_action(0, 99, 1, 2)
    assert result["ok"] is False


def test_set_follow_action_time_invalid_clip(tools, song):
    result = tools.set_follow_action_time(0, 99, 2.0)
    assert result["ok"] is False


def test_set_follow_action_time_except_block(tools):
    tools.song = None
    result = tools.set_follow_action_time(0, 0, 2.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Keyword-arg tests: lock in clip_index as the canonical parameter name
# ---------------------------------------------------------------------------


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
