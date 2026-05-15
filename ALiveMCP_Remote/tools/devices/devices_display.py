"""
Device parameter display value tools.

Single responsibility: reading parameter values as formatted UI strings and
collecting full enriched parameter info from track devices.
"""


class DevicesDisplayMixin:
    # ========================================================================
    # DEVICE PARAMETER DISPLAY VALUES
    # ========================================================================

    def get_device_param_display_value(self, track_index, device_index, param_index):
        """Get device parameter value as displayed in UI (Live 12+)

        See Also:
            Wiki: docs/wiki/tools/get_device_param_display_value.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]
            param = device.parameters[param_index]

            if hasattr(param, "display_value"):
                return {
                    "ok": True,
                    "display_value": str(param.display_value),
                    "raw_value": float(param.value),
                    "name": str(param.name),
                }
            else:
                return {
                    "ok": True,
                    "display_value": str(param.__str__()),
                    "raw_value": float(param.value),
                    "name": str(param.name),
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_all_param_display_values(self, track_index, device_index):
        """Get all enriched parameter info for a device on a regular track

        See Also:
            Wiki: docs/wiki/tools/get_all_param_display_values.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            params_info = []
            for i, param in enumerate(device.parameters):
                display_value = (
                    str(param.display_value)
                    if hasattr(param, "display_value")
                    else str(param.__str__())
                )
                is_quantized = bool(param.is_quantized) if hasattr(param, "is_quantized") else False
                value_items = (
                    [str(v) for v in param.value_items] if hasattr(param, "value_items") else []
                )
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
                "device_name": str(device.name),
                "count": len(params_info),
                "parameters": params_info,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
