---
name: "create_group_track"
summary: ""
Live mapping: "- Calls `self.song.create_group_track(track_index)` where `track_index = len(self.song.tracks)`, and sets `name` if provided."
---

# create_group_track

**Domain:** tracks

**Summary:** Create a new group track (folder/group) at the end of the track list.

**Parameters:**

- `name` (string, optional)

**Live mapping:**

- Calls `self.song.create_group_track(track_index)` where `track_index = len(self.song.tracks)`, and sets `name` if provided.
  **Example request:**

```json
{ "action": "create_group_track", "name": "Drums" }
```

**Example response:**

```json
{
  "ok": true,
  "message": "Group track created",
  "track_index": 4,
  "name": "Drums"
}
```
