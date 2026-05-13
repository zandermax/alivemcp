# is_max_device

Is Max Device

Check whether a device on a track is a Max for Live device.

Parameters:
- `track_index` (int)
- `device_index` (int)

Returns:
- `ok`: boolean
- `is_m4l`: boolean
- `class_name`: string
- `class_display_name`: string
- `device_name`: string

**Example request:**

```json
{"action": "is_max_device", "track_index": 0, "device_index": 0}
```

**Example response:**

```json
{"ok": true, "is_m4l": true, "class_name": "MaxForLiveDevice", "class_display_name": "Max Device", "device_name": "My M4L Device"}
```

