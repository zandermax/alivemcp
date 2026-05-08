"""
Tests for SessionTransportMixin automation and metronome-volume methods.
"""

from unittest.mock import MagicMock


def test_re_enable_automation(tools, song):
    result = tools.re_enable_automation()
    assert result["ok"] is True
    song.re_enable_automation.assert_called_once()


def test_re_enable_automation_exception(tools, song):
    song.re_enable_automation.side_effect = Exception("err")
    result = tools.re_enable_automation()
    assert result["ok"] is False


def test_get_session_automation_record(tools, song):
    song.session_automation_record = True
    result = tools.get_session_automation_record()
    assert result["ok"] is True
    assert result["session_automation_record"] is True


def test_get_session_automation_record_exception(tools, song):
    tools.song = None
    result = tools.get_session_automation_record()
    assert result["ok"] is False


def test_set_session_automation_record(tools, song):
    result = tools.set_session_automation_record(True)
    assert result["ok"] is True


def test_set_session_automation_record_exception(tools, song):
    song.session_automation_record = MagicMock(side_effect=Exception("x"))
    result = tools.set_session_automation_record(True)
    assert result["ok"] is True


def test_get_session_record(tools, song):
    song.session_record = False
    result = tools.get_session_record()
    assert result["ok"] is True


def test_get_session_record_exception(tools, song):
    tools.song = None
    result = tools.get_session_record()
    assert result["ok"] is False


def test_set_session_record(tools, song):
    result = tools.set_session_record(True)
    assert result["ok"] is True


def test_set_session_record_exception(tools, song):
    song.session_record = MagicMock(side_effect=Exception("x"))
    result = tools.set_session_record(True)
    assert result["ok"] is True


def test_capture_midi(tools, song):
    result = tools.capture_midi()
    assert result["ok"] is True
    song.capture_midi.assert_called_once()


def test_capture_midi_exception(tools, song):
    song.capture_midi.side_effect = Exception("err")
    result = tools.capture_midi()
    assert result["ok"] is False


def test_get_metronome_volume_with_attribute(tools, song):
    song.metronome = 0.75
    result = tools.get_metronome_volume()
    assert result["ok"] is True
    assert result["volume"] == 0.75


def test_get_metronome_volume_without_attribute(tools, song):
    del song.metronome
    result = tools.get_metronome_volume()
    assert result["ok"] is False
    assert "not available" in result["error"]


def test_get_metronome_volume_exception(tools, song):
    song.metronome = "bad"
    result = tools.get_metronome_volume()
    assert result["ok"] is False


def test_set_metronome_volume_with_attribute(tools, song):
    song.metronome = 0.0
    result = tools.set_metronome_volume(0.5)
    assert result["ok"] is True


def test_set_metronome_volume_without_attribute(tools, song):
    del song.metronome
    result = tools.set_metronome_volume(0.5)
    assert result["ok"] is False


def test_set_metronome_volume_exception(tools):
    result = tools.set_metronome_volume("bad")
    assert result["ok"] is False


def test_set_session_automation_record_except_block(tools):
    tools.song = None
    result = tools.set_session_automation_record(True)
    assert result["ok"] is False


def test_set_session_record_except_block(tools):
    tools.song = None
    result = tools.set_session_record(True)
    assert result["ok"] is False


def test_stop_recording_except_block(tools):
    tools.song = None
    result = tools.stop_recording()
    assert result["ok"] is False


def test_set_metronome_except_block(tools):
    tools.song = None
    result = tools.set_metronome(True)
    assert result["ok"] is False


def test_set_arrangement_overdub_except_block(tools):
    tools.song = None
    result = tools.set_arrangement_overdub(True)
    assert result["ok"] is False


def test_set_back_to_arranger_except_block(tools):
    tools.song = None
    result = tools.set_back_to_arranger(True)
    assert result["ok"] is False


def test_set_punch_in_except_block(tools):
    tools.song = None
    result = tools.set_punch_in(True)
    assert result["ok"] is False


def test_set_punch_out_except_block(tools):
    tools.song = None
    result = tools.set_punch_out(True)
    assert result["ok"] is False


def test_set_punch_in(tools, song):
    result = tools.set_punch_in(True)
    assert result["ok"] is True
    assert song.punch_in is True


def test_set_punch_in_exception(tools, song):
    song.punch_in = MagicMock(side_effect=Exception("x"))
    result = tools.set_punch_in(True)
    assert result["ok"] is True


def test_set_punch_out(tools, song):
    result = tools.set_punch_out(True)
    assert result["ok"] is True


def test_set_punch_out_exception(tools, song):
    song.punch_out = MagicMock(side_effect=Exception("x"))
    result = tools.set_punch_out(True)
    assert result["ok"] is True


def test_nudge_up(tools, song):
    result = tools.nudge_up()
    assert result["ok"] is True
    song.nudge_up.assert_called_once()


def test_nudge_up_exception(tools, song):
    song.nudge_up.side_effect = Exception("err")
    result = tools.nudge_up()
    assert result["ok"] is False


def test_nudge_down(tools, song):
    result = tools.nudge_down()
    assert result["ok"] is True
    song.nudge_down.assert_called_once()


def test_nudge_down_exception(tools, song):
    song.nudge_down.side_effect = Exception("err")
    result = tools.nudge_down()
    assert result["ok"] is False
