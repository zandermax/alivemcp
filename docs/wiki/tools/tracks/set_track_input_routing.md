---
name: "set_track_input_routing"
summary: ""
Live mapping: "- Validates index; returns a message indicating routing change requested. Actual routing options depend on host capabilities."
---

# set_track_input_routing

**Domain:** tracks

**Summary:** Set track input routing type and channel (requires routing configuration support).

**Parameters:**

- `track_index` (int)
- `routing_type_name` (string)
- `routing_channel` (int, default 0)

**Live mapping:**

- Validates index; returns a message indicating routing change requested. Actual routing options depend on host capabilities.
  **Example request:**

```json
{
  "action": "set_track_input_routing",
  "track_index": 1,
  "routing_type_name": "Input: All",
  "routing_channel": 0
}
```

**Example response:**

```json
{
  "ok": true,
  "message": "Input routing set (requires routing configuration)",
  "routing_type": "Input: All",
  "routing_channel": 0
}
```
