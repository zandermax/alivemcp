---
name: "get_browser_items"
summary: ""
Live mapping: "- Returns a set of available categories and a message noting limitations."
---

# get_browser_items

**Domain:** arrangement (browser)

**Summary:** Get available browser categories or items (limited by LiveAPI).

**Parameters:**

- `category` (string, optional)

**Live mapping:**

- Returns a set of available categories and a message noting limitations.
  **Example request:**

```json
{ "action": "get_browser_items", "category": "devices" }
```

**Example response:**

```json
{
  "ok": true,
  "category": "devices",
  "available_categories": ["devices", "plugins"],
  "message": "Browser item enumeration is limited in LiveAPI"
}
```
