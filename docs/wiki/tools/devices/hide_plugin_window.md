# hide_plugin_window

**Domain:** devices

**Summary:** Hide a device's plugin window (no-op in current implementation).

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Currently returns success; explicit hiding of plugin windows is not implemented.
**Example request:**
```json
{"action":"hide_plugin_window","track_index":1,"device_index":0}
```
**Example response:**
```json
{"ok": true, "message": "Plugin window hidden"}
```

**Notes:**
- Implementation may be extended in future to better control host UI.

**See also:**
- [show_plugin_window](tools/devices/show_plugin_window.md)
