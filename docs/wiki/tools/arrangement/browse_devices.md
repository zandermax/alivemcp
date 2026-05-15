---
name: "browse_devices"
summary: ""
Live mapping: "- Returns a set of device type category names (instrument, audio effect, etc.) — browser enumeration is limited via LiveAPI."
---

# browse_devices

**Domain:** arrangement (browser)

**Summary:** Return a small, curated list of device type categories reported by the browser layer.

**Parameters:**

- none

**Live mapping:**

- Returns a set of device type category names (instrument, audio effect, etc.) — browser enumeration is limited via LiveAPI.
  **Example request:**

```json
{ "action": "browse_devices" }
```

**Example response:**

```json
{ "ok": true, "device_types": ["Instrument", "Audio Effect"], "count": 2 }
```
