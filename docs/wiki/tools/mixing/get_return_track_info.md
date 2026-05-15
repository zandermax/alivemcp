---
name: "get_return_track_info"
summary: ""
Live mapping: "- Reads `song.return_tracks[return_index]` and returns mixer/device properties."
---

# get_return_track_info

**Domain:** mixing

**Summary:** Retrieve information about a specific return track (name, volume, pan, mute, solo, device count).

**Parameters:**

- `return_index` (int)

**Live mapping:**

- Reads `song.return_tracks[return_index]` and returns mixer/device properties.

**Example request:**

```json
{ "action": "get_return_track_info", "return_index": 0 }
```

**Example response:**

```json
{
  "ok": true,
  "index": 0,
  "name": "Return A",
  "volume": 0.6,
  "pan": 0.0,
  "mute": false,
  "solo": false,
  "num_devices": 1
}
```

**Notes:**

- Validates `return_index` and returns errors for invalid indexes.

**See also:**

- [set_return_track_volume](tools/mixing/set_return_track_volume.md)
