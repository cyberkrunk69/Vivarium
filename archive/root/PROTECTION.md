# Branch Protection Guidelines

- Protect the `main` branch.
- Require the following status checks before merging:
  - `CI / build` (the workflow defined in `.github/workflows/ci.yml`).
- Disallow force pushes and deletions.