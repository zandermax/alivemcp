"""Tests for Live 12 take lane tools."""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# get_take_lanes
# ---------------------------------------------------------------------------


def test_get_take_lanes_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "Take 1"
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lanes(0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_take_lanes_lane_no_name(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lanes(0)
    assert result["ok"] is True


def test_get_take_lanes_without_attr(tools, song):
    del song.tracks[0].take_lanes
    result = tools.get_take_lanes(0)
    assert result["ok"] is False


def test_get_take_lanes_exception(tools, song):
    song.tracks[0].take_lanes = None
    result = tools.get_take_lanes(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# create_take_lane
# ---------------------------------------------------------------------------


def test_create_take_lane_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "New Take"
    song.tracks[0].create_take_lane.return_value = lane
    result = tools.create_take_lane(0, name="Take A")
    assert result["ok"] is True


def test_create_take_lane_without_create_attr(tools, song):
    del song.tracks[0].create_take_lane
    result = tools.create_take_lane(0)
    assert result["ok"] is False


def test_create_take_lane_no_name_attr_on_lane(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].create_take_lane.return_value = lane
    result = tools.create_take_lane(0)
    assert result["ok"] is True


def test_create_take_lane_exception(tools, song):
    song.tracks[0].create_take_lane.side_effect = Exception("err")
    result = tools.create_take_lane(0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_take_lane_name / set_take_lane_name
# ---------------------------------------------------------------------------


def test_get_take_lane_name_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "Take 2"
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is True
    assert result["name"] == "Take 2"


def test_get_take_lane_name_no_name(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].take_lanes = [lane]
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is True


def test_get_take_lane_name_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is False


def test_get_take_lane_name_except_block(tools):
    tools.song = None
    result = tools.get_take_lane_name(0, 0)
    assert result["ok"] is False


def test_set_take_lane_name_with_attr(tools, song):
    lane = MagicMock()
    lane.name = "Old"
    song.tracks[0].take_lanes = [lane]
    result = tools.set_take_lane_name(0, 0, "New Name")
    assert result["ok"] is True


def test_set_take_lane_name_no_name_attr(tools, song):
    lane = MagicMock()
    del lane.name
    song.tracks[0].take_lanes = [lane]
    result = tools.set_take_lane_name(0, 0, "New Name")
    assert result["ok"] is False


def test_set_take_lane_name_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.set_take_lane_name(0, 0, "x")
    assert result["ok"] is False


def test_set_take_lane_name_except_block(tools):
    tools.song = None
    result = tools.set_take_lane_name(0, 0, "x")
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# create_audio_clip_in_lane / create_midi_clip_in_lane
# ---------------------------------------------------------------------------


def test_create_audio_clip_in_lane_with_attr(tools, song):
    lane = MagicMock()
    song.tracks[0].take_lanes = [lane]
    result = tools.create_audio_clip_in_lane(0, 0, length=4.0)
    assert result["ok"] is True
    lane.create_audio_clip.assert_called_once_with(4.0)


def test_create_audio_clip_in_lane_without_create_attr(tools, song):
    lane = MagicMock()
    del lane.create_audio_clip
    song.tracks[0].take_lanes = [lane]
    result = tools.create_audio_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_audio_clip_in_lane_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.create_audio_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_audio_clip_in_lane_except_block(tools):
    tools.song = None
    result = tools.create_audio_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_midi_clip_in_lane_with_attr(tools, song):
    lane = MagicMock()
    song.tracks[0].take_lanes = [lane]
    result = tools.create_midi_clip_in_lane(0, 0, length=8.0)
    assert result["ok"] is True
    lane.create_midi_clip.assert_called_once_with(8.0)


def test_create_midi_clip_in_lane_without_create_attr(tools, song):
    lane = MagicMock()
    del lane.create_midi_clip
    song.tracks[0].take_lanes = [lane]
    result = tools.create_midi_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_midi_clip_in_lane_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.create_midi_clip_in_lane(0, 0)
    assert result["ok"] is False


def test_create_midi_clip_in_lane_except_block(tools):
    tools.song = None
    result = tools.create_midi_clip_in_lane(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_clips_in_take_lane
# ---------------------------------------------------------------------------


def test_get_clips_in_take_lane_with_clips(tools, song):
    clip = MagicMock()
    clip.name = "audio"
    clip.length = 4.0
    clip.is_midi_clip = False
    lane = MagicMock()
    lane.clips = [clip]
    song.tracks[0].take_lanes = [lane]
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_clips_in_take_lane_no_clips_attr(tools, song):
    lane = MagicMock()
    del lane.clips
    song.tracks[0].take_lanes = [lane]
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_clips_in_take_lane_no_take_lanes(tools, song):
    del song.tracks[0].take_lanes
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is False


def test_get_clips_in_take_lane_except_block(tools):
    tools.song = None
    result = tools.get_clips_in_take_lane(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# delete_take_lane
# ---------------------------------------------------------------------------


def test_delete_take_lane_with_attr(tools, song):
    result = tools.delete_take_lane(0, 0)
    assert result["ok"] is True
    song.tracks[0].delete_take_lane.assert_called_once_with(0)


def test_delete_take_lane_without_attr(tools, song):
    del song.tracks[0].delete_take_lane
    result = tools.delete_take_lane(0, 0)
    assert result["ok"] is False


def test_delete_take_lane_exception(tools, song):
    song.tracks[0].delete_take_lane.side_effect = Exception("err")
    result = tools.delete_take_lane(0, 0)
    assert result["ok"] is False
