"""
Compatibility shim: SessionTransportMixin

This file re-exports the split session mixins as a single
`SessionTransportMixin` for backwards compatibility with older callers
and tests that expect a single aggregated mixin.
"""

from .session_automation import SessionAutomationMixin
from .session_metronome import SessionMetronomeMixin
from .session_playback import SessionPlaybackMixin
from .session_tempo import SessionTempoMixin


class SessionTransportMixin(
    SessionPlaybackMixin,
    SessionMetronomeMixin,
    SessionTempoMixin,
    SessionAutomationMixin,
):
    """Aggregated session transport mixin for backwards compatibility.

    This single class re-exports the focused session mixins so legacy
    callers and tests that expect `SessionTransportMixin` continue to
    work after the split refactor.
    """

    pass

    def set_metronome_volume(self, volume):
        """Set metronome volume (0.0 to 1.0)

        See Also:
            Wiki: docs/wiki/tools/set_metronome_volume.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            if hasattr(self.song, "metronome"):
                self.song.metronome = float(volume)
                return {"ok": True, "volume": float(self.song.metronome)}
            else:
                return {"ok": False, "error": "Metronome volume not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
