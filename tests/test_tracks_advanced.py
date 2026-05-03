"""
Tests for TracksMixin advanced methods: groups, freeze/flatten, annotations, delay.
"""

from unittest.mock import MagicMock


def test_create_group_track_no_name(tools, song):
    result = tools.create_group_track()
    assert result["ok"] is True


def test_create_group_track_with_name(tools, song):
    result = tools.create_group_track(name="Group 1")
    assert result["ok"] is True


def test_create_group_track_exception(tools, song):
    song.create_group_track.side_effect = Exception("err")
    result = tools.create_group_track()
    assert result["ok"] is False


def test_group_tracks_valid(tools, song):
    song.tracks = [MagicMock(), MagicMock()]
    result = tools.group_tracks(0, 1)
    assert result["ok"] is True


def test_group_tracks_invalid_start(tools, song):
    result = tools.group_tracks(-1, 0)
    assert result["ok"] is False


def test_group_tracks_invalid_end(tools, song):
    result = tools.group_tracks(0, 99)
    assert result["ok"] is False


def test_group_tracks_end_before_start(tools, song):
    song.tracks = [MagicMock(), MagicMock()]
    result = tools.group_tracks(1, 0)
    assert result["ok"] is False


def test_group_tracks_exception(tools, song):
    song.create_group_track.side_effect = Exception("err")
    song.tracks = [MagicMock(), MagicMock()]
    result = tools.group_tracks(0, 1)
    assert result["ok"] is False


def test_get_track_is_grouped_not_grouped(tools, song):
    song.tracks[0].group_track = None
    song.tracks[0].is_foldable = False
    result = tools.get_track_is_grouped(0)
    assert result["ok"] is True
    assert result["is_grouped"] is False


def test_get_track_is_grouped_is_grouped(tools, song):
    other_track = MagicMock()
    song.tracks = [MagicMock(), other_track]
    song.tracks[0].group_track = other_track
    song.tracks[0].is_foldable = False
    result = tools.get_track_is_grouped(0)
    assert result["ok"] is True


def test_get_track_is_grouped_invalid(tools):
    result = tools.get_track_is_grouped(-1)
    assert result["ok"] is False


def test_ungroup_track_is_group(tools, song):
    song.tracks[0].is_foldable = True
    result = tools.ungroup_track(0)
    assert result["ok"] is True


def test_ungroup_track_not_group(tools, song):
    song.tracks[0].is_foldable = False
    result = tools.ungroup_track(0)
    assert result["ok"] is False


def test_ungroup_track_invalid(tools):
    result = tools.ungroup_track(-1)
    assert result["ok"] is False


def test_freeze_track_can_freeze(tools, song):
    song.tracks[0].freeze_available = True
    result = tools.freeze_track(0)
    assert result["ok"] is True
    assert song.tracks[0].freeze_state == 1


def test_freeze_track_no_freeze_state(tools, song):
    song.tracks[0].freeze_available = True
    del song.tracks[0].freeze_state
    result = tools.freeze_track(0)
    assert result["ok"] is False


def test_freeze_track_cannot_freeze(tools, song):
    song.tracks[0].freeze_available = False
    result = tools.freeze_track(0)
    assert result["ok"] is False


def test_freeze_track_exception(tools, song):
    song.tracks = None
    result = tools.freeze_track(0)
    assert result["ok"] is False


def test_unfreeze_track_with_state(tools, song):
    result = tools.unfreeze_track(0)
    assert result["ok"] is True
    assert song.tracks[0].freeze_state == 0


def test_unfreeze_track_without_state(tools, song):
    del song.tracks[0].freeze_state
    result = tools.unfreeze_track(0)
    assert result["ok"] is False


def test_unfreeze_track_exception(tools, song):
    song.tracks[0].freeze_state = MagicMock(side_effect=Exception("x"))
    result = tools.unfreeze_track(0)
    assert result["ok"] is True


def test_flatten_track_with_attr(tools, song):
    result = tools.flatten_track(0)
    assert result["ok"] is True
    song.tracks[0].flatten.assert_called_once()


def test_flatten_track_without_attr(tools, song):
    del song.tracks[0].flatten
    result = tools.flatten_track(0)
    assert result["ok"] is False


def test_flatten_track_exception(tools, song):
    song.tracks[0].flatten.side_effect = Exception("err")
    result = tools.flatten_track(0)
    assert result["ok"] is False


def test_get_track_annotation_with_attr(tools, song):
    song.tracks[0].annotation = "my note"
    result = tools.get_track_annotation(0)
    assert result["ok"] is True
    assert result["annotation"] == "my note"


def test_get_track_annotation_without_attr(tools, song):
    del song.tracks[0].annotation
    result = tools.get_track_annotation(0)
    assert result["ok"] is False


def test_get_track_annotation_exception(tools, song):
    song.tracks = None
    result = tools.get_track_annotation(0)
    assert result["ok"] is False


def test_set_track_annotation_with_attr(tools, song):
    result = tools.set_track_annotation(0, "note text")
    assert result["ok"] is True


def test_set_track_annotation_without_attr(tools, song):
    del song.tracks[0].annotation
    result = tools.set_track_annotation(0, "note text")
    assert result["ok"] is False


def test_set_track_annotation_exception(tools, song):
    song.tracks[0].annotation = MagicMock(side_effect=Exception("x"))
    result = tools.set_track_annotation(0, "note text")
    assert result["ok"] is True


def test_get_track_delay_with_attr(tools, song):
    song.tracks[0].delay = 0.0
    result = tools.get_track_delay(0)
    assert result["ok"] is True
    assert result["delay"] == 0.0


def test_get_track_delay_without_attr(tools, song):
    del song.tracks[0].delay
    result = tools.get_track_delay(0)
    assert result["ok"] is False


def test_get_track_delay_exception(tools, song):
    song.tracks = None
    result = tools.get_track_delay(0)
    assert result["ok"] is False


def test_set_track_delay_with_attr(tools, song):
    result = tools.set_track_delay(0, 100.0)
    assert result["ok"] is True


def test_set_track_delay_without_attr(tools, song):
    del song.tracks[0].delay
    result = tools.set_track_delay(0, 100.0)
    assert result["ok"] is False


def test_set_track_delay_exception(tools):
    result = tools.set_track_delay(0, "bad")
    assert result["ok"] is False


def test_create_group_track_with_name_covers_assignment(tools, song):
    tracks_mock = MagicMock()
    tracks_mock.__len__ = MagicMock(side_effect=[0, 1, 1])
    song.tracks = tracks_mock
    result = tools.create_group_track(name="Group Bus")
    assert result["ok"] is True


def test_get_track_is_grouped_except_block(tools):
    tools.song = None
    result = tools.get_track_is_grouped(0)
    assert result["ok"] is False


def test_ungroup_track_except_block(tools):
    tools.song = None
    result = tools.ungroup_track(0)
    assert result["ok"] is False


def test_unfreeze_track_except_block(tools):
    tools.song = None
    result = tools.unfreeze_track(0)
    assert result["ok"] is False


def test_set_track_annotation_except_block(tools):
    tools.song = None
    result = tools.set_track_annotation(0, "text")
    assert result["ok"] is False


def test_rename_track_except_block(tools):
    tools.song = None
    result = tools.rename_track(0, "x")
    assert result["ok"] is False


def test_solo_track_except_block(tools):
    tools.song = None
    result = tools.solo_track(0)
    assert result["ok"] is False


def test_mute_track_except_block(tools):
    tools.song = None
    result = tools.mute_track(0)
    assert result["ok"] is False
