"""
Tests for ScenesMixin: scene operations and scene color management.
"""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# create_scene
# ---------------------------------------------------------------------------


def test_create_scene_no_name(tools, song):
    song.scenes = MagicMock()  # so song.scenes[any_index] works after creation
    result = tools.create_scene()
    assert result["ok"] is True
    song.create_scene.assert_called_once()


def test_create_scene_with_name(tools, song):
    song.scenes = MagicMock()
    result = tools.create_scene(name="Verse")
    assert result["ok"] is True


def test_create_scene_exception(tools, song):
    song.create_scene.side_effect = Exception("err")
    result = tools.create_scene()
    assert result == {"ok": False, "error": "err"}


# ---------------------------------------------------------------------------
# delete_scene
# ---------------------------------------------------------------------------


def test_delete_scene_valid(tools, song):
    result = tools.delete_scene(0)
    assert result["ok"] is True
    song.delete_scene.assert_called_once_with(0)


def test_delete_scene_negative_index(tools):
    result = tools.delete_scene(-1)
    assert result == {"ok": False, "error": "Invalid scene index"}


def test_delete_scene_out_of_range(tools, song):
    result = tools.delete_scene(len(song.scenes))
    assert result["ok"] is False


def test_delete_scene_exception(tools, song):
    song.delete_scene.side_effect = Exception("err")
    result = tools.delete_scene(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# duplicate_scene
# ---------------------------------------------------------------------------


def test_duplicate_scene_valid(tools, song):
    result = tools.duplicate_scene(0)
    assert result["ok"] is True
    assert result["new_index"] == 1


def test_duplicate_scene_invalid(tools, song):
    result = tools.duplicate_scene(99)
    assert result["ok"] is False


def test_duplicate_scene_exception(tools, song):
    song.duplicate_scene.side_effect = Exception("err")
    result = tools.duplicate_scene(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# launch_scene
# ---------------------------------------------------------------------------


def test_launch_scene_valid(tools, song):
    result = tools.launch_scene(0)
    assert result["ok"] is True
    song.scenes[0].fire.assert_called_once()


def test_launch_scene_invalid(tools):
    result = tools.launch_scene(-1)
    assert result["ok"] is False


def test_launch_scene_exception(tools, song):
    song.scenes[0].fire.side_effect = Exception("err")
    result = tools.launch_scene(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# rename_scene
# ---------------------------------------------------------------------------


def test_rename_scene_valid(tools, song):
    result = tools.rename_scene(0, "Chorus")
    assert result["ok"] is True
    assert result["name"] == "Chorus"


def test_rename_scene_invalid(tools):
    result = tools.rename_scene(-1, "x")
    assert result["ok"] is False


def test_rename_scene_exception(tools, song):
    song.scenes[0].name = MagicMock(side_effect=Exception("err"))
    result = tools.rename_scene(0, "x")
    assert result["ok"] is True  # MagicMock assignment doesn't raise


# ---------------------------------------------------------------------------
# get_scene_info
# ---------------------------------------------------------------------------


def test_get_scene_info_valid(tools, song):
    result = tools.get_scene_info(0)
    assert result["ok"] is True
    assert result["scene_index"] == 0


def test_get_scene_info_invalid(tools):
    result = tools.get_scene_info(-1)
    assert result["ok"] is False


def test_get_scene_info_exception(tools, song):
    song.scenes = None  # None[0] → TypeError caught by except
    result = tools.get_scene_info(0)
    assert result["ok"] is False


def test_get_scene_info_no_color(tools, song):
    del song.scenes[0].color
    result = tools.get_scene_info(0)
    assert result["ok"] is True
    assert result["color"] is None


def test_get_scene_info_no_tempo(tools, song):
    del song.scenes[0].tempo
    result = tools.get_scene_info(0)
    assert result["ok"] is True
    assert result["tempo"] is None


# ---------------------------------------------------------------------------
# get_scene_color / set_scene_color
# ---------------------------------------------------------------------------


def test_get_scene_color_with_attr(tools, song):
    song.scenes[0].color = 7
    result = tools.get_scene_color(0)
    assert result["ok"] is True
    assert result["color"] == 7


def test_get_scene_color_without_attr(tools, song):
    del song.scenes[0].color
    result = tools.get_scene_color(0)
    assert result["ok"] is False


def test_get_scene_color_exception(tools, song):
    song.scenes = None  # None[0] → TypeError caught by except
    result = tools.get_scene_color(0)
    assert result["ok"] is False


def test_set_scene_color_with_attr(tools, song):
    result = tools.set_scene_color(0, 12)
    assert result["ok"] is True


def test_set_scene_color_without_attr(tools, song):
    del song.scenes[0].color
    result = tools.set_scene_color(0, 12)
    assert result["ok"] is False


def test_set_scene_color_exception(tools, song):
    song.scenes[0].color = MagicMock(side_effect=Exception("err"))
    result = tools.set_scene_color(0, "bad")
    assert result["ok"] is False


def test_rename_scene_except_block(tools):
    tools.song = None
    result = tools.rename_scene(0, "x")
    assert result["ok"] is False
