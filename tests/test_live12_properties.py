"""Tests for Live 12 track/clip/scene property tools."""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# get_clip_start_time / set_clip_start_time
# ---------------------------------------------------------------------------


def test_get_clip_start_time_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.start_time = 2.0
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is True
    assert result["start_time"] == 2.0


def test_get_clip_start_time_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.start_time
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is False


def test_get_clip_start_time_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is False


def test_get_clip_start_time_except_block(tools):
    tools.song = None
    result = tools.get_clip_start_time(0, 0)
    assert result["ok"] is False


def test_set_clip_start_time_with_attr(tools, song):
    result = tools.set_clip_start_time(0, 0, 4.0)
    assert result["ok"] is True


def test_set_clip_start_time_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.start_time
    result = tools.set_clip_start_time(0, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_start_time_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_start_time(0, 0, 4.0)
    assert result["ok"] is False


def test_set_clip_start_time_except_block(tools):
    tools.song = None
    result = tools.set_clip_start_time(0, 0, 1.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_track_is_foldable / get_track_is_frozen
# ---------------------------------------------------------------------------


def test_get_track_is_foldable_with_attr(tools, song):
    song.tracks[0].is_foldable = True
    result = tools.get_track_is_foldable(0)
    assert result["ok"] is True
    assert result["is_foldable"] is True


def test_get_track_is_foldable_without_attr(tools, song):
    del song.tracks[0].is_foldable
    result = tools.get_track_is_foldable(0)
    assert result["ok"] is False


def test_get_track_is_foldable_except_block(tools):
    tools.song = None
    result = tools.get_track_is_foldable(0)
    assert result["ok"] is False


def test_get_track_is_frozen_with_attr(tools, song):
    song.tracks[0].is_frozen = False
    result = tools.get_track_is_frozen(0)
    assert result["ok"] is True
    assert result["is_frozen"] is False


def test_get_track_is_frozen_without_attr(tools, song):
    del song.tracks[0].is_frozen
    result = tools.get_track_is_frozen(0)
    assert result["ok"] is False


def test_get_track_is_frozen_except_block(tools):
    tools.song = None
    result = tools.get_track_is_frozen(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_scene_is_empty
# ---------------------------------------------------------------------------


def test_get_scene_is_empty_with_is_empty_attr(tools, song):
    song.scenes[0].is_empty = True
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is True
    assert result["is_empty"] is True


def test_get_scene_is_empty_manual_check(tools, song):
    del song.scenes[0].is_empty
    clip_slot = MagicMock()
    clip_slot.has_clip = False
    song.tracks[0].clip_slots = [clip_slot]
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is True
    assert result["is_empty"] is True


def test_get_scene_is_empty_manual_not_empty(tools, song):
    del song.scenes[0].is_empty
    clip_slot = MagicMock()
    clip_slot.has_clip = True
    song.tracks[0].clip_slots = [clip_slot]
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is True
    assert result["is_empty"] is False


def test_get_scene_is_empty_exception(tools, song):
    song.scenes = None
    result = tools.get_scene_is_empty(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_scene_tempo
# ---------------------------------------------------------------------------


def test_get_scene_tempo_with_attr(tools, song):
    song.scenes[0].tempo = 128.0
    result = tools.get_scene_tempo(0)
    assert result["ok"] is True
    assert result["tempo"] == 128.0


def test_get_scene_tempo_without_attr(tools, song):
    del song.scenes[0].tempo
    result = tools.get_scene_tempo(0)
    assert result["ok"] is False


def test_get_scene_tempo_exception(tools, song):
    song.scenes[0].tempo = "bad"
    result = tools.get_scene_tempo(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_arrangement_overdub
# ---------------------------------------------------------------------------


def test_get_arrangement_overdub_with_attr(tools, song):
    song.arrangement_overdub = True
    result = tools.get_arrangement_overdub()
    assert result["ok"] is True
    assert result["arrangement_overdub"] is True


def test_get_arrangement_overdub_without_attr(tools, song):
    del song.arrangement_overdub
    result = tools.get_arrangement_overdub()
    assert result["ok"] is False


def test_get_arrangement_overdub_exception(tools, song):
    tools.song = None
    result = tools.get_arrangement_overdub()
    assert result["ok"] is False


def test_get_arrangement_overdub_except_block(tools):
    tools.song = None
    result = tools.get_arrangement_overdub()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_record_mode
# ---------------------------------------------------------------------------


def test_set_record_mode_with_attr(tools, song):
    result = tools.set_record_mode(1)
    assert result["ok"] is True


def test_set_record_mode_without_attr(tools, song):
    del song.record_mode
    result = tools.set_record_mode(1)
    assert result["ok"] is False


def test_set_record_mode_exception(tools):
    result = tools.set_record_mode("bad")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_signature_numerator / get_signature_denominator
# ---------------------------------------------------------------------------


def test_get_signature_numerator_with_attr(tools, song):
    song.signature_numerator = 4
    result = tools.get_signature_numerator()
    assert result["ok"] is True
    assert result["signature_numerator"] == 4


def test_get_signature_numerator_without_attr(tools, song):
    del song.signature_numerator
    result = tools.get_signature_numerator()
    assert result["ok"] is False


def test_get_signature_numerator_exception(tools, song):
    song.signature_numerator = "bad"
    result = tools.get_signature_numerator()
    assert result["ok"] is False


def test_get_signature_denominator_with_attr(tools, song):
    song.signature_denominator = 4
    result = tools.get_signature_denominator()
    assert result["ok"] is True
    assert result["signature_denominator"] == 4


def test_get_signature_denominator_without_attr(tools, song):
    del song.signature_denominator
    result = tools.get_signature_denominator()
    assert result["ok"] is False


def test_get_signature_denominator_exception(tools, song):
    song.signature_denominator = "bad"
    result = tools.get_signature_denominator()
    assert result["ok"] is False
