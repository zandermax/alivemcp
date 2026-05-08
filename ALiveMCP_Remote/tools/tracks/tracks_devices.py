"""
Track device parameter tools with enriched parameter data (display values, items, etc).
Provides get and set operations matching master-channel enrichment level.
"""


class TracksDevicesMixin:
    # ========================================================================
    # TRACK DEVICE PARAMETERS — ENRICHED
    # ========================================================================

    def get_track_device_params(self, track_index, device_index):
        """Get all enriched parameter info for a device on any track.

        Returns name, raw_value, display_value, min, max, is_quantized, value_items
        for every parameter on that device.
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]
            params_info = []
            for i, param in enumerate(device.parameters):
                display_value = (
                    str(param.display_value)
                    if hasattr(param, "display_value")
                    else str(param.value)
                )
                is_quantized = bool(param.is_quantized) if hasattr(param, "is_quantized") else False
                value_items = [str(v) for v in param.value_items] if is_quantized else []
                params_info.append(
                    {
                        "index": i,
                        "name": str(param.name),
                        "raw_value": float(param.value),
                        "display_value": display_value,
                        "min": float(param.min),
                        "max": float(param.max),
                        "is_quantized": is_quantized,
                        "value_items": value_items,
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "device_name": str(device.name),
                "count": len(params_info),
                "parameters": params_info,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_device_param(self, track_index, device_index, param_index, value):
        """Set a parameter value on a device on any track by index.

        Clamps value to min/max range.
        """
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
            clamped = max(float(param.min), min(float(param.max), float(value)))
            param.value = clamped
            return {
                "ok": True,
                "track_index": track_index,
                "device_name": str(device.name),
                "param_name": str(param.name),
                "value": float(param.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_track_device_param_by_name(self, track_index, device_index, param_name, value):
        """Set a track device parameter by name.

        For quantized parameters, pass a string matching one of the value_items
        (e.g. "4:1"). For continuous parameters, pass a number — it will be
        clamped to the parameter's min/max range.
        Matches the first parameter whose name equals param_name.
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = track.devices[device_index]

            for param in device.parameters:
                if str(param.name) != param_name:
                    continue

                if isinstance(value, str):
                    is_quantized = (
                        bool(param.is_quantized) if hasattr(param, "is_quantized") else False
                    )
                    value_items = [str(v) for v in param.value_items] if is_quantized else []
                    if not value_items:
                        return {
                            "ok": False,
                            "error": "Parameter has no value_items for string lookup",
                        }
                    try:
                        idx = value_items.index(value)
                    except ValueError:
                        return {
                            "ok": False,
                            "error": "'" + value + "' not in value_items: " + str(value_items),
                        }
                    param.value = float(idx)
                else:
                    clamped = max(float(param.min), min(float(param.max), float(value)))
                    param.value = clamped

                try:
                    display_value = str(param.str_for_value(param.value))
                except Exception:
                    display_value = str(param.value)
                return {
                    "ok": True,
                    "track_index": track_index,
                    "device_name": str(device.name),
                    "param_name": str(param.name),
                    "value": float(param.value),
                    "display_value": display_value,
                }

            return {"ok": False, "error": "Parameter '" + param_name + "' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_track_chain_summary(self, track_index):
        """Get all devices on any track with full enriched parameter lists.

        Lets the AI read the entire device chain in one round trip, which is
        important for mastering work where you want a full picture before
        touching anything.
        """
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            devices = []

            for d_idx, device in enumerate(track.devices):
                params_info = []
                for i, param in enumerate(device.parameters):
                    display_value = (
                        str(param.display_value)
                        if hasattr(param, "display_value")
                        else str(param.value)
                    )
                    is_quantized = (
                        bool(param.is_quantized) if hasattr(param, "is_quantized") else False
                    )
                    value_items = [str(v) for v in param.value_items] if is_quantized else []
                    params_info.append(
                        {
                            "index": i,
                            "name": str(param.name),
                            "raw_value": float(param.value),
                            "display_value": display_value,
                            "min": float(param.min),
                            "max": float(param.max),
                            "is_quantized": is_quantized,
                            "value_items": value_items,
                        }
                    )

                devices.append(
                    {
                        "index": d_idx,
                        "name": str(device.name),
                        "class_name": str(device.class_name),
                        "is_active": device.is_active,
                        "parameters": params_info,
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "track_name": str(track.name),
                "count": len(devices),
                "devices": devices,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
