# 4.2 Add centralized result builders

Plan
1. Implement `ok_result(**fields)` and `err_result(e)` in `ALiveMCP_Remote/tools/core/base.py` or a new helper module.
2. Migrate a small subset of tools as proof; land rest incrementally.

Verification
- Tools continue to return expected fields; fewer duplicated patterns.

Commit message
- refactor(core): add ok_result and err_result helpers
