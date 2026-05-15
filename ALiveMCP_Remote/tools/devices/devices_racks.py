"""
Rack/chain operations and device class/type utilities.

Single responsibility: reading and mutating rack chain structure (mute/solo)
and querying device class metadata.
"""


class DevicesRacksMixin:
    # ========================================================================
    # RACK/CHAIN OPERATIONS
    # ========================================================================

    def get_device_chains(self, track_index, device_index):
        """Get chains from a rack device

        See Also:
            Wiki: docs/wiki/tools/get_device_chains.md

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

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains (not a rack)"}

            chains = []
            for i, chain in enumerate(device.chains):
                chains.append(
                    {
                        "index": i,
                        "name": str(chain.name),
                        "mute": chain.mute if hasattr(chain, "mute") else False,
                        "solo": chain.solo if hasattr(chain, "solo") else False,
                        "num_devices": len(chain.devices) if hasattr(chain, "devices") else 0,
                    }
                )

            return {"ok": True, "chains": chains, "count": len(chains)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_chain_devices(self, track_index, device_index, chain_index):
        """Get devices in a specific chain

        See Also:
            Wiki: docs/wiki/tools/get_chain_devices.md

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

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]
            chain_devices = []

            if hasattr(chain, "devices"):
                for dev in chain.devices:
                    chain_devices.append(
                        {
                            "name": str(dev.name),
                            "class_name": str(dev.class_name),
                            "is_active": dev.is_active,
                        }
                    )

            return {
                "ok": True,
                "chain_index": chain_index,
                "devices": chain_devices,
                "count": len(chain_devices),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_chain_mute(self, track_index, device_index, chain_index, mute):
        """Mute/unmute a chain in a rack

        See Also:
            Wiki: docs/wiki/tools/set_chain_mute.md

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

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]

            if hasattr(chain, "mute"):
                chain.mute = bool(mute)
                return {"ok": True, "chain_index": chain_index, "mute": chain.mute}
            else:
                return {"ok": False, "error": "Chain mute not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def set_chain_solo(self, track_index, device_index, chain_index, solo):
        """Solo/unsolo a chain in a rack

        See Also:
            Wiki: docs/wiki/tools/set_chain_solo.md

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

            device = track.devices[device_index]

            if not hasattr(device, "chains"):
                return {"ok": False, "error": "Device does not have chains"}

            if chain_index < 0 or chain_index >= len(device.chains):
                return {"ok": False, "error": "Invalid chain index"}

            chain = device.chains[chain_index]

            if hasattr(chain, "solo"):
                chain.solo = bool(solo)
                return {"ok": True, "chain_index": chain_index, "solo": chain.solo}
            else:
                return {"ok": False, "error": "Chain solo not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    # ========================================================================
    # DEVICE UTILITIES
    # ========================================================================

    def get_device_class_name(self, track_index, device_index):
        """Get device class name (e.g., 'OriginalSimpler', 'Compressor2')

        See Also:
            Wiki: docs/wiki/tools/get_device_class_name.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "class_name"):
                return {"ok": True, "class_name": str(device.class_name)}
            else:
                return {"ok": False, "error": "Class name not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_device_type(self, track_index, device_index):
        """Get device type (audio_effect, instrument, midi_effect)

        See Also:
            Wiki: docs/wiki/tools/get_device_type.md

        Args:
            TODO: describe parameters.

        Returns:
            TODO: describe return value.

        Raises:
            TODO: exceptions raised."""
        try:
            track = self.song.tracks[track_index]
            device = track.devices[device_index]

            if hasattr(device, "type"):
                return {"ok": True, "type": int(device.type)}
            else:
                return {"ok": False, "error": "Device type not available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
