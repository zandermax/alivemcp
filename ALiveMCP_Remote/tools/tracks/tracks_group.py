"""
Track grouping utilities (create/group/ungroup queries).
"""


class TracksGroupMixin:
    # ========================================================================
    # TRACK GROUPS
    # ========================================================================

    def create_group_track(self, name=None):
        """Create a new group track

        See Also:
            Wiki: docs/wiki/tools/create_group_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track_index = len(self.song.tracks)
            self.song.create_group_track(track_index)

            if name and track_index < len(self.song.tracks):
                self.song.tracks[track_index].name = str(name)

            return {
                "ok": True,
                "message": "Group track created",
                "track_index": track_index,
                "name": str(self.song.tracks[track_index].name)
                if track_index < len(self.song.tracks)
                else "",
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def group_tracks(self, start_index, end_index):
        """Group tracks from start_index to end_index (inclusive)

        See Also:
            Wiki: docs/wiki/tools/group_tracks.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if start_index < 0 or start_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid start index"}
            if end_index < start_index or end_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid end index"}

            self.song.create_group_track(end_index + 1)

            return {
                "ok": True,
                "message": "Tracks grouped",
                "start_index": start_index,
                "end_index": end_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_is_grouped(self, track_index):
        """Check if track is part of a group

        See Also:
            Wiki: docs/wiki/tools/get_track_is_grouped.md

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

            is_grouped = hasattr(track, "group_track") and track.group_track is not None
            is_foldable = hasattr(track, "is_foldable") and track.is_foldable

            result = {
                "ok": True,
                "track_index": track_index,
                "is_grouped": is_grouped,
                "is_group_track": is_foldable,
            }

            if is_grouped and hasattr(track, "group_track"):
                for i, t in enumerate(self.song.tracks):
                    if t == track.group_track:
                        result["group_track_index"] = i
                        break

            return result
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def ungroup_track(self, group_track_index):
        """Ungroup a group track

        See Also:
            Wiki: docs/wiki/tools/ungroup_track.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if group_track_index < 0 or group_track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[group_track_index]

            if not (hasattr(track, "is_foldable") and track.is_foldable):
                return {"ok": False, "error": "Track is not a group track"}

            return {
                "ok": True,
                "message": "Ungroup operation requested (may require manual implementation)",
                "group_track_index": group_track_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
