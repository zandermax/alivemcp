"""Tests for get_track_device_params and set_track_device_param."""

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


def test_get_track_device_params_success(tools, song):
    """Test get_track_device_params returns enriched parameter data."""
    param1 = make_param("Volume", 0.5, 0.0, 1.0)
    param2 = make_param("Decay", 100.0, 10.0, 500.0)
    device = make_device("Synth", "Sampler", [param1, param2])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.get_track_device_params(0, 0)

    assert result["ok"]
    assert result["device_name"] == "Synth"
    assert result["count"] == 2
    assert len(result["parameters"]) == 2
    assert result["parameters"][0]["name"] == "Volume"
    assert result["parameters"][0]["raw_value"] == 0.5
    assert result["parameters"][1]["name"] == "Decay"


def test_get_track_device_params_with_display_value(tools, song):
    """Test that display_value is included in response."""
    param = make_param("Cutoff", 100.0)
    param.display_value = "100 Hz"
    device = make_device("Filter", "Compressor", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.get_track_device_params(0, 0)

    assert result["ok"]
    assert result["parameters"][0]["display_value"] == "100 Hz"


def test_get_track_device_params_with_quantized(tools, song):
    """Test quantized parameter handling."""
    param = make_param("Mode", 0.0, 0.0, 2.0, quantized=True, value_items=["Off", "On", "Auto"])
    device = make_device("Envelope", "Compressor", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.get_track_device_params(0, 0)

    assert result["ok"]
    assert result["parameters"][0]["is_quantized"]
    assert result["parameters"][0]["value_items"] == ["Off", "On", "Auto"]


def test_get_track_device_params_invalid_track_index(tools, song):
    """Test invalid track index returns error."""
    result = tools.get_track_device_params(999, 0)
    assert not result["ok"]
    assert "Invalid track index" in result["error"]


def test_get_track_device_params_invalid_device_index(tools, song):
    """Test invalid device index returns error."""
    result = tools.get_track_device_params(0, 999)
    assert not result["ok"]
    assert "Invalid device index" in result["error"]


def test_set_track_device_param_success(tools, song):
    """Test set_track_device_param sets value correctly."""
    param = make_param("Volume", 0.5, 0.0, 1.0)
    device = make_device("Compressor", "Compressor", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.set_track_device_param(0, 0, 0, 0.75)

    assert result["ok"]
    assert result["track_index"] == 0
    assert result["device_name"] == "Compressor"
    assert result["param_name"] == "Volume"
    assert param.value == 0.75


def test_set_track_device_param_clamped_to_max(tools, song):
    """Test value is clamped to max."""
    param = make_param("Volume", 0.5, 0.0, 1.0)
    device = make_device("Compressor", "Compressor", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.set_track_device_param(0, 0, 0, 2.0)

    assert result["ok"]
    assert param.value == 1.0


def test_set_track_device_param_clamped_to_min(tools, song):
    """Test value is clamped to min."""
    param = make_param("Volume", 0.5, 0.0, 1.0)
    device = make_device("Compressor", "Compressor", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.set_track_device_param(0, 0, 0, -0.5)

    assert result["ok"]
    assert param.value == 0.0


def test_set_track_device_param_invalid_track_index(tools, song):
    """Test invalid track index returns error."""
    result = tools.set_track_device_param(999, 0, 0, 0.5)
    assert not result["ok"]
    assert "Invalid track index" in result["error"]


def test_set_track_device_param_invalid_device_index(tools, song):
    """Test invalid device index returns error."""
    result = tools.set_track_device_param(0, 999, 0, 0.5)
    assert not result["ok"]
    assert "Invalid device index" in result["error"]


def test_set_track_device_param_invalid_param_index(tools, song):
    """Test invalid param index returns error."""
    result = tools.set_track_device_param(0, 0, 999, 0.5)
    assert not result["ok"]
    assert "Invalid parameter index" in result["error"]
