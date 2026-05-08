"""Full rack interior inspection: chains, chain devices, and enriched parameter lists."""


class DevicesRackContentsMixin:
    def get_rack_contents(self, track_index, device_index):
        """Get full rack interior: chains, chain devices, and enriched parameters."""
        try:
            if track_index < 0 or track_index >= len(self.song.tracks):
                return {"ok": False, "error": "Invalid track index"}

            track = self.song.tracks[track_index]
            if device_index < 0 or device_index >= len(track.devices):
                return {"ok": False, "error": "Invalid device index"}

            rack_device = track.devices[device_index]
            class_name = str(rack_device.class_name) if hasattr(rack_device, "class_name") else ""
            if "GroupDevice" not in class_name:
                return {"ok": False, "error": "Device at device_index is not a rack (no chains)"}

            if not hasattr(rack_device, "chains"):
                return {"ok": False, "error": "Device at device_index is not a rack (no chains)"}

            chains_info = []
            for chain_index, chain in enumerate(rack_device.chains):
                chain_devices = []

                if hasattr(chain, "devices"):
                    for d_idx, device in enumerate(chain.devices):
                        params_info = []

                        if hasattr(device, "parameters"):
                            for param in device.parameters:
                                try:
                                    display_value = str(param.str_for_value(param.value))
                                except Exception:
                                    display_value = str(param.value)

                                is_quantized = (
                                    bool(param.is_quantized)
                                    if hasattr(param, "is_quantized")
                                    else False
                                )
                                value_items = []
                                if is_quantized and hasattr(param, "value_items"):
                                    value_items = [str(v) for v in param.value_items]

                                params_info.append(
                                    {
                                        "name": str(param.name),
                                        "raw_value": float(param.value),
                                        "display_value": display_value,
                                        "min": float(param.min),
                                        "max": float(param.max),
                                        "is_quantized": is_quantized,
                                        "value_items": value_items,
                                    }
                                )

                        chain_devices.append(
                            {
                                "device_index": d_idx,
                                "name": str(device.name),
                                "class_name": str(device.class_name),
                                "is_active": (
                                    bool(device.is_active)
                                    if hasattr(device, "is_active")
                                    else False
                                ),
                                "parameters": params_info,
                            }
                        )

                chains_info.append(
                    {
                        "chain_index": chain_index,
                        "chain_name": str(chain.name),
                        "devices": chain_devices,
                    }
                )

            return {
                "ok": True,
                "track_index": track_index,
                "device_index": device_index,
                "rack_name": str(rack_device.name),
                "chains": chains_info,
                "count": len(chains_info),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}
