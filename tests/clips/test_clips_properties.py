"""
Tests for ClipsMixin clip properties (looping, markers, color, annotation, fades, RAM).
"""

from unittest.mock import MagicMock


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
