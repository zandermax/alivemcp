"""
Tests for ArrangementMixin locators and relative jump operations.
"""


def test_create_locator_with_create_cue_point(tools, song):
    result = tools.create_locator(4.0, name="Drop")
    assert result["ok"] is True
    song.create_cue_point.assert_called_once_with(4.0)


def test_create_locator_without_create_cue_point(tools, song):
    del song.create_cue_point
    result = tools.create_locator(4.0)
    assert result["ok"] is False


def test_create_locator_exception(tools, song):
    song.create_cue_point.side_effect = Exception("err")
    result = tools.create_locator(4.0)
    assert result["ok"] is False


def test_delete_locator_with_cue_points(tools, song):
    cue = song.cue_points[0]
    result = tools.delete_locator(0)
    assert result["ok"] is True
    cue.delete.assert_called_once()


def test_delete_locator_invalid_index(tools, song):
    result = tools.delete_locator(5)
    assert result["ok"] is False


def test_delete_locator_without_cue_points(tools, song):
    del song.cue_points
    result = tools.delete_locator(0)
    assert result["ok"] is False


def test_delete_locator_cue_no_delete_method(tools, song):
    cue = song.cue_points[0]
    del cue.delete
    result = tools.delete_locator(0)
    assert result["ok"] is False


def test_delete_locator_exception(tools, song):
    song.cue_points = []

    bad_cue = type("Cue", (), {})()

    def _raise():
        raise Exception("delete failed")

    bad_cue.delete = _raise
    song.cue_points.append(bad_cue)

    result = tools.delete_locator(0)
    assert result["ok"] is False


def test_get_locators_with_cue_points(tools, song):
    cue = song.cue_points[0]
    cue.time = 4.0
    cue.name = "Bridge"
    result = tools.get_locators()
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_locators_without_cue_points(tools, song):
    del song.cue_points
    result = tools.get_locators()
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_locators_cue_no_time_or_name(tools, song):
    cue = song.cue_points[0]
    del cue.time
    del cue.name
    result = tools.get_locators()
    assert result["ok"] is True


def test_get_locators_exception(tools, song):
    song.cue_points = None
    result = tools.get_locators()
    assert result["ok"] is False


def test_jump_by_amount_positive(tools, song):
    song.current_song_time = 4.0
    result = tools.jump_by_amount(2.0)
    assert result["ok"] is True
    assert result["old_time"] == 4.0
    assert result["jumped_by"] == 2.0


def test_jump_by_amount_negative_clamped(tools, song):
    song.current_song_time = 1.0
    result = tools.jump_by_amount(-5.0)
    assert result["ok"] is True


def test_jump_by_amount_exception(tools, song):
    song.current_song_time = "bad"
    result = tools.jump_by_amount(1.0)
    assert result["ok"] is False
