# Security Policy

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

If you discover a security issue (e.g. a way to bypass webhook signature verification, expose API keys, or cause arbitrary code execution), please report it privately:

1. Go to the **Security** tab of this repository
2. Click **Report a vulnerability**
3. Describe the issue, steps to reproduce, and potential impact

You can expect an acknowledgement within 48 hours and a fix within 14 days for confirmed issues.

## What counts as a security issue

- Bypassing HMAC-SHA256 webhook signature verification
- API key or secret leakage
- Server-side code injection via PR diff content
- Unsafe deserialisation
- Dependency with a known CVE

## Supported versions

Only the latest version on the `main` branch receives security fixes.
