# create_automation_envelope

**Domain:** automation

**Summary:** Create an automation envelope for a device parameter inside a clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `device_index` (int)
- `param_index` (int)

**Live mapping:**
- Calls `clip.create_automation_envelope(param)` when supported by the host.
**Example request:**
```json
{"action":"create_automation_envelope","track_index":0,"clip_index":0,"device_index":0,"param_index":1}
```
**Example response:**
```json
{"ok": true, "parameter_name":"Resonance","device_name":"EQ Eight","message":"Automation envelope created"}
```

**Notes:**
- Validates clip presence and that `create_automation_envelope` is implemented by the host.

**See also:**
- [get_clip_automation_envelope](tools/automation/get_clip_automation_envelope.md)
