"""
Track freeze/flatten utilities.
"""


class TracksFreezeMixin:
    # ========================================================================
    # TRACK FREEZE/FLATTEN
    # ========================================================================

    def freeze_track(self, track_index):
        """Freeze a track to reduce CPU usage

        See Also:
            Wiki: docs/wiki/tools/freeze_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "freeze_available") and track.freeze_available:
                if hasattr(track, "freeze_state"):
                    track.freeze_state = 1
                    return {"ok": True, "track_index": track_index, "frozen": True}
                else:
                    return {"ok": False, "error": "Freeze state not available"}
            else:
                return {"ok": False, "error": "Track cannot be frozen"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def unfreeze_track(self, track_index):
        """Unfreeze a frozen track

        See Also:
            Wiki: docs/wiki/tools/unfreeze_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "freeze_state"):
                track.freeze_state = 0
                return {"ok": True, "track_index": track_index, "frozen": False}
            else:
                return {"ok": False, "error": "Freeze state not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def flatten_track(self, track_index):
        """Flatten a frozen track (converts to audio)

        See Also:
            Wiki: docs/wiki/tools/flatten_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "flatten"):
                track.flatten()
                return {"ok": True, "track_index": track_index, "message": "Track flattened"}
            else:
                return {"ok": False, "error": "Flatten not available (track must be frozen first)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
