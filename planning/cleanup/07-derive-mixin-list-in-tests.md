# 3.1 Derive mixin list in `test_live_api_tools.py`

Plan
1. Replace hardcoded mixin list with programmatic derivation from `liveapi_tools.LiveAPITools.__mro__`.
2. Add a test to ensure newly-added mixins surface automatically.

Verification
- Tests adapt to MRO changes without manual edits.

Commit message
- test: derive expected mixin list from LiveAPITools.__mro__
