---
name: "get_device_type"
summary: ""
Live mapping: "- Reads `device.type` and returns the integer value representing the device category."
---

# get_device_type

**Domain:** devices

**Summary:** Get the device type (audio_effect, instrument, midi_effect) when available.

**Parameters:**

- `track_index` (int)
- `device_index` (int)

**Live mapping:**

- Reads `device.type` and returns the integer value representing the device category.
  **Example request:**

```json
{ "action": "get_device_type", "track_index": 1, "device_index": 0 }
```

**Example response:**

```json
{ "ok": true, "type": 1 }
```

**Notes:**

- Behavior depends on Live's object model exposure.

**See also:**

- [get_device_class_name](tools/devices/get_device_class_name.md)
