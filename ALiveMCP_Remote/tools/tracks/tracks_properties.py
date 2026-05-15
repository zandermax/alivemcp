"""
Track property setters: volume, pan, arm/solo/mute, color.
"""


class TracksPropertiesMixin:
    # ========================================================================
    # TRACK PROPERTIES
    # ========================================================================

    def set_track_volume(self, track_index, volume):
        """Set track volume (0.0 to 1.0)

        See Also:
            Wiki: docs/wiki/tools/set_track_volume.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            volume = float(volume)
            if volume < 0.0 or volume > 1.0:
                return {"ok": False, "error": "Volume must be between 0.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.volume.value = volume

            return {
                "ok": True,
                "message": "Track volume set",
                "track_index": track_index,
                "volume": float(track.mixer_device.volume.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_pan(self, track_index, pan):
        """Set track pan (-1.0 to 1.0)

        See Also:
            Wiki: docs/wiki/tools/set_track_pan.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            pan = float(pan)
            if pan < -1.0 or pan > 1.0:
                return {"ok": False, "error": "Pan must be between -1.0 and 1.0"}

            track = self.song.tracks[track_index]
            track.mixer_device.panning.value = pan

            return {
                "ok": True,
                "message": "Track pan set",
                "track_index": track_index,
                "pan": float(track.mixer_device.panning.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def arm_track(self, track_index, armed=True):
        """Arm or disarm track for recording

        See Also:
            Wiki: docs/wiki/tools/arm_track.md

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
            if track.can_be_armed:
                track.arm = bool(armed)
                return {
                    "ok": True,
                    "message": "Track armed" if armed else "Track disarmed",
                    "armed": track.arm,
                }
            else:
                return {"ok": False, "error": "Track cannot be armed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def solo_track(self, track_index, solo=True):
        """Solo or unsolo track

        See Also:
            Wiki: docs/wiki/tools/solo_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].solo = bool(solo)
            return {"ok": True, "message": "Track soloed" if solo else "Track unsoloed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def mute_track(self, track_index, mute=True):
        """Mute or unmute track

        See Also:
            Wiki: docs/wiki/tools/mute_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            self.song.tracks[track_index].mute = bool(mute)
            return {"ok": True, "message": "Track muted" if mute else "Track unmuted"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_color(self, track_index, color_index):
        """Set track color

        See Also:
            Wiki: docs/wiki/tools/set_track_color.md

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
            if hasattr(track, "color"):
                track.color = int(color_index)
                return {"ok": True, "message": "Track color set", "color": track.color}
            else:
                return {"ok": False, "error": "Track color not supported"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
