# 5.3 Make `make all` the single local gate

Plan
1. Ensure `make all` runs `generate-from-wiki`, `validate-manifest`, `validate-wiki`, `validate-docstrings`, `check-length`.
2. Document in `CONTRIBUTING.md` as pre-merge checklist.

Verification
- New contributors run `make all` locally.

Commit message
- docs: document make all as local validation gate
