"""Tests for M4L audio clip tools: warp mode, file path, warping, and warp markers."""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# get_clip_warp_mode
# ---------------------------------------------------------------------------


def test_get_clip_warp_mode_audio_clip(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is True


def test_get_clip_warp_mode_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.get_clip_warp_mode(0, 0)
    assert result == {"ok": False, "error": "Clip is not an audio clip"}


def test_get_clip_warp_mode_invalid_track(tools):
    result = tools.get_clip_warp_mode(-1, 0)
    assert result["ok"] is False


def test_get_clip_warp_mode_invalid_clip(tools, song):
    result = tools.get_clip_warp_mode(0, 99)
    assert result["ok"] is False


def test_get_clip_warp_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is False


def test_get_clip_warp_mode_no_warp_mode_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warp_mode
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is True  # falls back to default 0


def test_get_clip_warp_mode_except_block(tools):
    tools.song = None
    result = tools.get_clip_warp_mode(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_clip_warp_mode
# ---------------------------------------------------------------------------


def test_set_clip_warp_mode_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    result = tools.set_clip_warp_mode(0, 0, 2)
    assert result["ok"] is True


def test_set_clip_warp_mode_without_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warp_mode
    result = tools.set_clip_warp_mode(0, 0, 2)
    assert result["ok"] is False


def test_set_clip_warp_mode_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.set_clip_warp_mode(0, 0, 2)
    assert result["ok"] is False


def test_set_clip_warp_mode_invalid(tools):
    result = tools.set_clip_warp_mode(-1, 0, 2)
    assert result["ok"] is False


def test_set_clip_warp_mode_invalid_clip(tools, song):
    result = tools.set_clip_warp_mode(0, 99, 0)
    assert result["ok"] is False


def test_set_clip_warp_mode_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_warp_mode(0, 0, 0)
    assert result["ok"] is False


def test_set_clip_warp_mode_except_block(tools):
    tools.song = None
    result = tools.set_clip_warp_mode(0, 0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_clip_file_path
# ---------------------------------------------------------------------------


def test_get_clip_file_path_via_file_path(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    song.tracks[0].clip_slots[0].clip.file_path = "/audio/kick.wav"
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is True
    assert result["file_path"] == "/audio/kick.wav"


def test_get_clip_file_path_via_sample(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.is_audio_clip = True
    del clip.file_path
    clip.sample.file_path = "/audio/snare.wav"
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is True


def test_get_clip_file_path_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is False


def test_get_clip_file_path_invalid(tools):
    result = tools.get_clip_file_path(-1, 0)
    assert result["ok"] is False


def test_get_clip_file_path_invalid_clip(tools, song):
    result = tools.get_clip_file_path(0, 99)
    assert result["ok"] is False


def test_get_clip_file_path_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is False


def test_get_clip_file_path_except_block(tools):
    tools.song = None
    result = tools.get_clip_file_path(0, 0)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# set_clip_warping
# ---------------------------------------------------------------------------


def test_set_clip_warping_with_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is True


def test_set_clip_warping_without_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warping
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_warping_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_warping_invalid(tools):
    result = tools.set_clip_warping(-1, 0, True)
    assert result["ok"] is False


def test_set_clip_warping_invalid_clip(tools, song):
    result = tools.set_clip_warping(0, 99, True)
    assert result["ok"] is False


def test_set_clip_warping_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


def test_set_clip_warping_except_block(tools):
    tools.song = None
    result = tools.set_clip_warping(0, 0, True)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# get_warp_markers
# ---------------------------------------------------------------------------


def test_get_warp_markers_with_markers(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.is_audio_clip = True
    marker = MagicMock()
    marker.sample_time = 0.0
    marker.beat_time = 0.0
    clip.warp_markers = [marker]
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_warp_markers_no_warp_markers_attr(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = True
    del song.tracks[0].clip_slots[0].clip.warp_markers
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is True
    assert result["count"] == 0


def test_get_warp_markers_not_audio(tools, song):
    song.tracks[0].clip_slots[0].clip.is_audio_clip = False
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is False


def test_get_warp_markers_invalid(tools):
    result = tools.get_warp_markers(-1, 0)
    assert result["ok"] is False


def test_get_warp_markers_invalid_clip(tools, song):
    result = tools.get_warp_markers(0, 99)
    assert result["ok"] is False


def test_get_warp_markers_no_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is False


def test_get_warp_markers_no_sample_time(tools, song):
    clip = song.tracks[0].clip_slots[0].clip
    clip.is_audio_clip = True
    marker = MagicMock()
    del marker.sample_time
    del marker.beat_time
    clip.warp_markers = [marker]
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is True


def test_get_warp_markers_except_block(tools):
    tools.song = None
    result = tools.get_warp_markers(0, 0)
    assert result["ok"] is False
