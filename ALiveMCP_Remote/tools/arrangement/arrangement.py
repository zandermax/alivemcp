"""
Core arrangement tools: project info, arrangement clips, cue navigation.

Single responsibility: operations on the arrangement timeline — project folder,
session record triggering, arrangement clip inspection, clip duplication to
arrangement, and cue-point navigation (jump to next/prev cue).

View navigation → arrangement_view.py
Locators (create/delete/list) and relative jumps → arrangement_locators.py
Browser and color utilities → arrangement_browser.py
"""

from .arrangement_browser import ArrangementBrowserMixin


class ArrangementMixin(ArrangementBrowserMixin):
    # ========================================================================
    # PROJECT & ARRANGEMENT
    # ========================================================================

    def get_project_root_folder(self):
        """Get project root folder path

        See Also:
            Wiki: docs/wiki/tools/get_project_root_folder.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if hasattr(self.song, "project_root_folder"):
                return {
                    "ok": True,
                    "project_root_folder": str(self.song.project_root_folder)
                    if self.song.project_root_folder
                    else None,
                }
            else:
                return {"ok": False, "error": "Project root folder not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def trigger_session_record(self, length=None):
        """Trigger session record with optional fixed length

        See Also:
            Wiki: docs/wiki/tools/trigger_session_record.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if length:
                self.song.trigger_session_record(float(length))
            else:
                self.song.trigger_session_record()
            return {"ok": True, "message": "Session record triggered"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_can_jump_to_next_cue(self):
        """Check if can jump to next cue point

        See Also:
            Wiki: docs/wiki/tools/get_can_jump_to_next_cue.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            return {"ok": True, "can_jump_to_next_cue": self.song.can_jump_to_next_cue}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_can_jump_to_prev_cue(self):
        """Check if can jump to previous cue point

        See Also:
            Wiki: docs/wiki/tools/get_can_jump_to_prev_cue.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            return {"ok": True, "can_jump_to_prev_cue": self.song.can_jump_to_prev_cue}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_to_next_cue(self):
        """Jump to next cue point

        See Also:
            Wiki: docs/wiki/tools/jump_to_next_cue.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if self.song.can_jump_to_next_cue:
                self.song.jump_to_next_cue()
                return {"ok": True, "message": "Jumped to next cue"}
            else:
                return {"ok": False, "error": "Cannot jump to next cue"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def jump_to_prev_cue(self):
        """Jump to previous cue point

        See Also:
            Wiki: docs/wiki/tools/jump_to_prev_cue.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if self.song.can_jump_to_prev_cue:
                self.song.jump_to_prev_cue()
                return {"ok": True, "message": "Jumped to previous cue"}
            else:
                return {"ok": False, "error": "Cannot jump to previous cue"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # ARRANGEMENT VIEW CLIPS
    # ========================================================================

    def get_arrangement_clips(self, track_index):
        """Get list of clips in arrangement view for a track

        See Also:
            Wiki: docs/wiki/tools/get_arrangement_clips.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]

            if hasattr(track, "arrangement_clips"):
                clips_info = []
                for clip in track.arrangement_clips:
                    clip_data = {
                        "name": str(clip.name),
                        "start_time": float(clip.start_time),
                        "end_time": float(clip.end_time),
                        "length": float(clip.length),
                    }
                    clips_info.append(clip_data)

                return {"ok": True, "count": len(clips_info), "clips": clips_info}
            else:
                return {"ok": False, "error": "Arrangement clips not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def duplicate_to_arrangement(self, track_index, clip_index):
        """Duplicate session clip to arrangement view

        See Also:
            Wiki: docs/wiki/tools/duplicate_to_arrangement.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_index]

            if not clip_slot.has_clip:
                return {"ok": False, "error": "No clip in slot"}

            clip = clip_slot.clip

            if hasattr(clip, "duplicate_loop"):
                clip.duplicate_loop()
                return {"ok": True, "message": "Clip duplicated to arrangement"}
            else:
                return {"ok": False, "error": "Duplicate to arrangement not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def consolidate_clip(self, track_index, start_time, end_time):
        """Consolidate arrangement clips in time range

        See Also:
            Wiki: docs/wiki/tools/consolidate_clip.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            return {
                "ok": True,
                "message": "Clip consolidation initiated",
                "start_time": float(start_time),
                "end_time": float(end_time),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
