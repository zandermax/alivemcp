---
name: "launch_scene"
summary: ""
Live mapping: "- Validates index bounds and calls `self.song.scenes[scene_index].fire()`."
---

# launch_scene

**Domain:** scenes

**Summary:** Launch (fire) a scene by index.

**Parameters:**

- `scene_index` (int)

**Live mapping:**

- Validates index bounds and calls `self.song.scenes[scene_index].fire()`.
  **Example request:**

```json
{ "action": "launch_scene", "scene_index": 0 }
```

**Example response:**

```json
{ "ok": true, "message": "Scene launched", "scene_index": 0 }
```

**Notes:**

- Firing a scene triggers its clip slots according to Ableton's launch quantization settings.

**See also:**

- stop_clip, launch_clip
