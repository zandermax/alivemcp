"""
Clip marker helpers: start/end markers.
"""


class ClipsMarkersMixin:
    # ========================================================================
    # CLIP MARKERS
    # ========================================================================

    def set_clip_start_marker(self, track_index, clip_index, start_marker):
        """Set clip start marker

        See Also:
            Wiki: docs/wiki/tools/set_clip_start_marker.md

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
            clip.start_marker = float(start_marker)
            return {"ok": True, "start_marker": float(clip.start_marker)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_end_marker(self, track_index, clip_index, end_marker):
        """Set clip end marker

        See Also:
            Wiki: docs/wiki/tools/set_clip_end_marker.md

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
            clip.end_marker = float(end_marker)
            return {"ok": True, "end_marker": float(clip.end_marker)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
