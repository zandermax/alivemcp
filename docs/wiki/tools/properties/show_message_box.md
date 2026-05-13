Show Message Box

Show a modal message box to the user (Live 12+).

Parameters:
- `message` (string): message body
- `title` (string, optional): dialog title (default: "Message")

Returns:
- `ok`: boolean
- `message`: status message
- `button_pressed`: integer (button id if available)

Example request:
```json
{"action": "show_message_box", "message": "Hello", "title": "Note"}
```
