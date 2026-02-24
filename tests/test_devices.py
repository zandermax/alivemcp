"""
Tests for DevicesMixin: device operations, parameters, racks/chains, plugin windows,
device utilities, and display values.
"""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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


def _song_with_device(device=None):
    dev = device or _make_device()
    track = MagicMock()
    track.devices = [dev]
    track.clip_slots = [MagicMock()]
    s = MagicMock()
    s.tracks = [track]
    s.scenes = [MagicMock()]
    return s


# ---------------------------------------------------------------------------
# add_device
# ---------------------------------------------------------------------------


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
    assert result["ok"] is True  # add_device has no len(tracks) call that would fail


# ---------------------------------------------------------------------------
# get_track_devices
# ---------------------------------------------------------------------------


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
    song.tracks[0].devices = None  # for dev in None → TypeError → ok=False
    result = tools.get_track_devices(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_device_param
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# set_device_on_off
# ---------------------------------------------------------------------------


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
    assert result["ok"] is True  # assignment doesn't raise on MagicMock


# ---------------------------------------------------------------------------
# get_device_parameters
# ---------------------------------------------------------------------------


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
    dev.parameters = None  # for param in None → TypeError → ok=False
    song.tracks[0].devices = [dev]
    result = tools.get_device_parameters(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_device_parameter_by_name
# ---------------------------------------------------------------------------


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
    dev.parameters = None  # for param in None → TypeError → ok=False
    song.tracks[0].devices = [dev]
    result = tools.get_device_parameter_by_name(0, 0, "x")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_device_parameter_by_name
# ---------------------------------------------------------------------------


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


def test_set_device_parameter_by_name_exception(tools, song):
    dev = _make_device()
    dev.parameters = None  # for param in None → TypeError → ok=False
    song.tracks[0].devices = [dev]
    result = tools.set_device_parameter_by_name(0, 0, "x", 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# delete_device
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# get_device_presets / set_device_preset
# ---------------------------------------------------------------------------


def test_get_device_presets_valid(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    result = tools.get_device_presets(0, 0)
    assert result["ok"] is True


def test_get_device_presets_invalid(tools):
    result = tools.get_device_presets(-1, 0)
    assert result["ok"] is False


def test_set_device_preset_valid(tools, song):
    dev = _make_device()
    song.tracks[0].devices = [dev]
    result = tools.set_device_preset(0, 0, 2)
    assert result["ok"] is True


def test_set_device_preset_invalid(tools):
    result = tools.set_device_preset(-1, 0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# randomize_device_parameters
# ---------------------------------------------------------------------------


def test_randomize_device_parameters_success(tools, song):
    param = _make_param(enabled=True, quantized=False, min_val=0.0, max_val=1.0)
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is True
    assert result["randomized_count"] == 1


def test_randomize_device_parameters_skips_quantized(tools, song):
    param_q = _make_param(enabled=True, quantized=True)
    dev = _make_device(params=[param_q])
    song.tracks[0].devices = [dev]
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is True
    assert result["randomized_count"] == 0


def test_randomize_device_parameters_invalid(tools):
    result = tools.randomize_device_parameters(-1, 0)
    assert result["ok"] is False


def test_randomize_device_parameters_exception(tools, song):
    dev = _make_device()
    dev.parameters = None  # for param in None → TypeError → ok=False
    song.tracks[0].devices = [dev]
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# randomize_device
# ---------------------------------------------------------------------------


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
    dev.parameters = None  # for param in None → TypeError → ok=False
    song.tracks[0].devices = [dev]
    result = tools.randomize_device(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_device_chains / get_chain_devices / set_chain_mute / set_chain_solo
# ---------------------------------------------------------------------------


def _make_chain(muted=False, solo=False):
    chain = MagicMock()
    chain.name = "Chain 1"
    chain.mute = muted
    chain.solo = solo
    chain.devices = [MagicMock()]
    return chain


def test_get_device_chains_with_chains(tools, song):
    chain = _make_chain()
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.get_device_chains(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_device_chains_no_chains_attr(tools, song):
    dev = _make_device()
    del dev.chains
    song.tracks[0].devices = [dev]
    result = tools.get_device_chains(0, 0)
    assert result["ok"] is False


def test_get_device_chains_invalid(tools):
    result = tools.get_device_chains(-1, 0)
    assert result["ok"] is False


def test_get_device_chains_exception(tools, song):
    dev = _make_device()
    dev.chains = None  # for chain in None → TypeError → ok=False
    song.tracks[0].devices = [dev]
    result = tools.get_device_chains(0, 0)
    assert result["ok"] is False


def test_get_chain_devices_success(tools, song):
    chain = _make_chain()
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.get_chain_devices(0, 0, 0)
    assert result["ok"] is True


def test_get_chain_devices_no_chains_attr(tools, song):
    dev = _make_device()
    del dev.chains
    song.tracks[0].devices = [dev]
    result = tools.get_chain_devices(0, 0, 0)
    assert result["ok"] is False


def test_get_chain_devices_invalid_chain(tools, song):
    chain = _make_chain()
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.get_chain_devices(0, 0, 99)
    assert result["ok"] is False


def test_get_chain_devices_invalid_track(tools):
    result = tools.get_chain_devices(-1, 0, 0)
    assert result["ok"] is False


def test_set_chain_mute_with_mute_attr(tools, song):
    chain = _make_chain()
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.set_chain_mute(0, 0, 0, True)
    assert result["ok"] is True


def test_set_chain_mute_without_mute_attr(tools, song):
    chain = _make_chain()
    del chain.mute
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.set_chain_mute(0, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_mute_no_chains(tools, song):
    dev = _make_device()
    del dev.chains
    song.tracks[0].devices = [dev]
    result = tools.set_chain_mute(0, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_mute_invalid(tools):
    result = tools.set_chain_mute(-1, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_solo_with_solo_attr(tools, song):
    chain = _make_chain()
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.set_chain_solo(0, 0, 0, True)
    assert result["ok"] is True


def test_set_chain_solo_without_solo_attr(tools, song):
    chain = _make_chain()
    del chain.solo
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.set_chain_solo(0, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_solo_invalid(tools):
    result = tools.set_chain_solo(-1, 0, 0, True)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# show_plugin_window / hide_plugin_window
# ---------------------------------------------------------------------------


def test_show_plugin_window_success(tools, song):
    result = tools.show_plugin_window(0, 0)
    assert result["ok"] is True


def test_show_plugin_window_exception(tools, song):
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.show_plugin_window(0, 0)
    assert result["ok"] is False


def test_hide_plugin_window_success(tools, song):
    result = tools.hide_plugin_window(0, 0)
    assert result["ok"] is True


# ---------------------------------------------------------------------------
# get_device_class_name / get_device_type
# ---------------------------------------------------------------------------


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
    song.tracks = None  # None[0] → TypeError → ok=False
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
    song.tracks = None  # None[0] → TypeError → ok=False
    result = tools.get_device_type(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_device_param_display_value / get_all_param_display_values
# ---------------------------------------------------------------------------


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
    dev.parameters = None  # None[0] → TypeError → ok=False
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
    dev.parameters = None  # for param in None → TypeError → ok=False
    song.tracks[0].devices = [dev]
    result = tools.get_all_param_display_values(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Additional coverage: invalid index branches and except blocks
# ---------------------------------------------------------------------------


def test_add_device_except_block(tools):
    tools.song = None
    result = tools.add_device(0, "EQ Eight")
    assert result["ok"] is False


def test_set_device_on_off_except_block(tools):
    tools.song = None
    result = tools.set_device_on_off(0, 0, True)
    assert result["ok"] is False


def test_set_device_parameter_by_name_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_parameter_by_name(0, 0, "x", 0)
    assert result["ok"] is False


def test_get_device_presets_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_device_presets(0, 0)
    assert result["ok"] is False


def test_get_device_presets_except_block(tools):
    tools.song = None
    result = tools.get_device_presets(0, 0)
    assert result["ok"] is False


def test_set_device_preset_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_device_preset(0, 0, 0)
    assert result["ok"] is False


def test_set_device_preset_except_block(tools):
    tools.song = None
    result = tools.set_device_preset(0, 0, 0)
    assert result["ok"] is False


def test_randomize_device_parameters_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.randomize_device_parameters(0, 0)
    assert result["ok"] is False


def test_randomize_device_inner_except_block(tools, song):
    """Cover lines 291-292: inner except pass when param.min is invalid."""
    param = _make_param(enabled=True, quantized=False)
    param.min = "bad"  # float("bad") → ValueError → inner except → pass
    dev = _make_device(params=[param])
    song.tracks[0].devices = [dev]
    result = tools.randomize_device(0, 0)
    assert result["ok"] is True
    assert result["randomized_parameters"] == 0


def test_get_device_chains_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_device_chains(0, 0)
    assert result["ok"] is False


def test_get_chain_devices_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.get_chain_devices(0, 0, 0)
    assert result["ok"] is False


def test_get_chain_devices_except_block(tools):
    tools.song = None
    result = tools.get_chain_devices(0, 0, 0)
    assert result["ok"] is False


def test_set_chain_mute_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_chain_mute(0, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_mute_invalid_chain(tools, song):
    chain = _make_chain()
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.set_chain_mute(0, 0, 99, True)
    assert result["ok"] is False


def test_set_chain_mute_except_block(tools):
    tools.song = None
    result = tools.set_chain_mute(0, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_solo_invalid_device(tools, song):
    song.tracks[0].devices = []
    result = tools.set_chain_solo(0, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_solo_no_chains(tools, song):
    dev = _make_device()
    del dev.chains
    song.tracks[0].devices = [dev]
    result = tools.set_chain_solo(0, 0, 0, True)
    assert result["ok"] is False


def test_set_chain_solo_invalid_chain(tools, song):
    chain = _make_chain()
    dev = _make_device(chains=[chain])
    song.tracks[0].devices = [dev]
    result = tools.set_chain_solo(0, 0, 99, True)
    assert result["ok"] is False


def test_set_chain_solo_except_block(tools):
    tools.song = None
    result = tools.set_chain_solo(0, 0, 0, True)
    assert result["ok"] is False
