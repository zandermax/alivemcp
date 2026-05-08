"""
Tests for ArrangementMixin browser and color utility methods.
"""


def test_browse_devices(tools):
    result = tools.browse_devices()
    assert result["ok"] is True
    assert len(result["device_types"]) > 0


def test_browse_plugins(tools):
    result = tools.browse_plugins("vst")
    assert result["ok"] is True
    assert result["plugin_type"] == "vst"


def test_browse_plugins_exception(tools, song):
    result = tools.browse_plugins()
    assert result["ok"] is True


def test_load_device_from_browser_delegates_to_add_device(tools, song):
    result = tools.load_device_from_browser(0, "EQ Eight")
    assert result["ok"] is True
    assert result["device_name"] == "EQ Eight"


def test_get_browser_items(tools):
    result = tools.get_browser_items("devices")
    assert result["ok"] is True
    assert result["category"] == "devices"


def test_get_browser_items_exception(tools, song):
    result = tools.get_browser_items()
    assert result["ok"] is True


def test_get_clip_color_via_color_index(tools, song):
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is True


def test_get_clip_color_via_color(tools, song):
    del song.tracks[0].clip_slots[0].clip.color_index
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is True


def test_get_clip_color_no_color_attrs(tools, song):
    del song.tracks[0].clip_slots[0].clip.color_index
    del song.tracks[0].clip_slots[0].clip.color
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is False


def test_get_clip_color_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is False


def test_get_clip_color_invalid_track(tools):
    result = tools.get_clip_color(-1, 0)
    assert result["ok"] is False


def test_get_clip_color_invalid_clip(tools, song):
    result = tools.get_clip_color(0, 99)
    assert result["ok"] is False


def test_get_track_color_via_color_index(tools, song):
    result = tools.get_track_color(0)
    assert result["ok"] is True


def test_get_track_color_via_color(tools, song):
    del song.tracks[0].color_index
    result = tools.get_track_color(0)
    assert result["ok"] is True


def test_get_track_color_no_color_attrs(tools, song):
    del song.tracks[0].color_index
    del song.tracks[0].color
    result = tools.get_track_color(0)
    assert result["ok"] is False


def test_get_track_color_invalid(tools):
    result = tools.get_track_color(-1)
    assert result["ok"] is False


def test_get_clip_color_except_block(tools):
    tools.song = None
    result = tools.get_clip_color(0, 0)
    assert result["ok"] is False


def test_get_track_color_except_block(tools):
    tools.song = None
    result = tools.get_track_color(0)
    assert result["ok"] is False
