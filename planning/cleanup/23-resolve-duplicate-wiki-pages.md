# 6.8 Resolve duplicate wiki pages

Plan
1. Find duplicates (e.g., `clips/get_clip_notes.md` vs `midi/get_clip_notes.md`).
2. Pick canonical location, delete duplicate, add redirect note in kept page.

Verification
- `maint/verify_docs_tools.py` passes with canonical set.

Commit message
- docs: remove duplicate wiki page and add redirect note
