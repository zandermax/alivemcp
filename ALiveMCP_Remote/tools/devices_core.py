"""
Core device operations: add, inspect, and set parameters.
"""


class DevicesCoreMixin:
    # ========================================================================
    # DEVICE OPERATIONS
    # ========================================================================

    def add_device(self, track_index, device_name):
        """Add device to track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            return {
                "ok": True,
                "message": "Device add requested (browser API required for full implementation)",
                "device_name": device_name,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_devices(self, track_index):
        """Get all devices on track"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            devices = []

            for device in track.devices:
                devices.append(
                    {
                        "name": str(device.name),
                        "class_name": str(device.class_name),
                        "is_active": device.is_active,
                        "num_parameters": len(device.parameters),
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "devices": devices,
                "count": len(devices),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_device_param(self, track_index, device_index, param_index, value):
        """Set device parameter value"""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            if param_index < 0 or param_index >= len(device.parameters):
                return {"ok": False, "error": "Invalid parameter index"}

            param = device.parameters[param_index]
            param.value = float(value)

            return {"ok": True, "message": "Parameter set", "value": float(param.value)}
        except Exception as e:
            return {"ok": False, "error": str(e)}
