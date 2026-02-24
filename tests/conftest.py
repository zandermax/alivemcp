"""
Pytest configuration and shared fixtures.

The `Live` module is only available inside the Ableton runtime, so we stub it
out here before any project code is imported. All test files inherit this
automatically — no explicit import needed.
"""

import sys
from unittest.mock import MagicMock

sys.modules["Live"] = MagicMock()
