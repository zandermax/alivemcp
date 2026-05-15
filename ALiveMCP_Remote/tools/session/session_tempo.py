"""
Session tempo and loop configuration mixin.
"""


class SessionTempoMixin:
    def set_tempo(self, bpm):
        """Set session tempo

        See Also:
            Wiki: docs/wiki/tools/set_tempo.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            bpm = float(bpm)
            if bpm < 20 or bpm > 999:
                return {"ok": False, "error": "BPM must be between 20 and 999"}
            self.song.tempo = bpm
            return {"ok": True, "message": "Tempo set", "bpm": float(self.song.tempo)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_time_signature(self, numerator, denominator):
        """Set time signature

        See Also:
            Wiki: docs/wiki/tools/set_time_signature.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            numerator = int(numerator)
            denominator = int(denominator)

            if numerator < 1 or numerator > 99:
                return {"ok": False, "error": "Numerator must be between 1 and 99"}
            if denominator not in [1, 2, 4, 8, 16]:
                return {"ok": False, "error": "Denominator must be 1, 2, 4, 8, or 16"}

            self.song.signature_numerator = numerator
            self.song.signature_denominator = denominator

            return {
                "ok": True,
                "message": "Time signature set",
                "numerator": self.song.signature_numerator,
                "denominator": self.song.signature_denominator,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_loop_start(self, position):
        """Set loop start position in beats

        See Also:
            Wiki: docs/wiki/tools/set_loop_start.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.loop_start = float(position)
            return {"ok": True, "loop_start": float(self.song.loop_start)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_loop_length(self, length):
        """Set loop length in beats

        See Also:
            Wiki: docs/wiki/tools/set_loop_length.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.loop_length = float(length)
            return {"ok": True, "loop_length": float(self.song.loop_length)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_metronome(self, enabled):
        """Enable or disable metronome

        See Also:
            Wiki: docs/wiki/tools/set_metronome.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.metronome = bool(enabled)
            return {"ok": True, "metronome": self.song.metronome}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def tap_tempo(self):
        """Tap tempo

        See Also:
            Wiki: docs/wiki/tools/tap_tempo.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.tap_tempo()
            return {"ok": True, "message": "Tempo tapped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
