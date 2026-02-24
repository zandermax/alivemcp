"""
Tests for AutomationMixin: clip automation envelope operations.
"""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _setup_song_with_clip_and_device(song):
    """Configure the song fixture with a clip and a device with one parameter."""
    clip = MagicMock()
    clip_slot = MagicMock()
    clip_slot.has_clip = True
    clip_slot.clip = clip

    param = MagicMock()
    param.name = "Volume"

    device = MagicMock()
    device.name = "EQ"
    device.parameters = [param]

    song.tracks[0].clip_slots = [clip_slot]
    song.tracks[0].devices = [device]
    return clip, param, device


# ---------------------------------------------------------------------------
# get_clip_automation_envelope
# ---------------------------------------------------------------------------


def test_get_clip_automation_envelope_has_envelope(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    envelope = MagicMock()
    clip.automation_envelope.return_value = envelope
    result = tools.get_clip_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is True
    assert result["has_envelope"] is True


def test_get_clip_automation_envelope_no_envelope_result(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    clip.automation_envelope.return_value = None
    result = tools.get_clip_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is True
    assert result["has_envelope"] is False


def test_get_clip_automation_envelope_no_automation_envelope_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    del clip.automation_envelope
    result = tools.get_clip_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


def test_get_clip_automation_envelope_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_automation_envelope(0, 0, 0, 0)
    assert result == {"ok": False, "error": "No clip in slot"}


def test_get_clip_automation_envelope_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.get_clip_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# create_automation_envelope
# ---------------------------------------------------------------------------


def test_create_automation_envelope_with_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    result = tools.create_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is True
    clip.create_automation_envelope.assert_called_once_with(param)


def test_create_automation_envelope_without_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    del clip.create_automation_envelope
    result = tools.create_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


def test_create_automation_envelope_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.create_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


def test_create_automation_envelope_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.create_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# clear_automation_envelope
# ---------------------------------------------------------------------------


def test_clear_automation_envelope_with_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    result = tools.clear_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is True
    clip.clear_envelope.assert_called_once_with(param)


def test_clear_automation_envelope_without_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    del clip.clear_envelope
    result = tools.clear_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


def test_clear_automation_envelope_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.clear_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


def test_clear_automation_envelope_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.clear_automation_envelope(0, 0, 0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# insert_automation_step
# ---------------------------------------------------------------------------


def test_insert_automation_step_with_insert_step(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    envelope = MagicMock()
    clip.automation_envelope.return_value = envelope
    result = tools.insert_automation_step(0, 0, 0, 0, 1.0, 0.5)
    assert result["ok"] is True
    envelope.insert_step.assert_called_once_with(1.0, 0.5)


def test_insert_automation_step_no_envelope(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    clip.automation_envelope.return_value = None
    result = tools.insert_automation_step(0, 0, 0, 0, 1.0, 0.5)
    assert result["ok"] is False


def test_insert_automation_step_no_insert_step_method(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    envelope = MagicMock()
    del envelope.insert_step
    clip.automation_envelope.return_value = envelope
    result = tools.insert_automation_step(0, 0, 0, 0, 1.0, 0.5)
    assert result["ok"] is False


def test_insert_automation_step_no_automation_envelope_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    del clip.automation_envelope
    result = tools.insert_automation_step(0, 0, 0, 0, 1.0, 0.5)
    assert result["ok"] is False


def test_insert_automation_step_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.insert_automation_step(0, 0, 0, 0, 1.0, 0.5)
    assert result["ok"] is False


def test_insert_automation_step_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.insert_automation_step(0, 0, 0, 0, 1.0, 0.5)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# remove_automation_step
# ---------------------------------------------------------------------------


def test_remove_automation_step_with_remove_step(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    envelope = MagicMock()
    clip.automation_envelope.return_value = envelope
    result = tools.remove_automation_step(0, 0, 0, 0, 2.0)
    assert result["ok"] is True
    envelope.remove_step.assert_called_once_with(2.0)


def test_remove_automation_step_no_envelope(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    clip.automation_envelope.return_value = None
    result = tools.remove_automation_step(0, 0, 0, 0, 2.0)
    assert result["ok"] is False


def test_remove_automation_step_no_remove_step_method(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    envelope = MagicMock()
    del envelope.remove_step
    clip.automation_envelope.return_value = envelope
    result = tools.remove_automation_step(0, 0, 0, 0, 2.0)
    assert result["ok"] is False


def test_remove_automation_step_no_automation_envelope_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    del clip.automation_envelope
    result = tools.remove_automation_step(0, 0, 0, 0, 2.0)
    assert result["ok"] is False


def test_remove_automation_step_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.remove_automation_step(0, 0, 0, 0, 2.0)
    assert result["ok"] is False


def test_remove_automation_step_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.remove_automation_step(0, 0, 0, 0, 2.0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_automation_envelope_values
# ---------------------------------------------------------------------------


def test_get_automation_envelope_values_has_envelope(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    envelope = MagicMock()
    clip.automation_envelope.return_value = envelope
    result = tools.get_automation_envelope_values(0, 0, 0, 0)
    assert result["ok"] is True
    assert result["has_envelope"] is True


def test_get_automation_envelope_values_no_envelope(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    clip.automation_envelope.return_value = None
    result = tools.get_automation_envelope_values(0, 0, 0, 0)
    assert result["ok"] is True
    assert result["has_envelope"] is False


def test_get_automation_envelope_values_no_attr(tools, song):
    clip, param, device = _setup_song_with_clip_and_device(song)
    del clip.automation_envelope
    result = tools.get_automation_envelope_values(0, 0, 0, 0)
    assert result["ok"] is False


def test_get_automation_envelope_values_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_automation_envelope_values(0, 0, 0, 0)
    assert result["ok"] is False


def test_get_automation_envelope_values_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.get_automation_envelope_values(0, 0, 0, 0)
    assert result["ok"] is False
