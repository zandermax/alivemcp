"""
Track information helpers: get info, lookup index by name, get color.
"""


class TracksInfoMixin:
    # ========================================================================
    # TRACK INFO
    # ========================================================================

    def get_track_info(self, track_index):
        """Get detailed track information

        See Also:
            Wiki: docs/wiki/tools/get_track_info.md

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
            return {
                "ok": True,
                "track_index": track_index,
                "name": str(track.name),
                "color": track.color if hasattr(track, "color") else None,
                "is_foldable": track.is_foldable,
                "mute": track.mute,
                "solo": track.solo,
                "arm": track.arm if track.can_be_armed else False,
                "has_midi_input": track.has_midi_input,
                "has_audio_input": track.has_audio_input,
                "volume": float(track.mixer_device.volume.value),
                "pan": float(track.mixer_device.panning.value),
                "num_devices": len(track.devices),
                "num_clips": len([cs for cs in track.clip_slots if cs.has_clip]),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_index_by_name(self, name):
        """Find a track's index by name (case-insensitive, partial match, first result)

        See Also:
            Wiki: docs/wiki/tools/get_track_index_by_name.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            needle = name.lower()
            for i, track in enumerate(self.song.tracks):
                if needle in str(track.name).lower():
                    return {"ok": True, "track_index": i, "name": str(track.name)}
            return {"ok": False, "error": "No track matching '" + name + "' found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_color(self, track_index):
        """Get track color

        See Also:
            Wiki: docs/wiki/tools/get_track_color.md

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

            if hasattr(track, "color_index"):
                return {
                    "ok": True,
                    "track_index": track_index,
                    "color_index": int(track.color_index),
                }
            elif hasattr(track, "color"):
                return {"ok": True, "track_index": track_index, "color": int(track.color)}
            else:
                return {"ok": False, "error": "Track color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
