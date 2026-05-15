"""
Groove and groove pool operations.

Single responsibility: clip groove amount and song-level groove settings.
Quantize operations live in clips_properties.py.
"""


class MixingGrooveMixin:
    # ========================================================================
    # GROOVE & GROOVE POOL
    # ========================================================================

    def set_clip_groove_amount(self, track_index, clip_index, amount):
        """Set clip groove amount (0.0-1.0)

        See Also:
            Wiki: docs/wiki/tools/set_clip_groove_amount.md"""
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
            if hasattr(clip, "groove_amount"):
                clip.groove_amount = float(amount)
                return {"ok": True, "groove_amount": float(clip.groove_amount)}
            else:
                return {"ok": False, "error": "Clip does not support groove"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_groove_amount(self):
        """Get song groove amount

        See Also:
            Wiki: docs/wiki/tools/get_groove_amount.md"""
        try:
            if hasattr(self.song, "groove_amount"):
                return {"ok": True, "groove_amount": float(self.song.groove_amount)}
            else:
                return {"ok": False, "error": "Song does not support groove_amount"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_groove_amount(self, amount):
        """Set song groove amount (0.0-1.0)

        See Also:
            Wiki: docs/wiki/tools/set_groove_amount.md"""
        try:
            if hasattr(self.song, "groove_amount"):
                self.song.groove_amount = float(amount)
                return {"ok": True, "groove_amount": float(self.song.groove_amount)}
            else:
                return {"ok": False, "error": "Song does not support groove_amount"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # GROOVE POOL
    # ========================================================================

    def get_groove_pool_grooves(self):
        """Get list of grooves in groove pool

        See Also:
            Wiki: docs/wiki/tools/get_groove_pool_grooves.md"""
        try:
            grooves = []

            if hasattr(self.song, "groove_pool"):
                for i, groove in enumerate(self.song.groove_pool):
                    groove_info = {
                        "index": i,
                        "name": str(groove.name) if hasattr(groove, "name") else f"Groove {i}",
                    }

                    if hasattr(groove, "timing_amount"):
                        groove_info["timing_amount"] = float(groove.timing_amount)
                    if hasattr(groove, "random_amount"):
                        groove_info["random_amount"] = float(groove.random_amount)
                    if hasattr(groove, "velocity_amount"):
                        groove_info["velocity_amount"] = float(groove.velocity_amount)

                    grooves.append(groove_info)

            return {"ok": True, "grooves": grooves, "count": len(grooves)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_groove(self, track_index, clip_index, groove_index):
        """Set groove for clip

        See Also:
            Wiki: docs/wiki/tools/set_clip_groove.md"""
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

            if (
                hasattr(self.song, "groove_pool")
                and groove_index >= 0
                and groove_index < len(self.song.groove_pool)
            ):
                if hasattr(clip, "groove"):
                    clip.groove = self.song.groove_pool[groove_index]
                    return {"ok": True, "message": "Groove set", "groove_index": groove_index}
                else:
                    return {"ok": False, "error": "Clip groove property not available"}
            else:
                return {"ok": False, "error": "Invalid groove index"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
