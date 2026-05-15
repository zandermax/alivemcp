"""
Clip extras: annotations, fades, RAM mode, and follow actions.
"""


class ClipsExtrasMixin:
    # ========================================================================
    # CLIP ANNOTATIONS
    # ========================================================================

    def get_clip_annotation(self, track_index, clip_index):
        """Get clip annotation text

        See Also:
            Wiki: docs/wiki/tools/get_clip_annotation.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "annotation"):
                return {"ok": True, "annotation": str(clip.annotation)}
            else:
                return {"ok": False, "error": "Clip annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_annotation(self, track_index, clip_index, annotation_text):
        """Set clip annotation text

        See Also:
            Wiki: docs/wiki/tools/set_clip_annotation.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "annotation"):
                clip.annotation = str(annotation_text)
                return {"ok": True, "annotation": str(clip.annotation)}
            else:
                return {"ok": False, "error": "Clip annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP FADE IN/OUT
    # ========================================================================

    def get_clip_fade_in(self, track_index, clip_index):
        """Get clip fade in time

        See Also:
            Wiki: docs/wiki/tools/get_clip_fade_in.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_in_time"):
                return {"ok": True, "fade_in_time": float(clip.fade_in_time)}
            else:
                return {"ok": False, "error": "Fade in not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_fade_in(self, track_index, clip_index, fade_time):
        """Set clip fade in time

        See Also:
            Wiki: docs/wiki/tools/set_clip_fade_in.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_in_time"):
                clip.fade_in_time = float(fade_time)
                return {"ok": True, "fade_in_time": float(clip.fade_in_time)}
            else:
                return {"ok": False, "error": "Fade in not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_clip_fade_out(self, track_index, clip_index):
        """Get clip fade out time

        See Also:
            Wiki: docs/wiki/tools/get_clip_fade_out.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_out_time"):
                return {"ok": True, "fade_out_time": float(clip.fade_out_time)}
            else:
                return {"ok": False, "error": "Fade out not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_fade_out(self, track_index, clip_index, fade_time):
        """Set clip fade out time

        See Also:
            Wiki: docs/wiki/tools/set_clip_fade_out.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "fade_out_time"):
                clip.fade_out_time = float(fade_time)
                return {"ok": True, "fade_out_time": float(clip.fade_out_time)}
            else:
                return {"ok": False, "error": "Fade out not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # CLIP RAM MODE
    # ========================================================================

    def get_clip_ram_mode(self, track_index, clip_index):
        """Get clip RAM mode setting

        See Also:
            Wiki: docs/wiki/tools/get_clip_ram_mode.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "ram_mode"):
                return {"ok": True, "ram_mode": bool(clip.ram_mode)}
            else:
                return {"ok": False, "error": "RAM mode not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_ram_mode(self, track_index, clip_index, ram_mode):
        """Set clip RAM mode (load into RAM vs stream from disk)

        See Also:
            Wiki: docs/wiki/tools/set_clip_ram_mode.md"""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "ram_mode"):
                clip.ram_mode = bool(ram_mode)
                return {"ok": True, "ram_mode": bool(clip.ram_mode)}
            else:
                return {"ok": False, "error": "RAM mode not available (audio clips only)"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # Follow actions were moved to `ClipsFollowActionsMixin`
    # See: ALiveMCP_Remote/tools/clips/clips_follow_actions.py
