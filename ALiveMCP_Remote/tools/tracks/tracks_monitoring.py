"""
Track monitoring and input state helpers.
"""


class TracksMonitoringMixin:
    # ========================================================================
    # MONITORING & INPUT
    # ========================================================================

    def set_track_current_monitoring_state(self, track_index, state):
        """Set track monitoring state (0=In, 1=Auto, 2=Off)

        See Also:
            Wiki: docs/wiki/tools/set_track_current_monitoring_state.md

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
            if track.can_be_armed:
                track.current_monitoring_state = int(state)
                return {"ok": True, "monitoring_state": track.current_monitoring_state}
            else:
                return {"ok": False, "error": "Track cannot be monitored"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
