"""
Tests for DevicesMixin core device operations and parameters.
"""

from unittest.mock import MagicMock


def _make_param(name="Volume", value=0.5, min_val=0.0, max_val=1.0, enabled=True, quantized=False):
    p = MagicMock()
    p.name = name
    p.value = value
    p.min = min_val
    p.max = max_val
    p.is_enabled = enabled
    p.is_quantized = quantized
    return p


def _make_device(name="EQ", class_name="AudioEq", params=None, chains=None):
    d = MagicMock()
    d.name = name
    d.class_name = class_name
    d.is_active = True
    d.parameters = params if params is not None else [_make_param()]
    if chains is not None:
        d.chains = chains
    return d


def test_add_device_valid(tools, song):
    result = tools.add_device(0, "EQ Eight")
    assert result["ok"] is True
    assert result["device_name"] == "EQ Eight"


def test_add_device_invalid_track(tools):
    result = tools.add_device(-1, "EQ Eight")
    assert result["ok"] is False


def test_add_device_exception(tools, song):
    song.tracks[0].devices = MagicMock(side_effect=Exception("err"))
    result = tools.add_device(0, "EQ Eight")
    assert result["ok"] is True


def test_get_track_devices_success(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    result = tools.get_track_devices(0)
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["devices"][0]["name"] == "EQ"


def test_get_track_devices_invalid(tools):
    result = tools.get_track_devices(-1)
    assert result["ok"] is False


def test_get_track_devices_exception(tools, song):
    song.tracks[0].devices = None
    result = tools.get_track_devices(0)
    assert result["ok"] is False


def test_set_device_param_valid(tools, song):
    param = _make_param()
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.set_device_param(0, 0, 0, 0.8)
    assert result["ok"] is True
    assert param.value == 0.8


def test_set_device_param_invalid_track(tools):
    result = tools.set_device_param(-1, 0, 0, 0.5)
    assert result["ok"] is False


def test_set_device_param_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_param(0, 0, 0, 0.5)
    assert result["ok"] is False


def test_set_device_param_invalid_param(tools, song):
    dev = _make_device(params=[])
    song.tracks[0].devices = [dev]
    result = tools.set_device_param(0, 0, 0, 0.5)
    assert result["ok"] is False


def test_set_device_param_exception(tools, song):
    param = _make_param()
    param.value = property(lambda s: (_ for _ in ()).throw(Exception("err")))
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.set_device_param(0, 0, 0, "bad")
    assert result["ok"] is False


def test_set_device_on_off_valid(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    result = tools.set_device_on_off(0, 0, True)
    assert result["ok"] is True


def test_set_device_on_off_no_is_active(tools, song):
    dev = _make_device()
    del dev.is_active
    song.tracks[0].devices = [dev]
    result = tools.set_device_on_off(0, 0, True)
    assert result["ok"] is False


def test_set_device_on_off_invalid_track(tools):
    result = tools.set_device_on_off(-1, 0, True)
    assert result["ok"] is False


def test_set_device_on_off_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_on_off(0, 0, True)
    assert result["ok"] is False


def test_set_device_on_off_exception(tools, song):
    dev = _make_device()
    dev.is_active = MagicMock(side_effect=Exception("err"))
    song.tracks[0].devices = [dev]
    result = tools.set_device_on_off(0, 0, True)
    assert result["ok"] is True


def test_get_device_parameters_success(tools, song):
    param = _make_param()
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.get_device_parameters(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["parameters"][0]["name"] == "Volume"


def test_get_device_parameters_invalid_track(tools):
    result = tools.get_device_parameters(-1, 0)
    assert result["ok"] is False


def test_get_device_parameters_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_device_parameters(0, 0)
    assert result["ok"] is False


def test_get_device_parameters_exception(tools, song):
    dev = _make_device()
    dev.parameters = None
    song.tracks[0].devices = [dev]
    result = tools.get_device_parameters(0, 0)
    assert result["ok"] is False


def test_get_device_parameter_by_name_found(tools, song):
    param = _make_param(name="Freq")
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.get_device_parameter_by_name(0, 0, "Freq")
    assert result["ok"] is True
    assert result["name"] == "Freq"


def test_get_device_parameter_by_name_not_found(tools, song):
    param = _make_param(name="Gain")
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.get_device_parameter_by_name(0, 0, "Unknown")
    assert result["ok"] is False
    assert "not found" in result["error"]


def test_get_device_parameter_by_name_invalid_track(tools):
    result = tools.get_device_parameter_by_name(-1, 0, "x")
    assert result["ok"] is False


def test_get_device_parameter_by_name_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_device_parameter_by_name(0, 0, "x")
    assert result["ok"] is False


def test_get_device_parameter_by_name_exception(tools, song):
    dev = _make_device()
    dev.parameters = None
    song.tracks[0].devices = [dev]
    result = tools.get_device_parameter_by_name(0, 0, "x")
    assert result["ok"] is False


def test_set_device_parameter_by_name_found(tools, song):
    param = _make_param(name="Resonance")
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.set_device_parameter_by_name(0, 0, "Resonance", 0.7)
    assert result["ok"] is True
    assert param.value == 0.7


def test_set_device_parameter_by_name_not_found(tools, song):
    param = _make_param(name="Gain")
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.set_device_parameter_by_name(0, 0, "Missing", 0.5)
    assert result["ok"] is False


def test_set_device_parameter_by_name_invalid(tools):
    result = tools.set_device_parameter_by_name(-1, 0, "x", 0)
    assert result["ok"] is False


def test_set_device_parameter_by_name_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_parameter_by_name(0, 0, "x", 0)
    assert result["ok"] is False


def test_set_device_parameter_by_name_exception(tools, song):
    dev = _make_device()
    dev.parameters = None
    song.tracks[0].devices = [dev]
    result = tools.set_device_parameter_by_name(0, 0, "x", 0)
    assert result["ok"] is False


def test_delete_device_valid(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    result = tools.delete_device(0, 0)
    assert result["ok"] is True
    song.tracks[0].delete_device.assert_called_once_with(0)


def test_delete_device_invalid_track(tools):
    result = tools.delete_device(-1, 0)
    assert result["ok"] is False


def test_delete_device_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.delete_device(0, 0)
    assert result["ok"] is False


def test_delete_device_exception(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    song.tracks[0].delete_device.side_effect = Exception("err")
    result = tools.delete_device(0, 0)
    assert result["ok"] is False
