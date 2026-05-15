---
name: "get_sample_length"
summary: ""
Live mapping: "Queries the device sample or Simpler API to retrieve sample length."
---

# get_sample_length

**Domain:** m4l

**Summary:** Return the length (in seconds or beats) of a sample used by a device (e.g., Simpler/Sampler).

**Parameters:**

- `track_index` (int)
- `device_id` (int or string) — identifies the device containing the sample

**Live mapping:** Queries the device sample or Simpler API to retrieve sample length.
**Example request:**

```json
{ "action": "get_sample_length", "track_index": 1, "device_id": 0 }
```

**Example response:**

```json
{ "ok": true }
```

**Example request:**

```json
{ "ok": true, "length_seconds": 3.25 }
```

**Notes:**

- Behavior depends on device type; may not be available for all devices.
