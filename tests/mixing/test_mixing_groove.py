"""
Tests for MixingMixin groove and quantize-related methods.
"""

from unittest.mock import MagicMock


def test_set_clip_groove_amount_with_attr(tools, song):
    result = tools.set_clip_groove_amount(0, 0, 0.5)
    assert result["ok"] is True


def test_set_clip_groove_amount_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.groove_amount
    result = tools.set_clip_groove_amount(0, 0, 0.5)
    assert result["ok"] is False


def test_set_clip_groove_amount_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_groove_amount(0, 0, 0.5)
    assert result["ok"] is False


def test_set_clip_groove_amount_invalid(tools):
    result = tools.set_clip_groove_amount(-1, 0, 0.5)
    assert result["ok"] is False


def test_quantize_clip_with_quantize_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    result = tools.quantize_clip(0, 0, 0.25)
    assert result["ok"] is True


def test_quantize_clip_without_quantize_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    del song.tracks[0].clip_slots[0].clip.quantize
    result = tools.quantize_clip(0, 0, 0.25)
    assert result["ok"] is False


def test_quantize_clip_no_midi_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.quantize_clip(0, 0, 0.25)
    assert result["ok"] is False


def test_quantize_clip_invalid(tools):
    result = tools.quantize_clip(-1, 0, 0.25)
    assert result["ok"] is False


def test_quantize_clip_pitch_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    result = tools.quantize_clip_pitch(0, 0, pitch=60)
    assert result["ok"] is True


def test_quantize_clip_pitch_without_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    del song.tracks[0].clip_slots[0].clip.quantize_pitch
    result = tools.quantize_clip_pitch(0, 0, pitch=60)
    assert result["ok"] is False


def test_quantize_clip_pitch_no_midi_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.quantize_clip_pitch(0, 0)
    assert result["ok"] is False


def test_get_groove_amount_with_attr(tools, song):
    song.groove_amount = 0.3
    result = tools.get_groove_amount()
    assert result["ok"] is True
    assert result["groove_amount"] == 0.3


def test_get_groove_amount_without_attr(tools, song):
    del song.groove_amount
    result = tools.get_groove_amount()
    assert result["ok"] is False


def test_get_groove_amount_exception(tools, song):
    song.groove_amount = "bad"
    result = tools.get_groove_amount()
    assert result["ok"] is False


def test_set_groove_amount_with_attr(tools, song):
    result = tools.set_groove_amount(0.5)
    assert result["ok"] is True


def test_set_groove_amount_without_attr(tools, song):
    del song.groove_amount
    result = tools.set_groove_amount(0.5)
    assert result["ok"] is False


def test_set_groove_amount_exception(tools):
    result = tools.set_groove_amount("bad")
    assert result["ok"] is False


def test_get_groove_pool_grooves_with_pool(tools, song):
    groove = MagicMock()
    groove.name = "Swing 8"
    groove.timing_amount = 0.5
    groove.random_amount = 0.1
    groove.velocity_amount = 0.3
    song.groove_pool = [groove]
    result = tools.get_groove_pool_grooves()
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_groove_pool_grooves_without_pool(tools, song):
    del song.groove_pool
    result = tools.get_groove_pool_grooves()
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_groove_pool_grooves_groove_no_name(tools, song):
    groove = MagicMock()
    del groove.name
    song.groove_pool = [groove]
    result = tools.get_groove_pool_grooves()
    assert result["ok"] is True


def test_get_groove_pool_grooves_exception(tools, song):
    song.groove_pool = None
    result = tools.get_groove_pool_grooves()
    assert result["ok"] is False


def test_set_clip_groove_valid(tools, song):
    groove = MagicMock()
    song.groove_pool = [groove]
    result = tools.set_clip_groove(0, 0, 0)
    assert result["ok"] is True


def test_set_clip_groove_invalid_groove_index(tools, song):
    song.groove_pool = []
    result = tools.set_clip_groove(0, 0, 0)
    assert result["ok"] is False


def test_set_clip_groove_without_groove_pool(tools, song):
    del song.groove_pool
    result = tools.set_clip_groove(0, 0, 0)
    assert result["ok"] is False


def test_set_clip_groove_clip_no_groove_attr(tools, song):
    groove = MagicMock()
    song.groove_pool = [groove]
    del song.tracks[0].clip_slots[0].clip.groove
    result = tools.set_clip_groove(0, 0, 0)
    assert result["ok"] is False


def test_set_clip_groove_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_groove(0, 0, 0)
    assert result["ok"] is False


def test_set_clip_groove_invalid_track(tools):
    result = tools.set_clip_groove(-1, 0, 0)
    assert result["ok"] is False


def test_set_clip_groove_exception(tools, song):
    song.tracks[0].clip_slots[0].has_clip = MagicMock(side_effect=Exception("err"))
    result = tools.set_clip_groove(0, 0, 0)
    assert result["ok"] is False


def test_set_clip_groove_amount_invalid_clip(tools, song):
    result = tools.set_clip_groove_amount(0, 99, 0.5)
    assert result["ok"] is False


def test_set_clip_groove_amount_except_block(tools):
    tools.song = None
    result = tools.set_clip_groove_amount(0, 0, 0.5)
    assert result["ok"] is False


def test_quantize_clip_invalid_clip(tools, song):
    result = tools.quantize_clip(0, 99, 0.25)
    assert result["ok"] is False


def test_quantize_clip_except_block(tools):
    tools.song = None
    result = tools.quantize_clip(0, 0, 0.25)
    assert result["ok"] is False


def test_quantize_clip_pitch_invalid_track(tools):
    result = tools.quantize_clip_pitch(-1, 0)
    assert result["ok"] is False


def test_quantize_clip_pitch_invalid_clip(tools, song):
    result = tools.quantize_clip_pitch(0, 99)
    assert result["ok"] is False


def test_quantize_clip_pitch_except_block(tools):
    tools.song = None
    result = tools.quantize_clip_pitch(0, 0)
    assert result["ok"] is False


def test_set_clip_groove_invalid_clip(tools, song):
    result = tools.set_clip_groove(0, 99, 0)
    assert result["ok"] is False


def test_set_clip_groove_except_block(tools):
    tools.song = None
    result = tools.set_clip_groove(0, 0, 0)
    assert result["ok"] is False
