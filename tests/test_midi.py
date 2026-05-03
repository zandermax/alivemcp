"""
Tests for MidiMixin core note operations.
"""

from unittest.mock import MagicMock


def _midi_song(has_clip=True, is_midi=True):
    clip = MagicMock()
    clip.is_midi_clip = is_midi
    clip.get_notes.return_value = ((60, 0.0, 1.0, 100, False),)

    clip_slot = MagicMock()
    clip_slot.has_clip = has_clip
    clip_slot.clip = clip

    track = MagicMock()
    track.has_midi_input = is_midi
    track.clip_slots = [clip_slot]

    s = MagicMock()
    s.tracks = [track]
    s.scenes = [MagicMock()]
    return s


def test_add_notes_success(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    notes = [{"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 100}]
    result = tools.add_notes(0, 0, notes)
    assert result["ok"] is True
    assert result["note_count"] == 1


def test_add_notes_invalid_track(tools):
    result = tools.add_notes(-1, 0, [])
    assert result["ok"] is False


def test_add_notes_not_midi_track(tools, song):
    song.tracks[0].has_midi_input = False
    result = tools.add_notes(0, 0, [])
    assert result == {"ok": False, "error": "Track is not a MIDI track"}


def test_add_notes_invalid_scene(tools, song):
    song.tracks[0].has_midi_input = True
    result = tools.add_notes(0, 99, [])
    assert result["ok"] is False


def test_add_notes_no_clip(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.add_notes(0, 0, [])
    assert result["ok"] is False


def test_add_notes_not_midi_clip(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = False
    result = tools.add_notes(0, 0, [{"pitch": 60, "start": 0, "duration": 1, "velocity": 100}])
    assert result == {"ok": False, "error": "Clip is not a MIDI clip"}


def test_add_notes_filters_invalid_pitch(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    notes = [
        {"pitch": 200, "start": 0.0, "duration": 1.0, "velocity": 100},
        {"pitch": 60, "start": 0.0, "duration": -1.0, "velocity": 100},
        {"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 200},
        {"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 80},
    ]
    result = tools.add_notes(0, 0, notes)
    assert result["ok"] is True
    assert result["note_count"] == 4


def test_add_notes_exception(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    song.tracks[0].clip_slots[0].clip.set_notes.side_effect = Exception("err")
    notes = [{"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 100}]
    result = tools.add_notes(0, 0, notes)
    assert result["ok"] is False


def test_get_clip_notes_success(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    song.tracks[0].clip_slots[0].clip.get_notes.return_value = ((60, 0.0, 1.0, 100, False),)
    result = tools.get_clip_notes(0, 0)
    assert result["ok"] is True
    assert result["count"] == 1
    assert result["notes"][0]["pitch"] == 60


def test_get_clip_notes_invalid_track(tools):
    result = tools.get_clip_notes(-1, 0)
    assert result["ok"] is False


def test_get_clip_notes_not_midi_track(tools, song):
    song.tracks[0].has_midi_input = False
    result = tools.get_clip_notes(0, 0)
    assert result["ok"] is False


def test_get_clip_notes_no_clip(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_clip_notes(0, 0)
    assert result["ok"] is False


def test_get_clip_notes_not_midi_clip(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = False
    result = tools.get_clip_notes(0, 0)
    assert result["ok"] is False


def test_get_clip_notes_exception(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    song.tracks[0].clip_slots[0].clip.get_notes.side_effect = Exception("err")
    result = tools.get_clip_notes(0, 0)
    assert result["ok"] is False


def _setup_midi_clip(song):
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True


def test_remove_notes_success(tools, song):
    _setup_midi_clip(song)
    result = tools.remove_notes(0, 0)
    assert result["ok"] is True
    song.tracks[0].clip_slots[0].clip.remove_notes.assert_called_once()


def test_remove_notes_invalid_track(tools):
    result = tools.remove_notes(-1, 0)
    assert result["ok"] is False


def test_remove_notes_no_midi_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.remove_notes(0, 0)
    assert result["ok"] is False


def test_remove_notes_exception(tools, song):
    _setup_midi_clip(song)
    song.tracks[0].clip_slots[0].clip.remove_notes.side_effect = Exception("err")
    result = tools.remove_notes(0, 0)
    assert result["ok"] is False


def test_select_all_notes_success(tools, song):
    _setup_midi_clip(song)
    result = tools.select_all_notes(0, 0)
    assert result["ok"] is True
    song.tracks[0].clip_slots[0].clip.select_all_notes.assert_called_once()


def test_select_all_notes_invalid(tools):
    result = tools.select_all_notes(-1, 0)
    assert result["ok"] is False


def test_select_all_notes_no_midi_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.select_all_notes(0, 0)
    assert result["ok"] is False


def test_select_all_notes_exception(tools, song):
    _setup_midi_clip(song)
    song.tracks[0].clip_slots[0].clip.select_all_notes.side_effect = Exception("err")
    result = tools.select_all_notes(0, 0)
    assert result["ok"] is False


def test_deselect_all_notes_success(tools, song):
    _setup_midi_clip(song)
    result = tools.deselect_all_notes(0, 0)
    assert result["ok"] is True


def test_deselect_all_notes_invalid(tools):
    result = tools.deselect_all_notes(-1, 0)
    assert result["ok"] is False


def test_deselect_all_notes_no_midi_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.deselect_all_notes(0, 0)
    assert result["ok"] is False


def test_deselect_all_notes_exception(tools, song):
    _setup_midi_clip(song)
    song.tracks[0].clip_slots[0].clip.deselect_all_notes.side_effect = Exception("err")
    result = tools.deselect_all_notes(0, 0)
    assert result["ok"] is False


def test_get_clip_notes_invalid_clip(tools, song):
    result = tools.get_clip_notes(0, 99)
    assert result["ok"] is False


def test_remove_notes_invalid_clip(tools, song):
    result = tools.remove_notes(0, 99)
    assert result["ok"] is False


def test_select_all_notes_invalid_clip(tools, song):
    result = tools.select_all_notes(0, 99)
    assert result["ok"] is False


def test_deselect_all_notes_invalid_clip(tools, song):
    result = tools.deselect_all_notes(0, 99)
    assert result["ok"] is False
