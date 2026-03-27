# Security Policy — {project-name}

---

## 0. Agent Context

| Campo | Valor |
|-------|-------|
| **Supported Versions** | See §1 |
| **Report via** | {security-email} |
| **Response SLA** | 48h acknowledgment, 7 days triage |

---

## 1. Supported Versions

| Version | Supported |
|---------|-----------|
| {latest} | ✅ |
| {previous} | 🟡 Critical only |
| Older | ❌ |

---

## 2. Reporting a Vulnerability

**Please do NOT report security vulnerabilities through public GitHub issues.**

To report a vulnerability:

1. **Email:** {security-email}
2. **Subject line:** `[SECURITY] {Brief description}`
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

**We will:**
- Acknowledge receipt within **48 hours**
- Provide triage status within **7 days**
- Notify you when the fix is released

---

## 3. Security Practices

### Authentication & Authorization
- [ ] JWT tokens with short expiration (≤ 24h)
- [ ] Refresh token rotation
- [ ] Role-based access control (RBAC)
- [ ] Rate limiting on auth endpoints

### Data Protection
- [ ] All secrets in environment variables (never in code)
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced in all environments (staging + prod)

### LGPD / GDPR Compliance
- [ ] Data minimization — collect only what's needed
- [ ] User consent mechanism
- [ ] Right to data deletion implemented
- [ ] Data processing documented

### Dependencies
- [ ] Automated dependency scanning (Dependabot / Snyk)
- [ ] No known critical vulnerabilities in production dependencies
- [ ] Regular dependency updates scheduled

### Infrastructure
- [ ] Principle of least privilege on all services
- [ ] Secrets managed via vault / environment secrets (not plaintext)
- [ ] Logs do not contain PII or secrets

---

## 4. Security Checklist (Pre-Deploy)

> Executado na Phase 5.5 (Security Review Gate) antes de cada release.

- [ ] OWASP Top 10 reviewed
- [ ] No hardcoded secrets (`grep -r "secret\|password\|key" src/ --include="*.js,*.ts,*.py"`)
- [ ] Dependencies scanned (`npm audit` / `pip-audit` / `trivy`)
- [ ] Auth endpoints rate-limited
- [ ] Input validation on all endpoints
- [ ] SQL injection protection verified
- [ ] XSS protection verified (CSP headers configured)
- [ ] CORS configured correctly (not `*` in production)

---

## 5. Disclosure Policy

We follow responsible disclosure. Once a vulnerability is fixed, we will:

1. Release a patched version
2. Credit the reporter (unless anonymity is requested)
3. Publish advisory in CHANGELOG.md under `### Security`

---

*Last updated: YYYY-MM-DD*
