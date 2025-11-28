# Security Policy

We take the security of the unofficial CourtListener SDK seriously. This document explains how to report vulnerabilities, what to expect from us, and how we automate security checks inside this repository.

## Supported Versions

| Version  | Supported |
|----------|-----------|
| `main`   | ✅
| Released tags within the past 6 months | ✅
| Anything older | ⚠️ Best effort only |

Security fixes are developed on `main` first, then cherry-picked into the most recent tagged release when needed.

## Reporting a Vulnerability

1. **Use GitHub Security Advisories (preferred):**
   - Navigate to the repository Security tab → “Report a vulnerability”.
   - Provide a minimal reproduction, impacted versions, and suggested fixes if available.
2. **Email fallback:**
   - If you cannot access GitHub, email `guesswho@rizzn.com` with the subject line `SECURITY REPORT: courtlistener-sdk`.
   - Encrypt with PGP if desired (key fingerprints available on request).

Please avoid creating public issues or pull requests for unresolved vulnerabilities. We will coordinate a private fix and disclosure timeline with you before anything is published.

## Response & Remediation SLAs

| Severity | Acknowledgement | Initial Fix ETA |
|----------|-----------------|-----------------|
| Critical | 24 hours        | 7 days          |
| High     | 2 business days | 14 days         |
| Medium   | 5 business days | 30 days         |
| Low      | 5 business days | Best effort     |

We will keep reporters updated weekly (or more frequently for Critical issues) until remediation is available.

## Automated Security Tooling

- `Security Audits` workflow runs `pip-audit` and `composer audit` on every push/PR and nightly, ensuring dependency advisories fail fast.
- `CodeQL` workflow runs static analysis for both the Python and PHP SDKs. Findings surface in the GitHub Security tab and block regressions via pull-request annotations.
- Dependabot is enabled for the `pip` and Composer ecosystems to keep transitive dependencies patched via automated PRs.

If you need more information about a specific security control or would like to coordinate on disclosure timing, please email us at `guesswho@rizzn.com`.
