"""
Browser operations: browse devices, plugins, and browser category items.

Single responsibility: Live browser inspection tools.

Color getters (get_clip_color, get_track_color) live in clips_properties.py
and tracks_core.py respectively.
"""


class ArrangementBrowserMixin:
    # ========================================================================
    # BROWSER OPERATIONS
    # ========================================================================

    def browse_devices(self):
        """Get list of available devices from browser

        See Also:
            Wiki: docs/wiki/tools/browse_devices.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            device_types = [
                "Instrument",
                "Audio Effect",
                "MIDI Effect",
                "Drum Rack",
                "Instrument Rack",
                "Effect Rack",
            ]
            return {"ok": True, "device_types": device_types, "count": len(device_types)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def browse_plugins(self, plugin_type="vst"):
        """Browse available plugins (VST, AU, etc.)

        See Also:
            Wiki: docs/wiki/tools/browse_plugins.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            return {
                "ok": True,
                "message": "Plugin browsing via LiveAPI is limited",
                "plugin_type": plugin_type,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def load_device_from_browser(self, track_index, device_name):
        """Load a device from browser onto track (alias for add_device)

        See Also:
            Wiki: docs/wiki/tools/load_device_from_browser.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        return self.add_device(track_index, device_name)

    def get_browser_items(self, category="devices"):
        """Get browser items by category

        See Also:
            Wiki: docs/wiki/tools/get_browser_items.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            categories = ["devices", "plugins", "instruments", "audio_effects", "midi_effects"]
            return {
                "ok": True,
                "category": category,
                "available_categories": categories,
                "message": "Browser item enumeration is limited in LiveAPI",
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
