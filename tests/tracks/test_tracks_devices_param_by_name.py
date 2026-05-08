"""Tests for set_track_device_param_by_name."""

from unittest.mock import MagicMock


def make_param(
    name="Volume", value=0.5, min_val=0.0, max_val=1.0, quantized=False, value_items=None
):
    """Create a mock parameter with enriched data."""
    param = MagicMock()
    param.name = name
    param.value = value
    param.min = min_val
    param.max = max_val
    param.is_quantized = quantized
    param.display_value = str(value)
    if value_items is not None:
        param.value_items = value_items
    return param


def make_device(name="EQ", class_name="AudioEq", params=None):
    """Create a mock device."""
    device = MagicMock()
    device.name = name
    device.class_name = class_name
    device.is_active = True
    device.parameters = params if params is not None else [make_param()]
    return device


def song_with_track_device(track_idx=0, device=None):
    """Create a song with one track containing a single device."""
    track_device = device or make_device()
    track = MagicMock()
    track.name = "Track " + str(track_idx)
    track.devices = [track_device]
    track.clip_slots = [MagicMock()]

    song = MagicMock()
    song.tracks = [track]
    song.scenes = [MagicMock()]
    return song


def test_set_track_device_param_by_name_continuous(tools, song):
    """Test set_track_device_param_by_name with continuous parameter."""
    param = make_param("Volume", 0.5, 0.0, 1.0)
    device = make_device("Synth", "Synth", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.set_track_device_param_by_name(0, 0, "Volume", 0.75)

    assert result["ok"]
    assert result["device_name"] == "Synth"
    assert result["param_name"] == "Volume"
    assert param.value == 0.75


def test_set_track_device_param_by_name_quantized(tools, song):
    """Test set_track_device_param_by_name with quantized parameter."""
    param = make_param(
        "Mode", 0.0, 0.0, 2.0, quantized=True, value_items=["Legato", "Portamento", "Glide"]
    )
    param.display_value = "Legato"
    device = make_device("Envelope", "Envelope", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.set_track_device_param_by_name(0, 0, "Mode", "Portamento")

    assert result["ok"]
    assert param.value == 1.0


def test_set_track_device_param_by_name_display_value(tools, song):
    """Test display_value is returned after setting."""
    param = make_param("Cutoff", 100.0)
    param.display_value = "100 Hz"
    device = make_device("Filter", "Filter", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.set_track_device_param_by_name(0, 0, "Cutoff", 500.0)

    assert result["ok"]
    assert "display_value" in result


def test_set_track_device_param_by_name_not_found(tools, song):
    """Test error when parameter not found."""
    result = tools.set_track_device_param_by_name(0, 0, "NonExistent", 0.5)
    assert not result["ok"]
    assert "not found" in result["error"].lower()


def test_set_track_device_param_by_name_invalid_quantized_value(tools, song):
    """Test error when quantized value not in items."""
    param = make_param("Mode", 0.0, 0.0, 2.0, quantized=True, value_items=["A", "B"])
    device = make_device("Device", "Device", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.set_track_device_param_by_name(0, 0, "Mode", "Invalid")

    assert not result["ok"]
    assert "not in value_items" in result["error"]


def test_set_track_device_param_by_name_invalid_track_index(tools, song):
    """Test invalid track index returns error."""
    result = tools.set_track_device_param_by_name(999, 0, "Volume", 0.5)
    assert not result["ok"]
    assert "Invalid track index" in result["error"]


def test_set_track_device_param_by_name_invalid_device_index(tools, song):
    """Test invalid device index returns error."""
    result = tools.set_track_device_param_by_name(0, 999, "Volume", 0.5)
    assert not result["ok"]
    assert "Invalid device index" in result["error"]
