"""
Arrangement locator and relative-jump tools.

Single responsibility: cue point (locator) creation, deletion, listing, and
relative time-position jumps.
"""


class ArrangementLocatorsMixin:
    # ========================================================================
    # LOCATOR / CUE POINT OPERATIONS
    # ========================================================================

    def create_locator(self, time_in_beats, name="Locator"):
        """Create a locator/cue point at specified time

        See Also:
            Wiki: docs/wiki/tools/create_locator.md"""
        try:
            if hasattr(self.song, "create_cue_point"):
                self.song.create_cue_point(float(time_in_beats))
                return {
                    "ok": True,
                    "message": "Cue point created",
                    "time": float(time_in_beats),
                    "name": name,
                }
            else:
                return {
                    "ok": False,
                    "error": "Cue point creation not available in this Ableton version",
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def delete_locator(self, locator_index):
        """Delete a locator/cue point

        See Also:
            Wiki: docs/wiki/tools/delete_locator.md"""
        try:
            if hasattr(self.song, "cue_points"):
                if locator_index < 0 or locator_index >= len(self.song.cue_points):
                    return {"ok": False, "error": "Invalid locator index"}
                cue_point = self.song.cue_points[locator_index]
                if hasattr(cue_point, "delete"):
                    cue_point.delete()
                    return {
                        "ok": True,
                        "message": "Locator deleted",
                        "locator_index": locator_index,
                    }
            return {"ok": False, "error": "Cue points not available in this Ableton version"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_locators(self):
        """Get all locators/cue points

        See Also:
            Wiki: docs/wiki/tools/get_locators.md"""
        try:
            if hasattr(self.song, "cue_points"):
                locators = []
                for i, cue in enumerate(self.song.cue_points):
                    locators.append(
                        {
                            "index": i,
                            "time": float(cue.time) if hasattr(cue, "time") else 0.0,
                            "name": str(cue.name) if hasattr(cue, "name") else "",
                        }
                    )
                return {"ok": True, "locators": locators, "count": len(locators)}
            else:
                return {"ok": True, "locators": [], "count": 0}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_by_amount(self, amount_in_beats):
        """Jump playback position by specified amount (positive or negative)

        See Also:
            Wiki: docs/wiki/tools/jump_by_amount.md"""
        try:
            current_time = self.song.current_song_time
            new_time = float(current_time) + float(amount_in_beats)
            new_time = max(0.0, new_time)
            self.song.current_song_time = new_time
            return {
                "ok": True,
                "old_time": float(current_time),
                "new_time": float(self.song.current_song_time),
                "jumped_by": float(amount_in_beats),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
