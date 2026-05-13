# clear_automation_envelope

**Domain:** automation

**Summary:** Remove all automation data for a device parameter's envelope inside a clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `device_index` (int)
- `param_index` (int)

**Live mapping:**
- Uses `clip.clear_envelope(param)` when supported to clear envelope data.
**Example request:**
```json
{"action":"clear_automation_envelope","track_index":0,"clip_index":0,"device_index":0,"param_index":1}
```
**Example response:**
```json
{"ok": true, "parameter_name":"Cutoff","message":"Automation envelope cleared"}
```

**Notes:**
- Host may not implement `clear_envelope`; function validates and errors if unavailable.

**See also:**
- [get_clip_automation_envelope](tools/automation/get_clip_automation_envelope.md)
