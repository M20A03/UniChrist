---
name: security-audit
description: >-
  Audits code and infrastructure against Garry Tan CSO checklist, Trail of Bits guidelines,
  STIX threat models, ClamAV scanning, and OWASP Top 10.
---

# 🛡️ Security Audit & Hardening Skill

Based on `garrytan/gstack/cso`, `Trail of Bits`, and `S.T.I.X`.

## Checklist:
1. **Zero Secret Leakage:** Scan for unencrypted API keys, database connection strings, or JWT secrets in git history.
2. **SQL Injection Defense:** All SQL statements parameterized or executed with strict type checking.
3. **RBAC & Authorization:** Every protected route verifies user token and active status.
4. **Header Hardening:** Enforce CSP, HSTS, X-Content-Type-Options: nosniff, X-Frame-Options: DENY.
