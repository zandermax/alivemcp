"""
Clip follow actions mixin: get/set follow actions and follow-action time.
"""


class ClipsFollowActionsMixin:
    def get_clip_follow_action(self, track_index, clip_index):
        """Get clip follow action settings

        See Also:
            Wiki: docs/wiki/tools/get_clip_follow_action.md

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

            action_names = {
                0: "Stop",
                1: "Play Again",
                2: "Previous",
                3: "Next",
                4: "First",
                5: "Last",
                6: "Any",
                7: "Other",
                8: "Jump",
            }

            result = {"ok": True, "track_index": track_index, "clip_index": clip_index}

            if hasattr(clip, "follow_action_A"):
                result["follow_action_A"] = int(clip.follow_action_A)
                result["follow_action_A_name"] = action_names.get(
                    int(clip.follow_action_A), "Unknown"
                )

            if hasattr(clip, "follow_action_B"):
                result["follow_action_B"] = int(clip.follow_action_B)
                result["follow_action_B_name"] = action_names.get(
                    int(clip.follow_action_B), "Unknown"
                )

            if hasattr(clip, "follow_action_time"):
                result["follow_action_time"] = float(clip.follow_action_time)

            if hasattr(clip, "follow_action_chance_A"):
                result["follow_action_chance_A"] = float(clip.follow_action_chance_A)

            if hasattr(clip, "follow_action_chance_B"):
                result["follow_action_chance_B"] = float(clip.follow_action_chance_B)

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_clip_follow_action(self, track_index, clip_index, action_A, action_B, chance_A=1.0):
        """Set clip follow action (0-8: Stop, Play Again, Previous, Next, First, Last, Any, Other, Jump)

        See Also:
            Wiki: docs/wiki/tools/set_clip_follow_action.md

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

            if hasattr(clip, "follow_action_A"):
                clip.follow_action_A = int(max(0, min(8, action_A)))

            if hasattr(clip, "follow_action_B"):
                clip.follow_action_B = int(max(0, min(8, action_B)))

            if hasattr(clip, "follow_action_chance_A"):
                clip.follow_action_chance_A = float(max(0.0, min(1.0, chance_A)))

            if hasattr(clip, "follow_action_chance_B"):
                clip.follow_action_chance_B = 1.0 - float(max(0.0, min(1.0, chance_A)))

            return {
                "ok": True,
                "track_index": track_index,
                "clip_index": clip_index,
                "follow_action_A": int(clip.follow_action_A)
                if hasattr(clip, "follow_action_A")
                else None,
                "follow_action_B": int(clip.follow_action_B)
                if hasattr(clip, "follow_action_B")
                else None,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_follow_action_time(self, track_index, clip_index, time_in_bars):
        """Set follow action time in bars

        See Also:
            Wiki: docs/wiki/tools/set_follow_action_time.md

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

            if hasattr(clip, "follow_action_time"):
                clip.follow_action_time = float(max(0.0, time_in_bars))
                return {"ok": True, "follow_action_time": float(clip.follow_action_time)}
            else:
                return {"ok": False, "error": "Follow action time not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
