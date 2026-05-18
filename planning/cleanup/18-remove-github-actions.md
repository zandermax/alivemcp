# 5.4 Remove GitHub Actions if chosen

Plan
1. If repo policy is no CI: delete `.github/workflows/check-wiki-parity.yml` and update docs that mention it.
2. Otherwise keep workflow and ensure `make all` is primary local gate.

Verification
- `.github/workflows` state matches repo policy.

Commit message
- chore(ci): remove check-wiki-parity workflow (if no-CI policy)
