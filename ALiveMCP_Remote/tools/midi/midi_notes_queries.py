"""
MIDI note query mixin: extended note queries.
"""


class MidiNotesQueriesMixin:
    def get_notes_extended(
        self, track_index, clip_index, start_time, time_span, start_pitch, pitch_span
    ):
        """Get notes with extended filtering options

        See Also:
            Wiki: docs/wiki/tools/get_notes_extended.md

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
            notes_data = clip.get_notes_extended(
                from_time=float(start_time),
                from_pitch=int(start_pitch),
                time_span=float(time_span),
                pitch_span=int(pitch_span),
            )

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

            return {"ok": True, "notes": notes, "count": len(notes)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
