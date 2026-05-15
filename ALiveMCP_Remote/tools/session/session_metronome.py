"""
Session metronome volume mixin.
"""


class SessionMetronomeMixin:
    def get_metronome_volume(self):
        """Get metronome volume

        See Also:
            Wiki: docs/wiki/tools/get_metronome_volume.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if hasattr(self.song, "metronome"):
                return {"ok": True, "volume": float(self.song.metronome)}
            else:
                return {"ok": False, "error": "Metronome volume not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_metronome_volume(self, volume):
        """Set metronome volume (0.0 to 1.0)"""
        try:
            if hasattr(self.song, "metronome"):
                self.song.metronome = float(volume)
                return {"ok": True, "volume": float(self.song.metronome)}
            else:
                return {"ok": False, "error": "Metronome volume not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
