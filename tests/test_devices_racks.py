"""
Tests for DevicesMixin rack and chain operations.
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
    dev.chains = None
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


def test_get_rack_contents_success_with_enriched_params(tools, song):
    param_cont = _make_param(name="Gain", value=0.25, min_val=0.0, max_val=1.0, quantized=False)
    param_cont.value_items = ["Low", "High"]
    param_cont.str_for_value = MagicMock(side_effect=Exception("no display string"))

    param_quant = _make_param(name="Mode", value=1.0, min_val=0.0, max_val=2.0, quantized=True)
    param_quant.value_items = ["Off", "On", "Auto"]
    param_quant.str_for_value = MagicMock(return_value="On")

    chain_device = _make_device(
        name="Chain Device", class_name="AudioEffect", params=[param_cont, param_quant]
    )
    chain = _make_chain()
    chain.devices = [chain_device]

    rack = _make_device(name="Rack", class_name="AudioEffectGroupDevice", chains=[chain])
    song.tracks[0].devices = [rack]

    result = tools.get_rack_contents(0, 0)

    assert result["ok"] is True
    assert result["count"] == 1
    assert result["chains"][0]["chain_index"] == 0
    assert result["chains"][0]["chain_name"] == "Chain 1"

    returned_device = result["chains"][0]["devices"][0]
    assert returned_device["device_index"] == 0
    assert returned_device["name"] == "Chain Device"
    assert returned_device["class_name"] == "AudioEffect"
    assert returned_device["is_active"] is True

    returned_params = returned_device["parameters"]
    assert returned_params[0]["name"] == "Gain"
    assert returned_params[0]["display_value"] == "0.25"
    assert returned_params[0]["is_quantized"] is False
    assert returned_params[0]["value_items"] == []

    assert returned_params[1]["name"] == "Mode"
    assert returned_params[1]["display_value"] == "On"
    assert returned_params[1]["is_quantized"] is True
    assert returned_params[1]["value_items"] == ["Off", "On", "Auto"]


def test_get_rack_contents_non_rack_returns_clear_error(tools, song):
    non_rack = _make_device(name="Compressor", class_name="Compressor2")
    song.tracks[0].devices = [non_rack]

    result = tools.get_rack_contents(0, 0)

    assert result["ok"] is False
    assert "not a rack" in result["error"]


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
