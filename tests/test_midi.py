"""
Tests for MidiMixin: add/get/remove notes, note selection, CC, and program change.
"""

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# add_notes
# ---------------------------------------------------------------------------


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
        {"pitch": 200, "start": 0.0, "duration": 1.0, "velocity": 100},  # invalid pitch
        {"pitch": 60, "start": 0.0, "duration": -1.0, "velocity": 100},  # invalid duration
        {"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 200},  # invalid velocity
        {"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 80},  # valid
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


# ---------------------------------------------------------------------------
# get_clip_notes
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# remove_notes
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# select_all_notes / deselect_all_notes
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# replace_selected_notes
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# get_notes_extended
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# send_midi_cc
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# send_program_change
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Additional coverage: invalid clip index branches
# ---------------------------------------------------------------------------


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


def test_replace_selected_notes_invalid_clip(tools, song):
    result = tools.replace_selected_notes(0, 99, [])
    assert result["ok"] is False


def test_get_notes_extended_invalid_clip(tools, song):
    result = tools.get_notes_extended(0, 99, 0, 4, 0, 128)
    assert result["ok"] is False


# ---------------------------------------------------------------------------
# Keyword-arg test: lock in clip_index as the canonical parameter for add_notes
# ---------------------------------------------------------------------------


def test_add_notes_keyword_clip_index(tools, song):
    song.tracks[0].has_midi_input = True
    song.tracks[0].clip_slots[0].has_clip = True
    song.tracks[0].clip_slots[0].clip.is_midi_clip = True
    notes = [{"pitch": 64, "start": 0.0, "duration": 0.5, "velocity": 90}]
    result = tools.add_notes(track_index=0, clip_index=0, notes=notes)
    assert result["ok"] is True
    assert result["clip_index"] == 0
