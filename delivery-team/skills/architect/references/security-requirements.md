# Security Requirements Reference

## OWASP Top 10 Mapped to Requirements

| Vulnerability | Security Requirement | Implementation Guidance |
|--------------|---------------------|------------------------|
| A01: Broken Access Control | Enforce least privilege; deny by default | Use server-side access control; validate permissions on every request; disable directory listing; log access failures |
| A02: Cryptographic Failures | Protect data at rest and in transit | Classify data by sensitivity; use TLS 1.2+ for transit; AES-256 for storage; never use deprecated algorithms (MD5, SHA1, DES) |
| A03: Injection | Validate and sanitize all input | Use parameterized queries; use ORM safely; apply allowlist input validation; escape output for context |
| A04: Insecure Design | Build security into design phase | Threat model during design; use secure design patterns; establish security user stories; define abuse cases |
| A05: Security Misconfiguration | Harden all environments consistently | Automate hardening; remove unused features; review cloud permissions; use security headers; disable debug in production |
| A06: Vulnerable Components | Track and update all dependencies | Maintain software bill of materials (SBOM); automate vulnerability scanning; establish patch SLAs by severity |
| A07: Auth Failures | Implement robust authentication | Use proven auth frameworks; enforce MFA; prevent credential stuffing; use secure password storage (bcrypt/argon2) |
| A08: Data Integrity Failures | Verify software and data integrity | Use digital signatures; verify CI/CD pipeline integrity; validate serialized data; use trusted repositories |
| A09: Logging Failures | Log security events comprehensively | Log auth events, access control failures, input validation failures; ensure logs are tamper-resistant; integrate with SIEM |
| A10: SSRF | Validate and restrict outbound requests | Sanitize URLs; use allowlists for outbound destinations; block internal network ranges; disable HTTP redirects |

---

## Authentication Requirements

### Multi-Factor Authentication (MFA)
- Required for all privileged accounts and administrative access
- Required for remote access and VPN connections
- Supported methods: TOTP, hardware tokens (FIDO2/WebAuthn), push notifications
- SMS-based MFA is acceptable only as fallback; prefer phishing-resistant methods
- Recovery flow must verify identity through alternate channel

### Password Policies
- Minimum 12 characters for standard users, 16 for privileged accounts
- No maximum length below 64 characters
- Check against known breached password databases (HIBP API or local list)
- No forced periodic rotation (NIST 800-63B guidance)
- Require password change only on evidence of compromise
- Store using adaptive hashing: Argon2id (preferred), bcrypt (minimum cost 10), scrypt

### Session Management
- Generate cryptographically random session identifiers (minimum 128 bits entropy)
- Set session timeout: 15 minutes idle for sensitive apps, 30 minutes for standard
- Absolute session lifetime: 8-12 hours maximum
- Invalidate session on logout, password change, and privilege escalation
- Bind session to client attributes (IP range, user agent) where feasible
- Use secure cookie attributes: Secure, HttpOnly, SameSite=Strict

### Account Lockout
- Lock after 5 consecutive failed attempts
- Progressive delay: 1min, 5min, 15min, 1hr
- Notify user of failed login attempts
- Admin unlock capability with identity verification
- Separate lockout counters per authentication method

---

## Authorization Requirements

### Principle of Least Privilege
- Grant minimum permissions required for each role
- Default deny: all access not explicitly granted is denied
- Separate read, write, delete, and admin permissions
- No shared or generic accounts for production systems
- Service accounts must have scoped permissions with no interactive login

### Role Definition
- Document each role with its permissions and justification
- Maximum 3 levels of privilege escalation from base user to admin
- Implement separation of duties for critical operations (e.g., deploy + approve)
- Role assignments require manager approval and documented business justification
- Privileged roles require additional background verification

### Access Review Cadence
- Quarterly review of all privileged access
- Semi-annual review of standard user access
- Immediate review on role change, transfer, or termination
- Automated deprovisioning within 24 hours of termination
- Annual review of service account permissions and necessity

---

## Encryption Requirements

### Data at Rest
- AES-256 (GCM mode preferred) for structured data
- Full-disk encryption for all endpoints and servers
- Database-level encryption with application-managed keys (not just TDE)
- Encrypt backups with separate key from production
- Sensitive fields (PII, credentials) encrypted at application layer

### Data in Transit
- TLS 1.2 minimum; TLS 1.3 preferred
- Disable SSL 2.0/3.0, TLS 1.0/1.1
- Use strong cipher suites: ECDHE key exchange, AES-GCM or ChaCha20
- Enable HSTS with minimum 1-year max-age and includeSubDomains
- Certificate pinning for mobile applications and critical API integrations
- Mutual TLS (mTLS) for service-to-service communication

### Key Management
- Use a dedicated key management system (KMS) or HSM
- Rotate encryption keys annually; rotate signing keys per policy
- Separate key custodians (no single person controls a key)
- Key backup and recovery procedures documented and tested
- Immediate key rotation on suspected compromise
- Distinct keys per environment (dev, staging, production)

---

## Input Validation Requirements

### Allowlist vs Denylist
- Prefer allowlist validation: define what IS allowed, reject everything else
- Denylist only as defense-in-depth layer, never as primary control
- Validate data type, length, range, and format on server side
- Client-side validation is for UX only; never trust it for security

### Parameterized Queries
- All database queries must use parameterized statements or prepared statements
- No string concatenation for SQL, LDAP, or XPath queries
- ORM usage must be reviewed for raw query escape hatches
- Stored procedures must use parameterized inputs internally

### Output Encoding
- Encode output based on context: HTML, JavaScript, URL, CSS, LDAP
- Use framework-provided encoding functions; do not write custom encoders
- Apply Content-Type headers correctly; set charset explicitly
- Implement Content Security Policy (CSP) headers to mitigate XSS

---

## Secure Coding Checklist

1. Validate all input on the server side (type, length, range, format)
2. Use parameterized queries for all database operations
3. Encode output based on rendering context
4. Use framework-provided authentication and session management
5. Apply principle of least privilege in all authorization checks
6. Log security-relevant events with sufficient detail (no sensitive data in logs)
7. Handle errors securely: generic messages to users, detailed logs internally
8. Use cryptographically secure random number generators
9. Keep secrets out of source code; use environment variables or secret managers
10. Validate and sanitize file uploads (type, size, content, storage location)
11. Set security headers (CSP, HSTS, X-Content-Type-Options, X-Frame-Options)
12. Disable debug modes and verbose error output in production
13. Implement rate limiting on authentication and sensitive endpoints
14. Validate redirect URLs against an allowlist
15. Use SRI (Subresource Integrity) for third-party scripts and stylesheets
16. Review third-party dependencies for known vulnerabilities before adoption
17. Implement CSRF protection on all state-changing operations
18. Sanitize data before logging to prevent log injection

---

## Security NFR Template

| Req ID | Category | Requirement | Priority | Verification Method |
|--------|----------|-------------|----------|-------------------|
| SEC-001 | Authentication | All user authentication must support MFA | P1 | Security test, configuration audit |
| SEC-002 | Encryption | All data in transit must use TLS 1.2+ | P1 | TLS scan (ssllabs, testssl.sh) |
| SEC-003 | Encryption | PII at rest must be encrypted with AES-256 | P1 | Code review, data audit |
| SEC-004 | Access Control | API endpoints must enforce RBAC | P1 | Penetration test, code review |
| SEC-005 | Logging | Security events must be logged within 5 seconds | P2 | Log pipeline test |
| SEC-006 | Input Validation | All inputs must be validated server-side | P1 | SAST scan, code review |
| SEC-007 | Session | Idle sessions must timeout after 15 minutes | P2 | Functional test |
| SEC-008 | Dependencies | No known critical/high CVEs in production dependencies | P1 | SCA scan (Snyk, Dependabot) |

Use this template as a starting point. Extend with project-specific requirements based on threat model findings and compliance obligations.

---

## Dependency Security

### Vulnerability Scanning
- Integrate SCA (Software Composition Analysis) into CI/CD pipeline
- Block builds with critical or high severity vulnerabilities
- Generate and maintain SBOM (Software Bill of Materials)
- Monitor for new CVEs against deployed dependency versions

### Update Policy
- Critical CVEs: patch within 48 hours
- High CVEs: patch within 7 days
- Medium CVEs: patch within 30 days
- Low CVEs: patch in next regular release cycle
- Track exceptions with documented risk acceptance and expiry date

### SCA Tools
- Dependabot / Renovate for automated dependency updates
- Snyk, Grype, or Trivy for vulnerability scanning
- OWASP Dependency-Check for build-time analysis
- Socket.dev or similar for supply chain risk detection
- Lock files must be committed and reviewed for unexpected changes
