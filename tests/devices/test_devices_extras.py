"""
Tests for DevicesMixin extras: randomization, plugin windows, metadata, display values.
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


def test_randomize_device_parameters_success(tools, song):
    param = _make_param(enabled=True, quantized=False, min_val=0.0, max_val=1.0)
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is True
    assert result["randomized_parameters"] == 1


def test_randomize_device_parameters_skips_quantized(tools, song):
    param_q = _make_param(enabled=True, quantized=True)
    dev = _make_device(params=[param_q])
    song.tracks[0].devices = [dev]
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is True
    assert result["randomized_parameters"] == 0


def test_randomize_device_parameters_invalid(tools):
    result = tools.randomize_device_parameters(-1, 0)
    assert result["ok"] is False


def test_randomize_device_parameters_exception(tools, song):
    dev = _make_device()
    dev.parameters = None
    song.tracks[0].devices = [dev]
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is False


def test_randomize_device_success(tools, song):
    param = _make_param(enabled=True, quantized=False, min_val=0.0, max_val=1.0)
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.randomize_device(0, 0)
    assert result["ok"] is True


def test_randomize_device_invalid(tools):
    result = tools.randomize_device(-1, 0)
    assert result["ok"] is False


def test_randomize_device_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.randomize_device(0, 0)
    assert result["ok"] is False


def test_randomize_device_exception(tools, song):
    dev = _make_device()
    dev.parameters = None
    song.tracks[0].devices = [dev]
    result = tools.randomize_device(0, 0)
    assert result["ok"] is False


def test_show_plugin_window_success(tools, song):
    result = tools.show_plugin_window(0, 0)
    assert result["ok"] is True


def test_show_plugin_window_exception(tools, song):
    song.tracks = None
    result = tools.show_plugin_window(0, 0)
    assert result["ok"] is False


def test_hide_plugin_window_success(tools, song):
    result = tools.hide_plugin_window(0, 0)
    assert result["ok"] is True


def test_get_device_class_name_with_attr(tools, song):
    dev = _make_device(class_name="Compressor2")
    song.tracks[0].devices = [dev]
    result = tools.get_device_class_name(0, 0)
    assert result["ok"] is True
    assert result["class_name"] == "Compressor2"


def test_get_device_class_name_without_attr(tools, song):
    dev = _make_device()
    del dev.class_name
    song.tracks[0].devices = [dev]
    result = tools.get_device_class_name(0, 0)
    assert result["ok"] is False


def test_get_device_class_name_exception(tools, song):
    song.tracks = None
    result = tools.get_device_class_name(0, 0)
    assert result["ok"] is False


def test_get_device_type_with_attr(tools, song):
    dev = _make_device()
    dev.type = 1
    song.tracks[0].devices = [dev]
    result = tools.get_device_type(0, 0)
    assert result["ok"] is True
    assert result["type"] == 1


def test_get_device_type_without_attr(tools, song):
    dev = _make_device()
    del dev.type
    song.tracks[0].devices = [dev]
    result = tools.get_device_type(0, 0)
    assert result["ok"] is False


def test_get_device_type_exception(tools, song):
    song.tracks = None
    result = tools.get_device_type(0, 0)
    assert result["ok"] is False


def test_get_device_param_display_value_with_display_value(tools, song):
    param = _make_param()
    param.display_value = "0.5 dB"
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.get_device_param_display_value(0, 0, 0)
    assert result["ok"] is True
    assert result["display_value"] == "0.5 dB"


def test_get_device_param_display_value_without_display_value(tools, song):
    param = _make_param()
    del param.display_value
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.get_device_param_display_value(0, 0, 0)
    assert result["ok"] is True


def test_get_device_param_display_value_exception(tools, song):
    dev = _make_device()
    dev.parameters = None
    song.tracks[0].devices = [dev]
    result = tools.get_device_param_display_value(0, 0, 0)
    assert result["ok"] is False


def test_get_all_param_display_values_with_display_value(tools, song):
    param = _make_param()
    param.display_value = "1.0 kHz"
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.get_all_param_display_values(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["parameters"][0]["display_value"] == "1.0 kHz"


def test_get_all_param_display_values_without_display_value(tools, song):
    param = _make_param()
    del param.display_value
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.get_all_param_display_values(0, 0)
    assert result["ok"] is True


def test_get_all_param_display_values_exception(tools, song):
    dev = _make_device()
    dev.parameters = None
    song.tracks[0].devices = [dev]
    result = tools.get_all_param_display_values(0, 0)
    assert result["ok"] is False


def test_set_device_on_off_except_block(tools):
    tools.song = None
    result = tools.set_device_on_off(0, 0, True)
    assert result["ok"] is False


def test_randomize_device_parameters_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is False


def test_randomize_device_inner_except_block(tools, song):
    param = _make_param(enabled=True, quantized=False)
    param.min = "bad"
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.randomize_device(0, 0)
    assert result["ok"] is True
    assert result["randomized_parameters"] == 0


def test_get_device_presets_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_device_presets(0, 0)
    assert result["ok"] is False


def test_get_device_presets_valid(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    result = tools.get_device_presets(0, 0)
    assert result["ok"] is True


def test_get_device_presets_invalid(tools):
    result = tools.get_device_presets(-1, 0)
    assert result["ok"] is False


def test_get_device_presets_except_block(tools):
    tools.song = None
    result = tools.get_device_presets(0, 0)
    assert result["ok"] is False


def test_set_device_preset_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_preset(0, 0, 0)
    assert result["ok"] is False


def test_set_device_preset_valid(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    result = tools.set_device_preset(0, 0, 2)
    assert result["ok"] is True


def test_set_device_preset_invalid(tools):
    result = tools.set_device_preset(-1, 0, 0)
    assert result["ok"] is False


def test_set_device_preset_except_block(tools):
    tools.song = None
    result = tools.set_device_preset(0, 0, 0)
    assert result["ok"] is False


def test_add_device_except_block(tools):
    tools.song = None
    result = tools.add_device(0, "EQ Eight")
    assert result["ok"] is False
