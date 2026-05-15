"""
Clip looping helpers: enable/disable looping and loop boundaries.
"""


class ClipsLoopingMixin:
    # ========================================================================
    # CLIP LOOPING
    # ========================================================================

    def set_clip_looping(self, track_index, clip_index, looping):
        """Enable/disable clip looping

        See Also:
            Wiki: docs/wiki/tools/set_clip_looping.md

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
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.looping = bool(looping)
            return {"ok": True, "looping": clip.looping}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_loop_start(self, track_index, clip_index, loop_start):
        """Set clip loop start position

        See Also:
            Wiki: docs/wiki/tools/set_clip_loop_start.md

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
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.loop_start = float(loop_start)
            return {"ok": True, "loop_start": float(clip.loop_start)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_loop_end(self, track_index, clip_index, loop_end):
        """Set clip loop end position

        See Also:
            Wiki: docs/wiki/tools/set_clip_loop_end.md

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
            if clip_index < 0 or clip_index >= len(track.clip_slots):
                return {"ok": False, "error": "Invalid clip index"}

            clip_slot = track.clip_slots[clip_index]
            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip
            clip.loop_end = float(loop_end)
            return {"ok": True, "loop_end": float(clip.loop_end)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
