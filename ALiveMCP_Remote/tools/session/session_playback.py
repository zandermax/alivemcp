"""
Session playback and control mixin.

Single responsibility: start/stop/record/continue and session info.
"""


class SessionPlaybackMixin:
    def start_playback(self):
        """Start Ableton playback

        See Also:
            Wiki: docs/wiki/tools/start_playback.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if not self.song.is_playing:
                self.song.start_playing()
            return {"ok": True, "message": "Playback started"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_playback(self):
        """Stop Ableton playback

        See Also:
            Wiki: docs/wiki/tools/stop_playback.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if self.song.is_playing:
                self.song.stop_playing()
            return {"ok": True, "message": "Playback stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def start_recording(self):
        """Start recording

        See Also:
            Wiki: docs/wiki/tools/start_recording.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.record_mode = True
            if not self.song.is_playing:
                self.song.start_playing()
            return {"ok": True, "message": "Recording started"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_recording(self):
        """Stop recording

        See Also:
            Wiki: docs/wiki/tools/stop_recording.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.record_mode = False
            return {"ok": True, "message": "Recording stopped"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def continue_playing(self):
        """Continue playback from current position

        See Also:
            Wiki: docs/wiki/tools/continue_playing.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.continue_playing()
            return {"ok": True, "message": "Playback continued"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_info(self):
        """Get current session state information

        See Also:
            Wiki: docs/wiki/tools/get_session_info.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            return {
                "ok": True,
                "is_playing": self.song.is_playing,
                "tempo": float(self.song.tempo),
                "time_signature_numerator": self.song.signature_numerator,
                "time_signature_denominator": self.song.signature_denominator,
                "current_song_time": float(self.song.current_song_time),
                "loop_start": float(self.song.loop_start),
                "loop_end": float(self.song.loop_start + self.song.loop_length),
                "loop_length": float(self.song.loop_length),
                "num_tracks": len(self.song.tracks),
                "num_scenes": len(self.song.scenes),
                "record_mode": self.song.record_mode,
                "metronome": self.song.metronome,
                "nudge_up": self.song.nudge_up,
                "nudge_down": self.song.nudge_down,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def undo(self):
        """Undo last action

        See Also:
            Wiki: docs/wiki/tools/undo.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.undo()
            return {"ok": True, "message": "Undo executed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def redo(self):
        """Redo last undone action

        See Also:
            Wiki: docs/wiki/tools/redo.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            self.song.redo()
            return {"ok": True, "message": "Redo executed"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
