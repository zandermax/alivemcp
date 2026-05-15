"""
Track annotation getters/setters.
"""


class TracksAnnotationsMixin:
    # ========================================================================
    # TRACK ANNOTATIONS
    # ========================================================================

    def get_track_annotation(self, track_index):
        """Get track annotation text

        See Also:
            Wiki: docs/wiki/tools/get_track_annotation.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "annotation"):
                return {"ok": True, "annotation": str(track.annotation)}
            else:
                return {"ok": False, "error": "Track annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_annotation(self, track_index, annotation_text):
        """Set track annotation text

        See Also:
            Wiki: docs/wiki/tools/set_track_annotation.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "annotation"):
                track.annotation = str(annotation_text)
                return {"ok": True, "annotation": str(track.annotation)}
            else:
                return {"ok": False, "error": "Track annotation not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
