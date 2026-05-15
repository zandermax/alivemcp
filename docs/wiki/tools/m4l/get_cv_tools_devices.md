---
name: "get_cv_tools_devices"
summary: ""
---

# get_cv_tools_devices

Get CV (Control Voltage) Tools Devices

List CV (Control Voltage) Tools devices on a track (heuristic by name).

Parameters:

- `track_index` (int)

Returns:

- `ok`: boolean
- `track_index`: int
- `track_name`: string
- `cv_devices`: list of {index, name, class_name, is_active, num_parameters}
- `count`: int

**Example request:**

```json
{ "action": "get_cv_tools_devices", "track_index": 0 }
```

**Example response:**

```json
{
  "ok": true,
  "track_index": 0,
  "track_name": "Track 1",
  "cv_devices": [
    {
      "index": 0,
      "name": "CV Tools Device",
      "class_name": "CVTool",
      "is_active": true,
      "num_parameters": 4
    }
  ],
  "count": 1
}
```
