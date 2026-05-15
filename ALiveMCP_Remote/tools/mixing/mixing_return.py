"""
Return track operations for Mixing.

Single responsibility: return-track queries and controls.
"""


class MixingReturnMixin:
    def get_return_track_count(self):
        """Get number of return tracks

        See Also:
            Wiki: docs/wiki/tools/get_return_track_count.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            return {"ok": True, "count": len(self.song.return_tracks)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_return_track_info(self, return_index):
        """Get return track information

        See Also:
            Wiki: docs/wiki/tools/get_return_track_info.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if return_index < 0 or return_index >= len(self.song.return_tracks):
                return {"ok": False, "error": "Invalid return track index"}

            return_track = self.song.return_tracks[return_index]

            info = {
                "ok": True,
                "index": return_index,
                "name": str(return_track.name),
                "volume": float(return_track.mixer_device.volume.value),
                "pan": float(return_track.mixer_device.panning.value),
                "mute": return_track.mute,
                "solo": return_track.solo,
                "num_devices": len(return_track.devices),
            }

            return info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_return_track_volume(self, return_index, volume):
        """Set return track volume

        See Also:
            Wiki: docs/wiki/tools/set_return_track_volume.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if return_index < 0 or return_index >= len(self.song.return_tracks):
                return {"ok": False, "error": "Invalid return track index"}

            return_track = self.song.return_tracks[return_index]
            return_track.mixer_device.volume.value = float(max(0.0, min(1.0, volume)))

            return {
                "ok": True,
                "return_index": return_index,
                "volume": float(return_track.mixer_device.volume.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
