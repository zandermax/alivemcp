"""
Transport position and automation recording controls.

Single responsibility: playhead position queries and automation arm/record state.
Metronome volume lives in session_transport.py.
"""


class SessionAutomationMixin:
    # ========================================================================
    # TRANSPORT OPERATIONS
    # ========================================================================

    def jump_to_time(self, time_in_beats):
        """Jump playback to specific time in beats

        See Also:
            Wiki: docs/wiki/tools/jump_to_time.md"""
        try:
            self.song.current_song_time = float(time_in_beats)
            return {"ok": True, "time": float(self.song.current_song_time)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_current_time(self):
        """Get current playback position in beats

        See Also:
            Wiki: docs/wiki/tools/get_current_time.md"""
        try:
            return {
                "ok": True,
                "current_song_time": float(self.song.current_song_time),
                "is_playing": self.song.is_playing,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_arrangement_overdub(self, enabled):
        """Enable/disable arrangement overdub

        See Also:
            Wiki: docs/wiki/tools/set_arrangement_overdub.md"""
        try:
            self.song.arrangement_overdub = bool(enabled)
            return {"ok": True, "arrangement_overdub": self.song.arrangement_overdub}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_back_to_arranger(self, enabled):
        """Enable/disable back to arrangement

        See Also:
            Wiki: docs/wiki/tools/set_back_to_arranger.md"""
        try:
            self.song.back_to_arranger = bool(enabled)
            return {"ok": True, "back_to_arranger": self.song.back_to_arranger}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_punch_in(self, enabled):
        """Enable/disable punch in recording

        See Also:
            Wiki: docs/wiki/tools/set_punch_in.md"""
        try:
            self.song.punch_in = bool(enabled)
            return {"ok": True, "punch_in": self.song.punch_in}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_punch_out(self, enabled):
        """Enable/disable punch out recording

        See Also:
            Wiki: docs/wiki/tools/set_punch_out.md"""
        try:
            self.song.punch_out = bool(enabled)
            return {"ok": True, "punch_out": self.song.punch_out}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def nudge_up(self):
        """Nudge playback position up

        See Also:
            Wiki: docs/wiki/tools/nudge_up.md"""
        try:
            self.song.nudge_up()
            return {"ok": True, "message": "Nudged up"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def nudge_down(self):
        """Nudge playback position down

        See Also:
            Wiki: docs/wiki/tools/nudge_down.md"""
        try:
            self.song.nudge_down()
            return {"ok": True, "message": "Nudged down"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # AUTOMATION OPERATIONS
    # ========================================================================

    def re_enable_automation(self):
        """Re-enable all automation

        See Also:
            Wiki: docs/wiki/tools/re_enable_automation.md"""
        try:
            self.song.re_enable_automation()
            return {"ok": True, "message": "Automation re-enabled"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_automation_record(self):
        """Get session automation recording state

        See Also:
            Wiki: docs/wiki/tools/get_session_automation_record.md"""
        try:
            return {"ok": True, "session_automation_record": self.song.session_automation_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_session_automation_record(self, enabled):
        """Enable/disable session automation recording

        See Also:
            Wiki: docs/wiki/tools/set_session_automation_record.md"""
        try:
            self.song.session_automation_record = bool(enabled)
            return {"ok": True, "session_automation_record": self.song.session_automation_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_session_record(self):
        """Get session record state

        See Also:
            Wiki: docs/wiki/tools/get_session_record.md"""
        try:
            return {"ok": True, "session_record": self.song.session_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_session_record(self, enabled):
        """Enable/disable session recording

        See Also:
            Wiki: docs/wiki/tools/set_session_record.md"""
        try:
            self.song.session_record = bool(enabled)
            return {"ok": True, "session_record": self.song.session_record}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def capture_midi(self):
        """Capture MIDI from the last played notes

        See Also:
            Wiki: docs/wiki/tools/capture_midi.md"""
        try:
            self.song.capture_midi()
            return {"ok": True, "message": "MIDI captured"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
