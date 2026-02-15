# Security Policy

## Supported Versions

Only the default branch is actively maintained with security updates.

## Reporting a Vulnerability

Please **do not** open a public issue. Instead, use GitHub Security Advisories:

1. Go to the repository **Security** tab.
2. Click **Report a vulnerability**.
3. Provide details and steps to reproduce.

The gatekeeper (**@cyberkrunk69**) will respond as soon as possible.

## Repository Control Model

- Final merge authority is retained by **@cyberkrunk69**.
- All paths are code-owner protected via `.github/CODEOWNERS`.
- Policy-critical paths (`.github/workflows/**`, policy scripts/templates) are owner-controlled.
- CI policy checks run through **Policy Guard** workflow to prevent silent weakening of standards.

## Branch Protection Enforcement

Apply repository-level branch protections (required checks, required reviews, owner-only direct push restrictions) with:

```bash
./devtools/apply-branch-protection.sh
```

This requires repository admin privileges through authenticated `gh`.
