"""Tests for M4L device detection and parameter control."""

from unittest.mock import MagicMock


def _m4l_device(class_name="MxDeviceAudioEffect", name="CV Shaper"):
    dev = MagicMock()
    dev.class_name = class_name
    dev.name = name
    dev.is_active = True
    dev.parameters = [MagicMock()]
    return dev


# ---------------------------------------------------------------------------
# is_max_device
# ---------------------------------------------------------------------------


def test_is_max_device_true(tools, song):
    dev = _m4l_device(class_name="MxDeviceAudioEffect")
    song.tracks[0].devices = [dev]
    result = tools.is_max_device(0, 0)
    assert result["ok"] is True
    assert result["is_m4l"] is True


def test_is_max_device_false(tools, song):
    dev = _m4l_device(class_name="Compressor2")
    song.tracks[0].devices = [dev]
    result = tools.is_max_device(0, 0)
    assert result["ok"] is True
    assert result["is_m4l"] is False


def test_is_max_device_invalid_track(tools):
    result = tools.is_max_device(-1, 0)
    assert result["ok"] is False


def test_is_max_device_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.is_max_device(0, 0)
    assert result["ok"] is False


def test_is_max_device_exception(tools, song):
    song.tracks[0].devices = MagicMock(side_effect=Exception("err"))
    result = tools.is_max_device(0, 0)
    assert result["ok"] is False


def test_is_max_device_except_block(tools):
    tools.song = None
    result = tools.is_max_device(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_m4l_devices
# ---------------------------------------------------------------------------


def test_get_m4l_devices_with_m4l(tools, song):
    dev = _m4l_device(class_name="MxDeviceAudioEffect", name="CV Shaper")
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_devices(0)
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["devices"][0]["type"] == "audio_effect"


def test_get_m4l_devices_no_m4l(tools, song):
    dev = _m4l_device(class_name="Sampler", name="Sampler")
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_devices(0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_m4l_devices_invalid(tools):
    result = tools.get_m4l_devices(-1)
    assert result["ok"] is False


def test_get_m4l_devices_exception(tools, song):
    song.tracks[0].devices = None
    result = tools.get_m4l_devices(0)
    assert result["ok"] is False


def test_get_m4l_type_variants(tools, song):
    """Cover all three M4L class names via get_m4l_devices."""
    for class_name, expected_type in [
        ("MxDeviceAudioEffect", "audio_effect"),
        ("MxDeviceMidiEffect", "midi_effect"),
        ("MxDeviceInstrument", "instrument"),
    ]:
        dev = _m4l_device(class_name=class_name)
        song.tracks[0].devices = [dev]
        result = tools.get_m4l_devices(0)
        assert result["devices"][0]["type"] == expected_type


# ---------------------------------------------------------------------------
# set_device_param_by_name
# ---------------------------------------------------------------------------


def test_set_device_param_by_name_found(tools, song):
    param = MagicMock()
    param.name = "Threshold"
    param.min = 0.0
    param.max = 1.0
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.set_device_param_by_name(0, 0, "Threshold", 0.5)
    assert result["ok"] is True
    assert param.value == 0.5


def test_set_device_param_by_name_not_found(tools, song):
    param = MagicMock()
    param.name = "Gain"
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.set_device_param_by_name(0, 0, "Missing", 0.5)
    assert result["ok"] is False
    assert "not found" in result["error"]


def test_set_device_param_by_name_invalid_track(tools):
    result = tools.set_device_param_by_name(-1, 0, "x", 0)
    assert result["ok"] is False


def test_set_device_param_by_name_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_param_by_name(0, 0, "x", 0)
    assert result["ok"] is False


def test_set_device_param_by_name_exception(tools, song):
    dev = MagicMock()
    dev.parameters = MagicMock(side_effect=Exception("err"))
    song.tracks[0].devices = [dev]
    result = tools.set_device_param_by_name(0, 0, "x", 0)
    assert result["ok"] is False


def test_set_device_param_by_name_except_block(tools):
    tools.song = None
    result = tools.set_device_param_by_name(0, 0, "x", 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_m4l_param_by_name
# ---------------------------------------------------------------------------


def test_get_m4l_param_by_name_found(tools, song):
    param = MagicMock()
    param.name = "Cutoff"
    param.value = 0.7
    param.min = 0.0
    param.max = 1.0
    param.is_enabled = True
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "Cutoff")
    assert result["ok"] is True
    assert result["value"] == 0.7


def test_get_m4l_param_by_name_not_found(tools, song):
    param = MagicMock()
    param.name = "Gain"
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "Missing")
    assert result["ok"] is False


def test_get_m4l_param_by_name_invalid(tools):
    result = tools.get_m4l_param_by_name(-1, 0, "x")
    assert result["ok"] is False


def test_get_m4l_param_by_name_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_m4l_param_by_name(0, 0, "x")
    assert result["ok"] is False


def test_get_m4l_param_by_name_no_is_enabled(tools, song):
    param = MagicMock()
    param.name = "P"
    param.value = 0.5
    param.min = 0.0
    param.max = 1.0
    del param.is_enabled
    dev = MagicMock()
    dev.parameters = [param]
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "P")
    assert result["ok"] is True
    assert result["is_enabled"] is True


def test_get_m4l_param_by_name_exception(tools, song):
    dev = MagicMock()
    dev.parameters = MagicMock(side_effect=Exception("err"))
    song.tracks[0].devices = [dev]
    result = tools.get_m4l_param_by_name(0, 0, "x")
    assert result["ok"] is False


def test_get_m4l_param_by_name_except_block(tools):
    tools.song = None
    result = tools.get_m4l_param_by_name(0, 0, "x")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_cv_tools_devices
# ---------------------------------------------------------------------------


def test_get_cv_tools_devices_found(tools, song):
    dev = MagicMock()
    dev.name = "CV Shaper"
    dev.class_name = "MxDeviceAudioEffect"
    dev.is_active = True
    dev.parameters = [MagicMock()]
    song.tracks[0].devices = [dev]
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_cv_tools_devices_lowercase_cv(tools, song):
    dev = MagicMock()
    dev.name = "cv_clock"
    dev.class_name = "MxDeviceAudioEffect"
    dev.is_active = True
    dev.parameters = [MagicMock()]
    song.tracks[0].devices = [dev]
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_cv_tools_devices_no_cv(tools, song):
    dev = MagicMock()
    dev.name = "EQ Eight"
    dev.class_name = "EQ"
    dev.is_active = True
    dev.parameters = []
    song.tracks[0].devices = [dev]
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_cv_tools_devices_invalid(tools):
    result = tools.get_cv_tools_devices(-1)
    assert result["ok"] is False


def test_get_cv_tools_devices_except_block(tools):
    tools.song = None
    result = tools.get_cv_tools_devices(0)
    assert result["ok"] is False
