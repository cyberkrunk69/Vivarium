# Contributing

Thanks for contributing! This repository is public but gated: all changes must
be reviewed and approved before they can land.

## Access Policy (Public Repo)

- All changes must be proposed via **pull requests**.
- **@cyberkrunk69** is the code owner and must approve before merge.
- Direct pushes to protected branches are not allowed.
- Use **PR review suggestions** for changes; maintainers apply or approve them.

## Local Setup

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Test Suite

Before committing any changes, ensure the full test suite passes:

```bash
pytest
```

If you have installed the repository’s Git hooks (see the README), this will be
executed automatically on every `git commit`.

## Pre-commit Hook

A lightweight pre-commit hook is provided in `.githooks/pre-commit`. To enable it:

```bash
ln -s ../../.githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This hook will block any commit that fails the test suite, ensuring that no code
reaches the remote repository without passing tests.

## CI Checks

All pull requests trigger GitHub Actions workflows defined in
`.github/workflows/`. The repository’s branch protection rules should require
these checks to pass before a merge is allowed.