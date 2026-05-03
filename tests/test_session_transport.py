"""
Tests for SessionTransportMixin session and transport methods.
"""

from unittest.mock import MagicMock


def test_start_playback_when_not_playing(tools, song):
    song.is_playing = False
    result = tools.start_playback()
    assert result["ok"] is True
    song.start_playing.assert_called_once()


def test_start_playback_when_already_playing(tools, song):
    song.is_playing = True
    result = tools.start_playback()
    assert result["ok"] is True
    song.start_playing.assert_not_called()


def test_start_playback_exception(tools, song):
    song.is_playing = False
    song.start_playing.side_effect = Exception("boom")
    result = tools.start_playback()
    assert result == {"ok": False, "error": "boom"}


def test_stop_playback_when_playing(tools, song):
    song.is_playing = True
    result = tools.stop_playback()
    assert result["ok"] is True
    song.stop_playing.assert_called_once()


def test_stop_playback_when_not_playing(tools, song):
    song.is_playing = False
    result = tools.stop_playback()
    assert result["ok"] is True
    song.stop_playing.assert_not_called()


def test_stop_playback_exception(tools, song):
    song.is_playing = True
    song.stop_playing.side_effect = Exception("err")
    result = tools.stop_playback()
    assert result["ok"] is False


def test_start_recording_not_playing(tools, song):
    song.is_playing = False
    result = tools.start_recording()
    assert result["ok"] is True
    assert song.record_mode is True
    song.start_playing.assert_called_once()


def test_start_recording_already_playing(tools, song):
    song.is_playing = True
    result = tools.start_recording()
    assert result["ok"] is True
    song.start_playing.assert_not_called()


def test_start_recording_exception(tools, song):
    song.is_playing = False
    song.start_playing.side_effect = Exception("fail")
    result = tools.start_recording()
    assert result["ok"] is False


def test_stop_recording(tools, song):
    result = tools.stop_recording()
    assert result["ok"] is True
    assert song.record_mode is False


def test_stop_recording_exception(tools, song):
    song.stop_playing.side_effect = Exception("x")
    delattr(song, "record_mode")
    result = tools.stop_recording()
    assert result["ok"] is True


def test_continue_playing(tools, song):
    result = tools.continue_playing()
    assert result["ok"] is True
    song.continue_playing.assert_called_once()


def test_continue_playing_exception(tools, song):
    song.continue_playing.side_effect = Exception("err")
    result = tools.continue_playing()
    assert result == {"ok": False, "error": "err"}


def test_get_session_info(tools, song):
    song.is_playing = True
    song.tempo = 120.0
    song.signature_numerator = 4
    song.signature_denominator = 4
    song.current_song_time = 0.0
    song.loop_start = 0.0
    song.loop_length = 4.0
    song.tracks = [MagicMock()]
    song.scenes = [MagicMock()]
    song.record_mode = False
    song.metronome = False
    song.nudge_up = False
    song.nudge_down = False

    result = tools.get_session_info()
    assert result["ok"] is True
    assert result["is_playing"] is True
    assert result["tempo"] == 120.0
    assert result["num_tracks"] == 1
    assert result["num_scenes"] == 1


def test_get_session_info_exception(tools, song):
    song.tracks = None
    result = tools.get_session_info()
    assert result["ok"] is False
