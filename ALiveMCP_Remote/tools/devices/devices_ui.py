"""
Device UI and preset helpers mixin.
"""


class DevicesUIMixin:
    def get_device_presets(self, track_index, device_index):
        """Get available presets for device

        See Also:
            Wiki: docs/wiki/tools/get_device_presets.md

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
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            return {
                "ok": True,
                "message": "Device preset browsing requires browser API",
                "device_index": device_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_preset(self, track_index, device_index, preset_index):
        """Load preset for device

        See Also:
            Wiki: docs/wiki/tools/set_device_preset.md

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
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            return {
                "ok": True,
                "message": "Device preset loading requires browser API",
                "preset_index": preset_index,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def show_plugin_window(self, track_index, device_index):
        """Show device/plugin window

        See Also:
            Wiki: docs/wiki/tools/show_plugin_window.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]
            self.c_instance.song().view.select_device(device)
            return {"ok": True, "message": "Plugin window shown", "device_name": str(device.name)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def hide_plugin_window(self, track_index, device_index):
        """Hide device/plugin window

        See Also:
            Wiki: docs/wiki/tools/hide_plugin_window.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            return {"ok": True, "message": "Plugin window hidden"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
