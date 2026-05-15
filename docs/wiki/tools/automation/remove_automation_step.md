---
name: "remove_automation_step"
summary: ""
Live mapping: "- Uses `clip.automation_envelope(param).remove_step(time)` when supported."
---

# remove_automation_step

**Domain:** automation

**Summary:** Remove an automation breakpoint/step at a specific time within a clip's automation envelope.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)
- `device_index` (int)
- `param_index` (int)
- `time` (float)

**Live mapping:**

- Uses `clip.automation_envelope(param).remove_step(time)` when supported.
  **Example request:**

```json
{
  "action": "remove_automation_step",
  "track_index": 0,
  "clip_index": 0,
  "device_index": 0,
  "param_index": 1,
  "time": 1.0
}
```

**Example response:**

```json
{
  "ok": true,
  "time": 1.0,
  "parameter_name": "Gain",
  "message": "Automation step removed"
}
```

**Notes:**

- Validates presence of clip and envelope; returns an error if removal function is unavailable.

**See also:**

- [insert_automation_step](tools/automation/insert_automation_step.md)
