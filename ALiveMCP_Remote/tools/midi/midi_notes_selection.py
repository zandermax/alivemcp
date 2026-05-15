"""
MIDI note selection mixin: select/deselect and replace selected notes.
"""


class MidiNotesSelectionMixin:
    def select_all_notes(self, track_index, clip_index):
        """Select all notes in clip

        See Also:
            Wiki: docs/wiki/tools/select_all_notes.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            clip.select_all_notes()
            return {"ok": True, "message": "All notes selected"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def deselect_all_notes(self, track_index, clip_index):
        """Deselect all notes in clip

        See Also:
            Wiki: docs/wiki/tools/deselect_all_notes.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip
            clip.deselect_all_notes()
            return {"ok": True, "message": "All notes deselected"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def replace_selected_notes(self, track_index, clip_index, notes):
        """Replace selected notes with new notes

        See Also:
            Wiki: docs/wiki/tools/replace_selected_notes.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip or not clip_slot.clip.is_midi_clip:
                return {"ok": False, "error": "No MIDI clip in slot"}

            clip = clip_slot.clip

            note_tuples = []
            for note in notes:
                pitch = int(note.get("pitch", 60))
                start = float(note.get("start", 0.0))
                duration = float(note.get("duration", 1.0))
                velocity = int(note.get("velocity", 100))
                muted = bool(note.get("muted", False))
                note_tuples.append((pitch, start, duration, velocity, muted))

            clip.replace_selected_notes(tuple(note_tuples))
            return {"ok": True, "message": "Selected notes replaced", "note_count": len(notes)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
