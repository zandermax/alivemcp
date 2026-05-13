# get_master_chain_summary

Get Master Chain Summary

Get all devices on the master track with enriched parameter lists.

Parameters: None

Returns:
- `ok`: boolean
- `count`: int
- `devices`: list of {index, name, class_name, is_active, parameters}

**Example request:**
```json
{"action": "get_master_chain_summary"}
```

**Example response:**
```json
{"ok": true, "message": "example"}
```
