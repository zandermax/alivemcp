"""
Master track operations for Mixing.

Single responsibility: master-track info and controls.
"""


class MixingMasterMixin:
    def get_master_track_info(self):
        """Get master track information

        See Also:
            Wiki: docs/wiki/tools/get_master_track_info.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            master = self.song.master_track

            info = {
                "ok": True,
                "name": str(master.name),
                "volume": float(master.mixer_device.volume.value)
                if hasattr(master, "mixer_device")
                else 0.0,
                "pan": float(master.mixer_device.panning.value)
                if hasattr(master, "mixer_device")
                else 0.0,
                "num_devices": len(master.devices) if hasattr(master, "devices") else 0,
            }

            return info
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_volume(self, volume):
        """Set master track volume (0.0 to 1.0)

        See Also:
            Wiki: docs/wiki/tools/set_master_volume.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            master = self.song.master_track
            if hasattr(master, "mixer_device"):
                master.mixer_device.volume.value = float(max(0.0, min(1.0, volume)))
                return {"ok": True, "volume": float(master.mixer_device.volume.value)}
            else:
                return {"ok": False, "error": "Master mixer device not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_pan(self, pan):
        """Set master track pan (-1.0 to 1.0)

        See Also:
            Wiki: docs/wiki/tools/set_master_pan.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            master = self.song.master_track
            if hasattr(master, "mixer_device"):
                master.mixer_device.panning.value = float(max(-1.0, min(1.0, pan)))
                return {"ok": True, "pan": float(master.mixer_device.panning.value)}
            else:
                return {"ok": False, "error": "Master mixer device not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_master_devices(self):
        """Get all devices on master track

        See Also:
            Wiki: docs/wiki/tools/get_master_devices.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            master = self.song.master_track
            devices = []

            if hasattr(master, "devices"):
                for device in master.devices:
                    devices.append(
                        {
                            "name": str(device.name),
                            "class_name": str(device.class_name),
                            "is_active": device.is_active,
                        }
                    )

            return {"ok": True, "devices": devices, "count": len(devices)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
