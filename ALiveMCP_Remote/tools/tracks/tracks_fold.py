"""
Track fold/unfold helpers.
"""


class TracksFoldMixin:
    # ========================================================================
    # FOLD STATE
    # ========================================================================

    def set_track_fold_state(self, track_index, folded):
        """Fold or unfold a group track

        See Also:
            Wiki: docs/wiki/tools/set_track_fold_state.md

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
            if track.is_foldable:
                track.fold_state = bool(folded)
                return {"ok": True, "fold_state": track.fold_state}
            else:
                return {"ok": False, "error": "Track is not foldable"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
