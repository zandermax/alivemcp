"""
Track management: create, delete, duplicate, rename tracks.
"""


class TracksManagementMixin:
    # ========================================================================
    # TRACK MANAGEMENT
    # ========================================================================

    def create_midi_track(self, name=None):
        """Create a new MIDI track

        See Also:
            Wiki: docs/wiki/tools/create_midi_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track_index = len(self.song.tracks)
            self.song.create_midi_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "MIDI track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_audio_track(self, name=None):
        """Create a new audio track

        See Also:
            Wiki: docs/wiki/tools/create_audio_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track_index = len(self.song.tracks)
            self.song.create_audio_track(track_index)

            if name:
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "Audio track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def create_return_track(self):
        """Create a new return track

        See Also:
            Wiki: docs/wiki/tools/create_return_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.create_return_track()
            return_index = len(self.song.return_tracks) - 1
            return {"ok": True, "message": "Return track created", "return_index": return_index}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_track(self, track_index):
        """Delete track by index

        See Also:
            Wiki: docs/wiki/tools/delete_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.delete_track(track_index)
            return {"ok": True, "message": "Track deleted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_track(self, track_index):
        """Duplicate track

        See Also:
            Wiki: docs/wiki/tools/duplicate_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.duplicate_track(track_index)
            return {"ok": True, "message": "Track duplicated", "new_index": track_index + 1}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def rename_track(self, track_index, name):
        """Rename track

        See Also:
            Wiki: docs/wiki/tools/rename_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].name = str(name)
            return {"ok": True, "message": "Track renamed", "name": str(name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
