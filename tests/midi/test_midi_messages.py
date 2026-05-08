"""
Tests for MidiMixin raw MIDI message methods.
"""


def test_send_midi_cc_with_send_midi(tools, song):
    result = tools.send_midi_cc(0, 7, 100, channel=0)
    assert result["ok"] is True
    song.send_midi.assert_called_once_with((176, 7, 100))


def test_send_midi_cc_without_send_midi(tools, song):
    del song.send_midi
    result = tools.send_midi_cc(0, 7, 100)
    assert result == {"ok": False, "error": "send_midi not available"}


def test_send_midi_cc_exception(tools):
    result = tools.send_midi_cc(0, "bad", 100)
    assert result["ok"] is False


def test_send_program_change_with_send_midi(tools, song):
    result = tools.send_program_change(0, 5, channel=0)
    assert result["ok"] is True
    song.send_midi.assert_called_once_with((192, 5))


def test_send_program_change_without_send_midi(tools, song):
    del song.send_midi
    result = tools.send_program_change(0, 5)
    assert result == {"ok": False, "error": "send_midi not available"}


def test_send_program_change_exception(tools):
    result = tools.send_program_change(0, "bad")
    assert result["ok"] is False
