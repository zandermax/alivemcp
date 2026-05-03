"""
Tests for ArrangementMixin view/navigation and loop controls.
"""

from unittest.mock import MagicMock, patch

import pytest

import ALiveMCP_Remote.tools.arrangement as arrangement_module


@pytest.fixture
def live_in_arrangement():
    fresh_live = MagicMock()
    with patch.object(arrangement_module, "Live", fresh_live, create=True):
        yield fresh_live


def test_show_clip_view_success(tools, live_in_arrangement):
    result = tools.show_clip_view()
    assert result["ok"] is True


def test_show_clip_view_no_show_view(tools, live_in_arrangement):
    del live_in_arrangement.Application.get_application.return_value.view.show_view
    result = tools.show_clip_view()
    assert result["ok"] is False


def test_show_clip_view_exception(tools):
    result = tools.show_clip_view()
    assert result["ok"] is False


def test_show_arrangement_view_success(tools, live_in_arrangement):
    result = tools.show_arrangement_view()
    assert result["ok"] is True


def test_show_arrangement_view_no_show_view(tools, live_in_arrangement):
    del live_in_arrangement.Application.get_application.return_value.view.show_view
    result = tools.show_arrangement_view()
    assert result["ok"] is False


def test_show_arrangement_view_exception(tools):
    result = tools.show_arrangement_view()
    assert result["ok"] is False


def test_focus_track_with_selected_track_attr(tools, song):
    result = tools.focus_track(0)
    assert result["ok"] is True


def test_focus_track_without_selected_track_attr(tools, song):
    del song.view.selected_track
    result = tools.focus_track(0)
    assert result["ok"] is False


def test_focus_track_invalid(tools):
    result = tools.focus_track(-1)
    assert result["ok"] is False


def test_focus_track_exception(tools, song):
    song.view.selected_track = MagicMock(side_effect=Exception("err"))
    result = tools.focus_track(0)
    assert result["ok"] is True


def test_scroll_view_to_time_with_visible_tracks(tools, song):
    result = tools.scroll_view_to_time(8.0)
    assert result["ok"] is True


def test_scroll_view_to_time_without_visible_tracks(tools, song):
    del song.view.visible_tracks
    result = tools.scroll_view_to_time(8.0)
    assert result["ok"] is False


def test_scroll_view_to_time_exception(tools):
    result = tools.scroll_view_to_time("bad")
    assert result["ok"] is False


def test_set_loop_enabled(tools, song):
    result = tools.set_loop_enabled(True)
    assert result["ok"] is True
    assert song.loop is True


def test_set_loop_enabled_exception(tools, song):
    song.loop = MagicMock(side_effect=Exception("err"))
    result = tools.set_loop_enabled(True)
    assert result["ok"] is True


def test_get_loop_enabled(tools, song):
    song.loop = True
    song.loop_start = 0.0
    song.loop_length = 8.0
    result = tools.get_loop_enabled()
    assert result["ok"] is True
    assert result["loop_enabled"] is True


def test_get_loop_enabled_exception(tools, song):
    song.loop_start = "bad"
    result = tools.get_loop_enabled()
    assert result["ok"] is False


def test_focus_track_except_block(tools):
    tools.song = None
    result = tools.focus_track(0)
    assert result["ok"] is False


def test_set_loop_enabled_except_block(tools):
    tools.song = None
    result = tools.set_loop_enabled(True)
    assert result["ok"] is False
