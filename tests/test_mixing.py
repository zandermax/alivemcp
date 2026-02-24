"""
Tests for MixingMixin: sends, master, return tracks, crossfader, groove, groove pool.
"""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _song_with_send(value=0.7):
    send = MagicMock()
    send.value = value

    track = MagicMock()
    track.mixer_device.sends = [send]
    track.clip_slots = [MagicMock()]
    track.devices = [MagicMock()]

    clip_slot = MagicMock()
    clip_slot.has_clip = True

    s = MagicMock()
    s.tracks = [track]
    s.scenes = [MagicMock()]
    s.return_tracks = [MagicMock()]
    return s


# ---------------------------------------------------------------------------
# set_track_send
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# get_track_sends
# ---------------------------------------------------------------------------


def test_get_track_sends_success(tools, song):
    send = MagicMock()
    send.value = 0.5
    del send.name  # no name attribute
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
    song.tracks[0].mixer_device.sends = None  # for send in None → TypeError → ok=False
    result = tools.get_track_sends(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_master_track_info
# ---------------------------------------------------------------------------


def test_get_master_track_info_success(tools, song):
    result = tools.get_master_track_info()
    assert result["ok"] is True
    assert "name" in result
    assert "volume" in result


def test_get_master_track_info_exception(tools, song):
    song.master_track = None  # None.name → AttributeError → ok=False
    result = tools.get_master_track_info()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_master_volume
# ---------------------------------------------------------------------------


def test_set_master_volume_with_mixer_device(tools, song):
    result = tools.set_master_volume(0.8)
    assert result["ok"] is True


def test_set_master_volume_without_mixer_device(tools, song):
    del song.master_track.mixer_device
    result = tools.set_master_volume(0.8)
    assert result["ok"] is False


def test_set_master_volume_exception(tools, song):
    song.master_track = None  # hasattr(None, "mixer_device") = False → else → ok=False
    result = tools.set_master_volume(0.8)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_master_pan
# ---------------------------------------------------------------------------


def test_set_master_pan_with_mixer_device(tools, song):
    result = tools.set_master_pan(0.0)
    assert result["ok"] is True


def test_set_master_pan_without_mixer_device(tools, song):
    del song.master_track.mixer_device
    result = tools.set_master_pan(0.0)
    assert result["ok"] is False


def test_set_master_pan_exception(tools, song):
    song.master_track = None  # hasattr(None, "mixer_device") = False → else → ok=False
    result = tools.set_master_pan(0.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_master_devices
# ---------------------------------------------------------------------------


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
    song.master_track.devices = None  # for device in None → TypeError → ok=False
    result = tools.get_master_devices()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_return_track_count
# ---------------------------------------------------------------------------


def test_get_return_track_count(tools, song):
    song.return_tracks = [MagicMock(), MagicMock()]
    result = tools.get_return_track_count()
    assert result["ok"] is True
    assert result["count"] == 2


def test_get_return_track_count_exception(tools, song):
    song.return_tracks = None  # len(None) → TypeError → ok=False
    result = tools.get_return_track_count()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_return_track_info
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# set_return_track_volume
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# get_crossfader_assignment
# ---------------------------------------------------------------------------


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
    song.tracks[0].mixer_device.crossfade_assign = "bad"  # int("bad") → ValueError → ok=False
    result = tools.get_crossfader_assignment(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_crossfader_assignment
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# get_crossfader_position
# ---------------------------------------------------------------------------


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
    song.master_track = None  # hasattr(None, "mixer_device") = False → else → ok=False
    result = tools.get_crossfader_position()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_clip_groove_amount
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# quantize_clip
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# quantize_clip_pitch
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# get_groove_amount / set_groove_amount
# ---------------------------------------------------------------------------


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
    song.groove_amount = "bad"  # float("bad") → ValueError → ok=False
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


# ---------------------------------------------------------------------------
# get_groove_pool_grooves
# ---------------------------------------------------------------------------


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
    song.groove_pool = None  # for groove in None → TypeError → ok=False
    result = tools.get_groove_pool_grooves()
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_clip_groove
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Additional coverage: invalid index branches and except blocks
# ---------------------------------------------------------------------------


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
