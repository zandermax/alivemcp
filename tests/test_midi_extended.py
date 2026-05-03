"""
Tests for MidiMixin extended note operations and alias coverage.
"""


def _setup_midi_clip(song):
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True


def test_replace_selected_notes_success(tools, song):
    _setup_midi_clip(song)
    notes = [{"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 100, "muted": False}]
    result = tools.replace_selected_notes(0, 0, notes)
    assert result["ok"] is True
    assert result["note_count"] == 1


def test_replace_selected_notes_invalid(tools):
    result = tools.replace_selected_notes(-1, 0, [])
    assert result["ok"] is False


def test_replace_selected_notes_no_midi_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.replace_selected_notes(0, 0, [])
    assert result["ok"] is False


def test_replace_selected_notes_exception(tools, song):
    _setup_midi_clip(song)
    song.tracks[0].clip_slots[0].clip.replace_selected_notes.side_effect = Exception("err")
    result = tools.replace_selected_notes(0, 0, [{"pitch": 60, "start": 0, "duration": 1}])
    assert result["ok"] is False


def test_get_notes_extended_success(tools, song):
    _setup_midi_clip(song)
    song.tracks[0].clip_slots[0].clip.get_notes_extended.return_value = (
        (60, 0.0, 1.0, 100, False),
    )
    result = tools.get_notes_extended(0, 0, 0.0, 4.0, 0, 128)
    assert result["ok"] is True
    assert result["count"] == 1


def test_get_notes_extended_invalid(tools):
    result = tools.get_notes_extended(-1, 0, 0, 4, 0, 128)
    assert result["ok"] is False


def test_get_notes_extended_no_midi_clip(tools, song):
    song.tracks[0].clip_slots[0].has_clip = False
    result = tools.get_notes_extended(0, 0, 0, 4, 0, 128)
    assert result["ok"] is False


def test_get_notes_extended_exception(tools, song):
    _setup_midi_clip(song)
    song.tracks[0].clip_slots[0].clip.get_notes_extended.side_effect = Exception("err")
    result = tools.get_notes_extended(0, 0, 0, 4, 0, 128)
    assert result["ok"] is False


def test_replace_selected_notes_invalid_clip(tools, song):
    result = tools.replace_selected_notes(0, 99, [])
    assert result["ok"] is False


def test_get_notes_extended_invalid_clip(tools, song):
    result = tools.get_notes_extended(0, 99, 0, 4, 0, 128)
    assert result["ok"] is False


def test_add_notes_keyword_clip_index(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    notes = [{"pitch": 64, "start": 0.0, "duration": 0.5, "velocity": 90}]
    result = tools.add_notes(track_index=0, clip_index=0, notes=notes)
    assert result["ok"] is True
    assert result["clip_index"] == 0
