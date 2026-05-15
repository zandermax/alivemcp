"""
Track delay compensation helpers.
"""


class TracksDelayMixin:
    # ========================================================================
    # TRACK DELAY COMPENSATION
    # ========================================================================

    def get_track_delay(self, track_index):
        """Get track delay compensation in samples

        See Also:
            Wiki: docs/wiki/tools/get_track_delay.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "delay"):
                return {"ok": True, "delay": float(track.delay)}
            else:
                return {"ok": False, "error": "Track delay not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_delay(self, track_index, delay_samples):
        """Set track delay compensation in samples

        See Also:
            Wiki: docs/wiki/tools/set_track_delay.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "delay"):
                track.delay = float(delay_samples)
                return {"ok": True, "delay": float(track.delay)}
            else:
                return {"ok": False, "error": "Track delay not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
