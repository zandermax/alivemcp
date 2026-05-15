---
name: "get_all_param_display_values"
summary: ""
Live mapping: "- Iterates `device.parameters`, collects `index`, `name`, `raw_value`, `display_value`, `min`, `max`, `is_quantized`, and `value_items`."
---

# get_all_param_display_values

**Domain:** devices

**Summary:** Return an enriched parameter list for a device including display strings, ranges and quantized items.

**Parameters:**

- `track_index` (int)
- `device_index` (int)

**Live mapping:**

- Iterates `device.parameters`, collects `index`, `name`, `raw_value`, `display_value`, `min`, `max`, `is_quantized`, and `value_items`.
  **Example request:**

```json
{
  "action": "get_all_param_display_values",
  "track_index": 1,
  "device_index": 0
}
```

**Example response:**

```json
{
  "ok": true,
  "device_name": "EQ",
  "count": 3,
  "parameters": [
    {
      "index": 0,
      "name": "Freq",
      "raw_value": 440.0,
      "display_value": "440 Hz",
      "min": 20.0,
      "max": 20000.0,
      "is_quantized": false,
      "value_items": []
    }
  ]
}
```

**Notes:**

- Useful for UIs that need fully formatted parameter metadata from the host.
