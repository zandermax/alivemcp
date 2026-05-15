---
name: "set_clip_signature_numerator"
summary: ""
---

# set_clip_signature_numerator

Set Clip Signature Numerator

Set the time signature numerator for a clip.

Parameters:

- `track_index` (int)
- `clip_index` (int)
- `numerator` (int)

Returns:

- `ok`: boolean
- `signature_numerator`: int (new value)
  **Example request:**

```json
{
  "action": "set_clip_signature_numerator",
  "track_index": 0,
  "clip_index": 0,
  "numerator": 4
}
```

**Example response:**

```json
{ "ok": true }
```
