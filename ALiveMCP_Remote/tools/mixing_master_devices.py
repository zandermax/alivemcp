"""
Master track device parameter tools: read, inspect, and set params on master chain devices.
"""


class MixingMasterDevicesMixin:
    # ========================================================================
    # MASTER TRACK DEVICE PARAMETERS
    # ========================================================================

    def get_master_device_params(self, device_index):
        """Get all enriched parameter info for a device on the master track"""
        try:
            master = self.song.master_track
            if device_index < 0 or device_index >= len(master.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = master.devices[device_index]
            params_info = []
            for i, param in enumerate(device.parameters):
                display_value = str(param.display_value) if hasattr(param, "display_value") else str(param.__str__())
                is_quantized = bool(param.is_quantized) if hasattr(param, "is_quantized") else False
                value_items = [str(v) for v in param.value_items] if hasattr(param, "value_items") else []
                params_info.append({
                    "index": i,
                    "name": str(param.name),
                    "raw_value": float(param.value),
                    "display_value": display_value,
                    "min": float(param.min),
                    "max": float(param.max),
                    "is_quantized": is_quantized,
                    "value_items": value_items,
                })

            return {
                "ok": True,
                "device_name": str(device.name),
                "count": len(params_info),
                "parameters": params_info,
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_device_param(self, device_index, param_index, value):
        """Set a parameter value on a device on the master track by index"""
        try:
            master = self.song.master_track
            if device_index < 0 or device_index >= len(master.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = master.devices[device_index]
            if param_index < 0 or param_index >= len(device.parameters):
                return {"ok": False, "error": "Invalid parameter index"}

            param = device.parameters[param_index]
            clamped = max(float(param.min), min(float(param.max), float(value)))
            param.value = clamped
            return {
                "ok": True,
                "device_name": str(device.name),
                "param_name": str(param.name),
                "value": float(param.value),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_master_device_param_by_name(self, device_index, param_name, value):
        """Set a master track device parameter by name.

        For quantized parameters, pass a string matching one of the value_items
        (e.g. "4:1"). For continuous parameters, pass a number — it will be
        clamped to the parameter's min/max range.
        Matches the first parameter whose name equals param_name.
        """
        try:
            master = self.song.master_track
            if device_index < 0 or device_index >= len(master.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = master.devices[device_index]

            for param in device.parameters:
                if str(param.name) != param_name:
                    continue

                if isinstance(value, str):
                    value_items = [str(v) for v in param.value_items] if hasattr(param, "value_items") else []
                    if not value_items:
                        return {"ok": False, "error": "Parameter has no value_items for string lookup"}
                    try:
                        idx = value_items.index(value)
                    except ValueError:
                        return {"ok": False, "error": "'" + value + "' not in value_items: " + str(value_items)}
                    param.value = float(idx)
                else:
                    clamped = max(float(param.min), min(float(param.max), float(value)))
                    param.value = clamped

                display_value = str(param.display_value) if hasattr(param, "display_value") else str(param.__str__())
                return {
                    "ok": True,
                    "device_name": str(device.name),
                    "param_name": str(param.name),
                    "value": float(param.value),
                    "display_value": display_value,
                }

            return {"ok": False, "error": "Parameter '" + param_name + "' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_master_device_param_info(self, device_index, param_name):
        """Get enriched info for a single master track device parameter by name.

        Matches the first parameter whose name equals param_name.
        """
        try:
            master = self.song.master_track
            if device_index < 0 or device_index >= len(master.devices):
                return {"ok": False, "error": "Invalid device index"}

            device = master.devices[device_index]

            for i, param in enumerate(device.parameters):
                if str(param.name) != param_name:
                    continue

                display_value = str(param.display_value) if hasattr(param, "display_value") else str(param.__str__())
                is_quantized = bool(param.is_quantized) if hasattr(param, "is_quantized") else False
                value_items = [str(v) for v in param.value_items] if hasattr(param, "value_items") else []
                return {
                    "ok": True,
                    "device_name": str(device.name),
                    "index": i,
                    "name": str(param.name),
                    "raw_value": float(param.value),
                    "display_value": display_value,
                    "min": float(param.min),
                    "max": float(param.max),
                    "is_quantized": is_quantized,
                    "value_items": value_items,
                }

            return {"ok": False, "error": "Parameter '" + param_name + "' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_master_chain_summary(self):
        """Get all devices on the master track with full enriched parameter lists"""
        try:
            master = self.song.master_track
            devices = []

            for d_idx, device in enumerate(master.devices):
                params_info = []
                for i, param in enumerate(device.parameters):
                    display_value = str(param.display_value) if hasattr(param, "display_value") else str(param.__str__())
                    is_quantized = bool(param.is_quantized) if hasattr(param, "is_quantized") else False
                    value_items = [str(v) for v in param.value_items] if hasattr(param, "value_items") else []
                    params_info.append({
                        "index": i,
                        "name": str(param.name),
                        "raw_value": float(param.value),
                        "display_value": display_value,
                        "min": float(param.min),
                        "max": float(param.max),
                        "is_quantized": is_quantized,
                        "value_items": value_items,
                    })

                devices.append({
                    "index": d_idx,
                    "name": str(device.name),
                    "class_name": str(device.class_name),
                    "is_active": device.is_active,
                    "parameters": params_info,
                })

            return {"ok": True, "count": len(devices), "devices": devices}
        except Exception as e:
            return {"ok": False, "error": str(e)}
