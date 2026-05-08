"""
Tests for MixingMasterDevicesMixin — master track device parameter tools.
"""

from unittest.mock import MagicMock


def _make_param(name="Gain", value=0.5, min_=0.0, max_=1.0, is_quantized=False):
    param = MagicMock()
    param.name = name
    param.value = value
    param.min = min_
    param.max = max_
    param.is_quantized = is_quantized
    param.display_value = str(value)
    param.value_items = []
    return param


def _make_device(name="Utility", params=None):
    device = MagicMock()
    device.name = name
    device.class_name = "PluginDevice"
    device.is_active = True
    device.parameters = params or [_make_param()]
    return device


# ---------------------------------------------------------------------------
# get_master_device_params
# ---------------------------------------------------------------------------


def test_get_master_device_params_success(tools, song):
    song.master_track.devices = [_make_device()]
    result = tools.get_master_device_params(0)
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["parameters"][0]["name"] == "Gain"


def test_get_master_device_params_invalid_index(tools, song):
    song.master_track.devices = [_make_device()]
    result = tools.get_master_device_params(5)
    assert result["ok"] is False
    assert "Invalid device index" in result["error"]


def test_get_master_device_params_negative_index(tools, song):
    song.master_track.devices = [_make_device()]
    result = tools.get_master_device_params(-1)
    assert result["ok"] is False


def test_get_master_device_params_exception(tools, song):
    song.master_track = None
    result = tools.get_master_device_params(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_master_device_param
# ---------------------------------------------------------------------------


def test_set_master_device_param_success(tools, song):
    param = _make_param(value=0.0, min_=0.0, max_=1.0)
    song.master_track.devices = [_make_device(params=[param])]
    result = tools.set_master_device_param(0, 0, 0.8)
    assert result["ok"] is True
    assert param.value == 0.8


def test_set_master_device_param_clamped(tools, song):
    param = _make_param(value=0.0, min_=0.0, max_=1.0)
    song.master_track.devices = [_make_device(params=[param])]
    tools.set_master_device_param(0, 0, 2.5)
    assert param.value == 1.0


def test_set_master_device_param_invalid_device(tools, song):
    song.master_track.devices = [_make_device()]
    result = tools.set_master_device_param(99, 0, 0.5)
    assert result["ok"] is False
    assert "Invalid device index" in result["error"]


def test_set_master_device_param_invalid_param(tools, song):
    song.master_track.devices = [_make_device(params=[_make_param()])]
    result = tools.set_master_device_param(0, 99, 0.5)
    assert result["ok"] is False
    assert "Invalid parameter index" in result["error"]


def test_set_master_device_param_exception(tools, song):
    song.master_track = None
    result = tools.set_master_device_param(0, 0, 0.5)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_master_device_param_by_name
# ---------------------------------------------------------------------------


def test_set_master_device_param_by_name_success(tools, song):
    param = _make_param(name="Volume", value=0.0, min_=0.0, max_=1.0)
    song.master_track.devices = [_make_device(params=[param])]
    result = tools.set_master_device_param_by_name(0, "Volume", 0.75)
    assert result["ok"] is True
    assert param.value == 0.75


def test_set_master_device_param_by_name_not_found(tools, song):
    song.master_track.devices = [_make_device(params=[_make_param(name="Gain")])]
    result = tools.set_master_device_param_by_name(0, "NonExistent", 0.5)
    assert result["ok"] is False
    assert "not found" in result["error"]


def test_set_master_device_param_by_name_quantized_string(tools, song):
    param = _make_param(name="Mode", is_quantized=True)
    param.value_items = ["Off", "On"]
    song.master_track.devices = [_make_device(params=[param])]
    result = tools.set_master_device_param_by_name(0, "Mode", "On")
    assert result["ok"] is True
    assert param.value == 1.0


def test_set_master_device_param_by_name_quantized_not_in_items(tools, song):
    param = _make_param(name="Mode", is_quantized=True)
    param.value_items = ["Off", "On"]
    song.master_track.devices = [_make_device(params=[param])]
    result = tools.set_master_device_param_by_name(0, "Mode", "Maybe")
    assert result["ok"] is False


def test_set_master_device_param_by_name_invalid_device(tools, song):
    song.master_track.devices = []
    result = tools.set_master_device_param_by_name(0, "Gain", 0.5)
    assert result["ok"] is False


def test_set_master_device_param_by_name_exception(tools, song):
    song.master_track = None
    result = tools.set_master_device_param_by_name(0, "Gain", 0.5)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_master_device_param_info
# ---------------------------------------------------------------------------


def test_get_master_device_param_info_success(tools, song):
    param = _make_param(name="Gain", value=0.5)
    song.master_track.devices = [_make_device(params=[param])]
    result = tools.get_master_device_param_info(0, "Gain")
    assert result["ok"] is True
    assert result["name"] == "Gain"
    assert result["raw_value"] == 0.5
    assert "display_value" in result
    assert "min" in result
    assert "max" in result


def test_get_master_device_param_info_not_found(tools, song):
    song.master_track.devices = [_make_device(params=[_make_param(name="Gain")])]
    result = tools.get_master_device_param_info(0, "Missing")
    assert result["ok"] is False
    assert "not found" in result["error"]


def test_get_master_device_param_info_invalid_device(tools, song):
    song.master_track.devices = []
    result = tools.get_master_device_param_info(0, "Gain")
    assert result["ok"] is False


def test_get_master_device_param_info_exception(tools, song):
    song.master_track = None
    result = tools.get_master_device_param_info(0, "Gain")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_master_chain_summary
# ---------------------------------------------------------------------------


def test_get_master_chain_summary_success(tools, song):
    song.master_track.devices = [_make_device("EQ Eight", [_make_param("LowGain")])]
    result = tools.get_master_chain_summary()
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["devices"][0]["name"] == "EQ Eight"
    assert result["devices"][0]["parameters"][0]["name"] == "LowGain"


def test_get_master_chain_summary_empty(tools, song):
    song.master_track.devices = []
    result = tools.get_master_chain_summary()
    assert result["ok"] is True
    assert result["count"] == 0
    assert result["devices"] == []


def test_get_master_chain_summary_exception(tools, song):
    song.master_track = None
    result = tools.get_master_chain_summary()
    assert result["ok"] is False
