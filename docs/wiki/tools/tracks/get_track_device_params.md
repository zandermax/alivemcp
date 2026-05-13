# get_track_device_params

**Domain:** tracks

**Summary:** Get enriched parameter information for a device on a track (name, raw/display values, ranges, quantization items).

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Iterates `device.parameters` and returns `index`, `name`, `raw_value`, `display_value`, `min`, `max`, `is_quantized`, and `value_items` for each parameter.
**Example request:**
```json
{"action": "get_track_device_params", "track_index": 1, "device_index": 0}
```
**Example response:**
```json
{"ok": true, "track_index": 1, "device_name": "Utility", "count": 3, "parameters": [{"index":0,"name":"Gain","raw_value":0.5,"display_value":"0.5 dB","min":0.0,"max":1.0,"is_quantized":false,"value_items":[]} ] }
```
