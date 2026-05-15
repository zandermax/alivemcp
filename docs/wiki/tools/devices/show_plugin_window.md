---
name: "show_plugin_window"
summary: ""
Live mapping: "- Calls `c_instance.song().view.select_device(device)` to focus the device in Live's UI."
---

# show_plugin_window

**Domain:** devices

**Summary:** Bring a device's plugin window into view (select the device in Live UI).

**Parameters:**

- `track_index` (int)
- `device_index` (int)

**Live mapping:**

- Calls `c_instance.song().view.select_device(device)` to focus the device in Live's UI.
  **Example request:**

```json
{ "action": "show_plugin_window", "track_index": 1, "device_index": 0 }
```

**Example response:**

```json
{ "ok": true, "message": "Plugin window shown", "device_name": "Reverb" }
```

**Notes:**

- This manipulates the Live UI; use carefully during performance.

**See also:**

- [hide_plugin_window](tools/devices/hide_plugin_window.md)
