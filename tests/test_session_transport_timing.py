"""
Tests for SessionTransportMixin timing, navigation, and state methods.
"""

from unittest.mock import MagicMock


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


def test_save_project(tools, monkeypatch):
    calls = []

    def _ok_check_call(command):
        calls.append(command)

    monkeypatch.setattr(
        "ALiveMCP_Remote.tools.session_transport.subprocess.check_call", _ok_check_call
    )
    monkeypatch.setattr("ALiveMCP_Remote.tools.session_transport.time.sleep", lambda _: None)

    result = tools.save_project()

    assert result["ok"] is True
    assert result["message"] == "Project saved"
    assert len(calls) == 2


def test_save_project_exception(tools, monkeypatch):
    def _failing_check_call(_):
        raise Exception("disk full")

    monkeypatch.setattr(
        "ALiveMCP_Remote.tools.session_transport.subprocess.check_call",
        _failing_check_call,
    )

    result = tools.save_project()
    assert result == {"ok": False, "error": "disk full"}


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


def test_set_back_to_arranger(tools, song):
    result = tools.set_back_to_arranger(False)
    assert result["ok"] is True


def test_set_back_to_arranger_exception(tools, song):
    song.back_to_arranger = MagicMock(side_effect=Exception("x"))
    result = tools.set_back_to_arranger(False)
    assert result["ok"] is True
