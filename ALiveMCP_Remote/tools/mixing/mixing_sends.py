"""
Send operations for Mixing.

Single responsibility: operations for track sends.
"""


class MixingSendsMixin:
    def set_track_send(self, track_index, send_index, value):
        """Set track send level

        See Also:
            Wiki: docs/wiki/tools/set_track_send.md

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
            sends = track.mixer_device.sends

            if send_index < 0 or send_index >= len(sends):
                return {"ok": False, "error": "Invalid send index"}

            sends[send_index].value = float(value)
            return {"ok": True, "send_index": send_index, "value": float(sends[send_index].value)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_sends(self, track_index):
        """Get all send levels for track

        See Also:
            Wiki: docs/wiki/tools/get_track_sends.md

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
            sends = []

            for i, send in enumerate(track.mixer_device.sends):
                sends.append(
                    {
                        "index": i,
                        "value": float(send.value),
                        "name": str(send.name) if hasattr(send, "name") else "Send " + chr(65 + i),
                    }
                )

            return {"ok": True, "track_index": track_index, "sends": sends, "count": len(sends)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
