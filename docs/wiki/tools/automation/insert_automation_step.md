# insert_automation_step

**Domain:** automation

**Summary:** Insert an automation breakpoint/step at a specific time within a clip's automation envelope.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `device_index` (int)
- `param_index` (int)
- `time` (float) — time in beats or clip units
- `value` (float)

**Live mapping:**
- Retrieves `clip.automation_envelope(param)` and calls `envelope.insert_step(time, value)` when available.
**Example request:**
```json
{"action":"insert_automation_step","track_index":0,"clip_index":0,"device_index":0,"param_index":1,"time":1.0,"value":0.7}
```
**Example response:**
```json
{"ok": true, "time":1.0, "value":0.7, "parameter_name":"Gain","message":"Automation step inserted"}
```

**Notes:**
- Validates clip and envelope presence; `insert_step` may not be available in all hosts.

**See also:**
- [remove_automation_step](tools/automation/remove_automation_step.md)
