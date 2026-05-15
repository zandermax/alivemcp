"""
MIDI note operation mixin: add, get, remove notes.
"""


class MidiNotesOperationsMixin:
    # ========================================================================
    # MIDI NOTE OPERATIONS
    # ========================================================================

    def add_notes(self, track_index, clip_index, notes):
        """Add MIDI notes to a clip

        See Also:
            Wiki: docs/wiki/tools/add_notes.md

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
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid scene/clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_midi_clip:
                return {"ok": False, "error": "Clip is not a MIDI clip"}

            for note in notes:
                pitch = int(note.get("pitch", 60))
                start = float(note.get("start", 0.0))
                duration = float(note.get("duration", 1.0))
                velocity = int(note.get("velocity", 100))

                if pitch < 0 or pitch > 127:
                    continue
                if velocity < 0 or velocity > 127:
                    continue
                if duration <= 0:
                    continue

                clip.set_notes(((pitch, start, duration, velocity, False),))

            return {
                "ok": True,
                "message": "Notes added",
                "track_index": track_index,
                "clip_index": clip_index,
                "note_count": len(notes),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_notes(self, track_index, clip_index):
        """Get all MIDI notes from a clip

        See Also:
            Wiki: docs/wiki/tools/get_clip_notes.md

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
            if not track.has_midi_input:
                return {"ok": False, "error": "Track is not a MIDI track"}

            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            if not clip.is_midi_clip:
                return {"ok": False, "error": "Clip is not a MIDI clip"}

            notes_data = clip.get_notes(0, 0, clip.length, 128)

            notes = []
            for note_tuple in notes_data:
                notes.append(
                    {
                        "pitch": note_tuple[0],
                        "start_time": float(note_tuple[1]),
                        "duration": float(note_tuple[2]),
                        "velocity": note_tuple[3],
                        "muted": note_tuple[4],
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "clip_index": clip_index,
                "notes": notes,
                "count": len(notes),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def remove_notes(
        self, track_index, clip_index, pitch_from=0, pitch_to=127, time_from=0.0, time_to=999.0
    ):
        """Remove MIDI notes from clip

        See Also:
            Wiki: docs/wiki/tools/remove_notes.md

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
            clip.remove_notes(
                float(time_from),
                int(pitch_from),
                float(time_to - time_from),
                int(pitch_to - pitch_from),
            )
            return {"ok": True, "message": "Notes removed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
