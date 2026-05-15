---
name: "load_device_from_browser"
summary: ""
Live mapping: "- Delegates to `add_device(track_index, device_name)`; actual loading depends on host browser APIs."
---

# load_device_from_browser

**Domain:** arrangement (browser)

**Summary:** Alias to `add_device`: load a device by name from the browser onto a track.

**Parameters:**

- `track_index` (int)
- `device_name` (string)

**Live mapping:**

- Delegates to `add_device(track_index, device_name)`; actual loading depends on host browser APIs.
  **Example request:**

```json
{
  "action": "load_device_from_browser",
  "track_index": 1,
  "device_name": "Operator"
}
```

**Example response:**

```json
{ "ok": true, "message": "Device added" }
```
