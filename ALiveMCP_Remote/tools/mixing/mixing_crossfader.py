"""
Crossfader operations for Mixing.

Single responsibility: track crossfader assignment and master crossfader position.
"""


class MixingCrossfaderMixin:
    def get_crossfader_assignment(self, track_index):
        """Get track crossfader assignment (0=None, 1=A, 2=B)

        See Also:
            Wiki: docs/wiki/tools/get_crossfader_assignment.md

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
            assignment_names = {0: "None", 1: "A", 2: "B"}

            if hasattr(track, "mixer_device") and hasattr(track.mixer_device, "crossfade_assign"):
                assignment = int(track.mixer_device.crossfade_assign)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "crossfader_assignment": assignment,
                    "assignment_name": assignment_names.get(assignment, "Unknown"),
                }
            else:
                return {"ok": False, "error": "Crossfader assignment not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_crossfader_assignment(self, track_index, assignment):
        """Set track crossfader assignment (0=None, 1=A, 2=B)

        See Also:
            Wiki: docs/wiki/tools/set_crossfader_assignment.md

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

            if hasattr(track, "mixer_device") and hasattr(track.mixer_device, "crossfade_assign"):
                track.mixer_device.crossfade_assign = int(max(0, min(2, assignment)))
                return {
                    "ok": True,
                    "track_index": track_index,
                    "crossfader_assignment": int(track.mixer_device.crossfade_assign),
                }
            else:
                return {"ok": False, "error": "Crossfader assignment not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_crossfader_position(self):
        """Get master crossfader position (-1.0 to 1.0)

        See Also:
            Wiki: docs/wiki/tools/get_crossfader_position.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            master = self.song.master_track
            if hasattr(master, "mixer_device") and hasattr(master.mixer_device, "crossfader"):
                return {"ok": True, "position": float(master.mixer_device.crossfader.value)}
            else:
                return {"ok": False, "error": "Crossfader not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
