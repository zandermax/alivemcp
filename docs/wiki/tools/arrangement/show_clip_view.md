---
name: "show_clip_view"
summary: ""
Live mapping: '- Uses `Live.Application.get_application().view.show_view("Session")` when view control exists.'
---

# show_clip_view

**Domain:** arrangement (view)

**Summary:** Switch UI to the Session/Clip view when supported.

**Parameters:**

- none

**Live mapping:**

- Uses `Live.Application.get_application().view.show_view("Session")` when view control exists.
  **Example request:**

```json
{ "action": "show_clip_view" }
```

**Example response:**

```json
{ "ok": true, "message": "Showing clip/session view" }
```
