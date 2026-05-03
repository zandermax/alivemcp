"""Tests for get_track_chain_summary."""

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


def test_get_track_chain_summary_single_device(tools, song):
    """Test get_track_chain_summary with single device."""
    param1 = make_param("Volume", 0.5, 0.0, 1.0)
    param2 = make_param("Pan", 0.0, -1.0, 1.0)
    device = make_device("Utility", "Utility", [param1, param2])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.get_track_chain_summary(0)

    assert result["ok"]
    assert result["track_index"] == 0
    assert result["count"] == 1
    assert len(result["devices"]) == 1
    assert result["devices"][0]["name"] == "Utility"
    assert result["devices"][0]["index"] == 0
    assert len(result["devices"][0]["parameters"]) == 2


def test_get_track_chain_summary_multiple_devices(tools, song):
    """Test get_track_chain_summary with multiple devices."""
    device1 = make_device("EQ", "AudioEq", [make_param("Volume", 0.5)])
    device2 = make_device("Compressor", "Compressor", [make_param("Ratio", 4.0)])

    track = MagicMock()
    track.name = "Master"
    track.devices = [device1, device2]
    track.clip_slots = [MagicMock()]

    local_song = MagicMock()
    local_song.tracks = [track]
    local_song.scenes = [MagicMock()]
    tools.song = local_song

    result = tools.get_track_chain_summary(0)

    assert result["ok"]
    assert result["count"] == 2
    assert result["devices"][0]["name"] == "EQ"
    assert result["devices"][1]["name"] == "Compressor"


def test_get_track_chain_summary_enriched_data(tools, song):
    """Test that chain summary includes enriched parameter data."""
    param = make_param("Mode", 0.0, 0.0, 2.0, quantized=True, value_items=["Off", "On"])
    param.display_value = "Off"
    device = make_device("Device", "Device", [param])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.get_track_chain_summary(0)

    assert result["ok"]
    param_info = result["devices"][0]["parameters"][0]
    assert param_info["is_quantized"]
    assert param_info["value_items"] == ["Off", "On"]
    assert param_info["display_value"] == "Off"


def test_get_track_chain_summary_includes_device_class(tools, song):
    """Test that chain summary includes device class_name."""
    device = make_device("MyDevice", "CustomClass", [make_param()])
    song = song_with_track_device(0, device)
    tools.song = song

    result = tools.get_track_chain_summary(0)

    assert result["ok"]
    assert result["devices"][0]["class_name"] == "CustomClass"
    assert result["devices"][0]["is_active"]


def test_get_track_chain_summary_includes_track_name(tools, song):
    """Test that chain summary includes track name."""
    device = make_device("Device", "Class", [make_param()])
    track = MagicMock()
    track.name = "Mastering Chain"
    track.devices = [device]
    track.clip_slots = [MagicMock()]

    local_song = MagicMock()
    local_song.tracks = [track]
    local_song.scenes = [MagicMock()]
    tools.song = local_song

    result = tools.get_track_chain_summary(0)

    assert result["ok"]
    assert result["track_name"] == "Mastering Chain"


def test_get_track_chain_summary_invalid_track_index(tools, song):
    """Test invalid track index returns error."""
    result = tools.get_track_chain_summary(999)
    assert not result["ok"]
    assert "Invalid track index" in result["error"]


def test_get_track_chain_summary_empty_chain(tools, song):
    """Test chain summary with no devices."""
    track = MagicMock()
    track.name = "Empty"
    track.devices = []
    track.clip_slots = [MagicMock()]

    local_song = MagicMock()
    local_song.tracks = [track]
    local_song.scenes = [MagicMock()]
    tools.song = local_song

    result = tools.get_track_chain_summary(0)

    assert result["ok"]
    assert result["count"] == 0
    assert result["devices"] == []
