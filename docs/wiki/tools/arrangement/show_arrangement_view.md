# show_arrangement_view

**Domain:** arrangement (view)

**Summary:** Switch UI to the Arrangement view when supported.

**Parameters:**
- none

**Live mapping:**
- Uses `Live.Application.get_application().view.show_view("Arranger")` when view control exists.
**Example request:**
```json
{"action":"show_arrangement_view"}
```
**Example response:**
```json
{"ok": true, "message":"Showing arrangement view"}
```
