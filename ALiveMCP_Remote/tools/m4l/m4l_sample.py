"""
Sample/Simpler utilities: sample length and playback mode.
"""


class M4LSampleMixin:
    # ========================================================================
    # SAMPLE/SIMPLER OPERATIONS
    # ========================================================================

    def get_sample_length(self, track_index, clip_index):
        """Get audio sample length for a clip

        See Also:
            Wiki: docs/wiki/tools/get_sample_length.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "sample_length"):
                return {"ok": True, "sample_length": float(clip.sample_length)}
            else:
                return {"ok": False, "error": "Sample length not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_sample_playback_mode(self, track_index, device_index):
        """Get Simpler/Sampler playback mode

        See Also:
            Wiki: docs/wiki/tools/get_sample_playback_mode.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "playback_mode"):
                return {"ok": True, "playback_mode": int(device.playback_mode)}
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_sample_playback_mode(self, track_index, device_index, mode):
        """Set Simpler/Sampler playback mode

        See Also:
            Wiki: docs/wiki/tools/set_sample_playback_mode.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "playback_mode"):
                device.playback_mode = int(mode)
                return {"ok": True, "playback_mode": int(device.playback_mode)}
            else:
                return {"ok": False, "error": "Playback mode not available (Simpler/Sampler only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
