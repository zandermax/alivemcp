"""
Clip color helpers mixin.
"""


class ClipsColorMixin:
    def get_clip_color(self, track_index, clip_index):
        """Get clip color

        See Also:
            Wiki: docs/wiki/tools/get_clip_color.md"""
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

            if hasattr(clip, "color_index"):
                return {"ok": True, "color_index": int(clip.color_index)}
            elif hasattr(clip, "color"):
                return {"ok": True, "color": int(clip.color)}
            else:
                return {"ok": False, "error": "Clip color not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_color(self, track_index, clip_index, color_index):
        """Set clip color

        See Also:
            Wiki: docs/wiki/tools/set_clip_color.md"""
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

            if hasattr(clip, "color_index"):
                clip.color_index = int(color_index)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "color_index": int(color_index),
                }
            elif hasattr(clip, "color"):
                clip.color = int(color_index)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "clip_index": clip_index,
                    "color": int(color_index),
                }
            else:
                return {"ok": False, "error": "Clip color not available in this Ableton version"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
