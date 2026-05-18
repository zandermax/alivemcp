# 1.1 Fix `check-length` Makefile target

Problem
- `scripts/check_file_length.py` expects file paths; `Makefile` calls it with none.

Plan
1. Update `Makefile` `check-length` target to pass tracked Python files:

```makefile
check-length:
	git ls-files '*.py' | xargs python scripts/check_file_length.py
```
2. Run `make check-length` locally.

Verification
- Target exits non-zero on files > configured length.

Commit message
- fix(make): pass Python files to check-length target
