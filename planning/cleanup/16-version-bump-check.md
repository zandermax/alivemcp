# 5.2 Strengthen version-bump check

Plan
1. Move `check-version-bump` to a pre-commit/pre-push script that cannot easily be skipped.
2. Document `make release` procedure that includes version-check.

Verification
- Version bump check runs as part of release flow.

Commit message
- chore(release): strengthen version bump check and docs
