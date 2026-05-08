"""
Built-in tools: ping, health_check, and the public PARAM_ALIASES backward-compat table.

These tools are handled at the LiveAPITools level so the dispatcher in
ALiveMCP.__init__ can route them uniformly via getattr, exactly like all other
tools, with no special-case branching.

PARAM_ALIASES lives here because the built-in dispatcher (ALiveMCP.__init__)
consumes it — keeping it co-located with the tools that motivated its creation
makes the dependency explicit.

NOTE: Do not remove PARAM_ALIASES entries — each is a supported public alias
(see CLAUDE.md).
"""

import Live

# Per-action parameter aliases for backward compatibility.
# When a client sends the legacy key, it is translated to the canonical key
# before dispatch. Only clip-slot actions get the scene_index->clip_index alias;
# actual scene operations (launch_scene, delete_scene, ...) keep their own
# scene_index parameter and are NOT listed here.
PARAM_ALIASES = {
    "create_midi_clip": {"scene_index": "clip_index"},
    "delete_clip": {"scene_index": "clip_index"},
    "duplicate_clip": {"scene_index": "clip_index"},
    "launch_clip": {"scene_index": "clip_index"},
    "stop_clip": {"scene_index": "clip_index"},
    "get_clip_info": {"scene_index": "clip_index"},
    "set_clip_name": {"scene_index": "clip_index"},
    "add_notes": {"scene_index": "clip_index"},
}


class BuiltinMixin:
    """
    Provides ping, health_check, and access to PARAM_ALIASES.

    Single responsibility: built-in diagnostic/protocol tools that every
    ALiveMCP client expects to be available regardless of domain.
    """

    def ping(self):
        """Return a pong response confirming the script is running."""
        from ALiveMCP_Remote import __version__

        return {
            "ok": True,
            "message": "pong (queue-based, thread-safe)",
            "script": "ALiveMCP_Remote",
            "version": __version__,
        }

    def health_check(self):
        """Return health status including version, tool count, and queue size."""
        from ALiveMCP_Remote import __version__

        try:
            ableton_version = str(Live.Application.get_application().get_major_version())
        except Exception:
            ableton_version = "unknown"

        cmd_queue = getattr(self, "_command_queue", None)
        return {
            "ok": True,
            "message": "ALiveMCP Remote Script running (thread-safe)",
            "version": __version__,
            "tool_count": len(self.get_available_tools()),
            "ableton_version": ableton_version,
            "queue_size": cmd_queue.qsize() if cmd_queue is not None else 0,
        }
