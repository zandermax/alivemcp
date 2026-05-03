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


def test_set_tempo_valid(tools, song):
    result = tools.set_tempo(140)
    assert result["ok"] is True
    assert song.tempo == 140.0


def test_set_tempo_too_low(tools):
    result = tools.set_tempo(10)
    assert result == {"ok": False, "error": "BPM must be between 20 and 999"}


def test_set_tempo_too_high(tools):
    result = tools.set_tempo(1000)
    assert result == {"ok": False, "error": "BPM must be between 20 and 999"}


def test_set_tempo_exception(tools, song):
    song.tempo = MagicMock(side_effect=Exception("err"))
    result = tools.set_tempo("not-a-number")
    assert result["ok"] is False


def test_set_time_signature_valid(tools, song):
    result = tools.set_time_signature(3, 4)
    assert result["ok"] is True
    assert song.signature_numerator == 3
    assert song.signature_denominator == 4


def test_set_time_signature_bad_numerator_low(tools):
    result = tools.set_time_signature(0, 4)
    assert result["ok"] is False
    assert "Numerator" in result["error"]


def test_set_time_signature_bad_numerator_high(tools):
    result = tools.set_time_signature(100, 4)
    assert result["ok"] is False


def test_set_time_signature_bad_denominator(tools):
    result = tools.set_time_signature(4, 3)
    assert result["ok"] is False
    assert "Denominator" in result["error"]


def test_set_time_signature_exception(tools):
    result = tools.set_time_signature("x", 4)
    assert result["ok"] is False


def test_set_loop_start(tools, song):
    result = tools.set_loop_start(8.0)
    assert result["ok"] is True
    assert song.loop_start == 8.0


def test_set_loop_start_exception(tools, song):
    song.loop_start = MagicMock(side_effect=Exception("err"))
    result = tools.set_loop_start("bad")
    assert result["ok"] is False


def test_set_loop_length(tools, song):
    result = tools.set_loop_length(16.0)
    assert result["ok"] is True


def test_set_loop_length_exception(tools):
    result = tools.set_loop_length("oops")
    assert result["ok"] is False


def test_set_metronome(tools, song):
    result = tools.set_metronome(True)
    assert result["ok"] is True
    assert song.metronome is True


def test_set_metronome_exception(tools, song):
    song.metronome = property(lambda s: (_ for _ in ()).throw(Exception("err")))
    result = tools.set_metronome(True)
    assert result["ok"] is True


def test_tap_tempo(tools, song):
    result = tools.tap_tempo()
    assert result["ok"] is True
    song.tap_tempo.assert_called_once()


def test_tap_tempo_exception(tools, song):
    song.tap_tempo.side_effect = Exception("err")
    result = tools.tap_tempo()
    assert result["ok"] is False


def test_undo(tools, song):
    result = tools.undo()
    assert result["ok"] is True
    song.undo.assert_called_once()


def test_undo_exception(tools, song):
    song.undo.side_effect = Exception("err")
    result = tools.undo()
    assert result["ok"] is False


def test_redo(tools, song):
    result = tools.redo()
    assert result["ok"] is True
    song.redo.assert_called_once()


def test_redo_exception(tools, song):
    song.redo.side_effect = Exception("err")
    result = tools.redo()
    assert result["ok"] is False


def test_jump_to_time(tools, song):
    result = tools.jump_to_time(4.0)
    assert result["ok"] is True
    assert song.current_song_time == 4.0


def test_jump_to_time_exception(tools):
    result = tools.jump_to_time("bad")
    assert result["ok"] is False


def test_get_current_time(tools, song):
    song.current_song_time = 2.5
    song.is_playing = True
    result = tools.get_current_time()
    assert result["ok"] is True
    assert result["current_song_time"] == 2.5
    assert result["is_playing"] is True


def test_get_current_time_exception(tools, song):
    song.current_song_time = "bad"
    result = tools.get_current_time()
    assert result["ok"] is False


def test_set_arrangement_overdub(tools, song):
    result = tools.set_arrangement_overdub(True)
    assert result["ok"] is True
    assert song.arrangement_overdub is True


def test_set_arrangement_overdub_exception(tools, song):
    song.arrangement_overdub = property(lambda s: (_ for _ in ()).throw(Exception("e")))
    result = tools.set_arrangement_overdub(True)
    assert result["ok"] is True


def test_set_back_to_arranger(tools, song):
    result = tools.set_back_to_arranger(False)
    assert result["ok"] is True


def test_set_back_to_arranger_exception(tools, song):
    song.back_to_arranger = MagicMock(side_effect=Exception("x"))
    result = tools.set_back_to_arranger(False)
    assert result["ok"] is True
