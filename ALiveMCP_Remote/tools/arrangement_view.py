"""
Arrangement view navigation and loop state tools.

Single responsibility: controlling the arrangement/session view display,
track focus, view scrolling, and song loop enable/disable state.

Note: ``Live`` is used without an explicit import — it is injected into the
Ableton runtime namespace.  Tests that exercise the ``show_*`` methods must
patch ``Live`` onto this module directly (see the ``live_in_arrangement``
fixture in the test suite).
"""


class ArrangementViewMixin:
    # ========================================================================
    # VIEW / NAVIGATION
    # ========================================================================

    def show_clip_view(self):
        """Show clip/session view"""
        try:
            app = Live.Application.get_application()
            if hasattr(app.view, "show_view"):
                app.view.show_view("Session")
                return {"ok": True, "message": "Showing clip/session view"}
            else:
                return {"ok": False, "error": "View control not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_arrangement_view(self):
        """Show arrangement view"""
        try:
            app = Live.Application.get_application()
            if hasattr(app.view, "show_view"):
                app.view.show_view("Arranger")
                return {"ok": True, "message": "Showing arrangement view"}
            else:
                return {"ok": False, "error": "View control not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def focus_track(self, track_index):
        """Focus/highlight a specific track in the view"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]

            if hasattr(self.song.view, "selected_track"):
                self.song.view.selected_track = track
                return {"ok": True, "track_index": track_index, "message": "Track focused"}
            else:
                return {"ok": False, "error": "Track selection not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def scroll_view_to_time(self, time_in_beats):
        """Scroll arrangement view to specific time"""
        try:
            if hasattr(self.song.view, "visible_tracks"):
                return {
                    "ok": True,
                    "message": "View scroll requested (limited API support)",
                    "time": float(time_in_beats),
                }
            else:
                return {"ok": False, "error": "View scrolling not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # LOOP STATE
    # ========================================================================

    def set_loop_enabled(self, enabled):
        """Enable or disable song loop"""
        try:
            self.song.loop = bool(enabled)
            return {"ok": True, "loop_enabled": self.song.loop}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_loop_enabled(self):
        """Get current loop enabled state"""
        try:
            return {
                "ok": True,
                "loop_enabled": self.song.loop,
                "loop_start": float(self.song.loop_start),
                "loop_length": float(self.song.loop_length),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
