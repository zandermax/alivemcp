"""Tests for M4L sampler tools: sample length and playback mode."""


# ---------------------------------------------------------------------------
# get_sample_length
# ---------------------------------------------------------------------------


def test_get_sample_length_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.sample_length = 44100.0
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is True
    assert result["sample_length"] == 44100.0


def test_get_sample_length_without_attr(tools, song):
    del song.tracks[0].clip_slots[0].clip.sample_length
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is False


def test_get_sample_length_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is False


def test_get_sample_length_except_block(tools):
    tools.song = None
    result = tools.get_sample_length(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_sample_playback_mode / set_sample_playback_mode
# ---------------------------------------------------------------------------


def test_get_sample_playback_mode_with_attr(tools, song):
    song.tracks[0].devices[0].playback_mode = 0
    result = tools.get_sample_playback_mode(0, 0)
    assert result["ok"] is True


def test_get_sample_playback_mode_without_attr(tools, song):
    del song.tracks[0].devices[0].playback_mode
    result = tools.get_sample_playback_mode(0, 0)
    assert result["ok"] is False


def test_get_sample_playback_mode_exception(tools, song):
    song.tracks = None
    result = tools.get_sample_playback_mode(0, 0)
    assert result["ok"] is False


def test_set_sample_playback_mode_with_attr(tools, song):
    result = tools.set_sample_playback_mode(0, 0, 1)
    assert result["ok"] is True


def test_set_sample_playback_mode_without_attr(tools, song):
    del song.tracks[0].devices[0].playback_mode
    result = tools.set_sample_playback_mode(0, 0, 1)
    assert result["ok"] is False


def test_set_sample_playback_mode_except_block(tools):
    tools.song = None
    result = tools.set_sample_playback_mode(0, 0, 1)
    assert result["ok"] is False
