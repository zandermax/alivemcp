"""
Audio clip file helpers.
"""


class M4LFileMixin:
    def get_clip_file_path(self, track_index, clip_index):
        """Get audio clip file path

        See Also:
            Wiki: docs/wiki/tools/get_clip_file_path.md

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
            if not clip.is_audio_clip:
                return {"ok": False, "error": "Clip is not an audio clip"}

            file_path = ""
            if hasattr(clip, "file_path"):
                file_path = str(clip.file_path)
            elif hasattr(clip, "sample") and hasattr(clip.sample, "file_path"):
                file_path = str(clip.sample.file_path)

            return {"ok": True, "file_path": file_path}
        except Exception as e:
            return {"ok": False, "error": str(e)}
