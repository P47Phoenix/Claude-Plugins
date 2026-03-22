# Security Architecture Patterns

## STRIDE Threat Modeling

STRIDE is a classification framework for security threats. Use it to systematically enumerate what can go wrong at each component in a system.

### Threat Types

**Spoofing**: Pretending to be someone or something else.
- Example: Attacker uses stolen credentials to access an API as a legitimate user.
- Mitigations: Multi-factor authentication, certificate-based identity for services, strong credential policies.

**Tampering**: Modifying data or code without authorization.
- Example: Attacker modifies request payload between client and server to change order total.
- Mitigations: Input validation, message integrity checks (HMAC), digital signatures, immutable audit logs, code signing.

**Repudiation**: Denying an action was taken, with no way to prove otherwise.
- Example: User denies placing an order because there is no audit trail.
- Mitigations: Immutable audit logging with timestamps and user identity, digital signatures on transactions, centralized log aggregation with tamper detection.

**Information Disclosure**: Exposing data to unauthorized parties.
- Example: API error responses include stack traces with database connection strings.
- Mitigations: Encryption in transit and at rest, data classification and access controls, sanitized error responses, data masking in non-production environments.

**Denial of Service**: Making a system unavailable.
- Example: Attacker sends millions of requests to overwhelm the authentication endpoint.
- Mitigations: Rate limiting, auto-scaling, CDN/DDoS protection, circuit breakers, resource quotas per tenant.

**Elevation of Privilege**: Gaining higher access than authorized.
- Example: Regular user manipulates a request parameter to access admin endpoints.
- Mitigations: Server-side authorization checks on every request, principle of least privilege, input validation, role separation.

## Running a Threat Model

### Process

1. **Identify assets**: What are you protecting? Customer data, financial transactions, intellectual property, system availability.
2. **Draw data flow diagram**: Show actors, processes, data stores, data flows, and trust boundaries. Every line crossing a trust boundary is a threat surface.
3. **Enumerate threats per element**: Walk through each element on the DFD. For each, ask: which STRIDE categories apply? Processes are susceptible to all six. Data stores are susceptible to Tampering, Repudiation, Information Disclosure, Denial of Service. Data flows are susceptible to Tampering, Information Disclosure, Denial of Service. External entities are susceptible to Spoofing, Repudiation.
4. **Rate and prioritize**: Use DREAD (Damage, Reproducibility, Exploitability, Affected users, Discoverability) or a simple High/Medium/Low rating. Focus on high-damage, high-exploitability threats first.
5. **Select mitigations**: For each prioritized threat, choose a mitigation. Document the residual risk if the mitigation is partial.

### When to Threat Model

- At architecture design time (before building).
- When adding a new integration or data flow.
- When changing authentication or authorization mechanisms.
- Annually for existing critical systems.

Anti-pattern: threat modeling after the system is built. Most mitigations become 10x more expensive to retrofit.

## Zero Trust Architecture

### Core Principles

- **Never trust, always verify**: No implicit trust based on network location. Internal network traffic is treated with the same suspicion as external.
- **Least privilege**: Grant the minimum access needed for the task, for the minimum duration.
- **Assume breach**: Design as if an attacker is already inside the network. Limit blast radius.

### Implementation Pillars

**Identity**: Strong authentication for all users and services. Continuous verification (not just at login). Identity provider as the central control plane.

**Device**: Assess device health before granting access. Is the device managed? Is it patched? Does it have endpoint protection? Device posture feeds into access decisions.

**Network**: Micro-segmentation. No flat networks. Each workload communicates only with explicitly allowed peers. East-west traffic is filtered and monitored.

**Application**: Per-application access policies. Applications authenticate users independently (not relying on network-level trust). Runtime application self-protection (RASP) for critical apps.

**Data**: Classify data. Encrypt based on classification. Apply access controls at the data layer, not just the application layer. Monitor data access patterns for anomalies.

### Micro-segmentation

Divide the network into small segments, each containing a single workload or small group of related workloads. Define allow-list policies for traffic between segments. Default deny everything else. Implement with: service mesh (Istio, Linkerd), cloud security groups, or network firewalls with identity-aware policies.

## Authentication Patterns

### OAuth 2.0 Flows

**Authorization Code + PKCE**: For public clients (SPAs, mobile apps, CLIs). The client generates a code_verifier, hashes it to a code_challenge, and sends the challenge with the authorization request. The token endpoint verifies the original code_verifier. This prevents authorization code interception attacks.

**Client Credentials**: For service-to-service communication where no user is involved. The client authenticates directly with its client_id and client_secret. Rotate secrets on a schedule (90 days minimum).

**Device Code**: For input-constrained devices (smart TVs, CLI tools). The device displays a code; the user enters it on a separate device with a browser. Poll the token endpoint until the user completes authorization.

### OIDC for Identity

OAuth 2.0 provides authorization (access tokens), not identity. OpenID Connect adds an ID token (JWT) containing user identity claims. Use OIDC when you need to know who the user is, not just what they can access. Validate ID tokens: check signature, issuer, audience, and expiration.

### API Key Management

API keys are shared secrets, not user identity. Use for: server-to-server calls where OAuth is overkill, rate limiting, and usage tracking. Requirements: scope keys to specific APIs/operations, set expiration dates, support rotation without downtime (accept old and new key during rotation window), store hashed (never plaintext), transmit in headers (never in URLs -- URLs appear in logs).

### mTLS for Service-to-Service

Both client and server present certificates. The server verifies the client certificate against a trusted CA. Use for: internal service mesh communication, high-security service-to-service calls. Automate certificate rotation (short-lived certificates via tools like cert-manager or SPIFFE/SPIRE).

### Session Management

**Stateless JWT**: Token contains all session data. No server-side storage. Drawback: cannot revoke individual tokens before expiration. Mitigation: short expiration (15 minutes) with refresh tokens.

**Stateful sessions**: Session ID in a cookie, session data on the server (Redis, database). Supports immediate revocation. Higher infrastructure cost.

**Token refresh**: Access tokens are short-lived (5-15 minutes). Refresh tokens are long-lived (hours to days) and stored securely. Implement refresh token rotation: each use of a refresh token invalidates it and issues a new one. Detect reuse of old refresh tokens as a compromise signal.

## Authorization Patterns

### RBAC (Role-Based Access Control)

Assign permissions to roles, assign roles to users. Simple and effective for most applications. Design: define roles by job function (viewer, editor, admin), define permissions as resource + action pairs (orders:read, orders:write), allow role inheritance (admin inherits editor permissions).

Pitfall: role explosion. If you have more than 15-20 roles, you likely need ABAC.

### ABAC (Attribute-Based Access Control)

Access decisions based on attributes of the user, resource, action, and environment. Example policy: "Allow access if user.department == resource.department AND user.clearance_level >= resource.classification AND time.current is within business_hours."

More flexible than RBAC but harder to reason about. Use when access rules depend on dynamic context, not just static role assignments.

### Policy Engines (OPA Pattern)

Externalize authorization logic into a policy engine. Open Policy Agent (OPA) uses Rego language. Pattern: application sends authorization query (user, action, resource) to OPA. OPA evaluates policies and returns allow/deny. Benefits: policies are version-controlled, testable, and decoupled from application code. Audit: OPA logs every decision.

### Resource-Based Authorization

Authorization is checked against the specific resource, not just the action. Example: "Can user X edit document Y?" requires checking that user X owns document Y or has been granted access. Implement by storing ownership/grants in the resource metadata and checking on every access.

## Data Protection

### Encryption at Rest

Use AES-256 for symmetric encryption. Implement a key hierarchy: data encryption keys (DEKs) encrypt data, key encryption keys (KEKs) encrypt DEKs, master keys protect KEKs. This limits blast radius -- rotating a master key does not require re-encrypting all data.

### Encryption in Transit

TLS 1.3 minimum. Disable TLS 1.0 and 1.1. Certificate management: automate issuance and renewal (Let's Encrypt for external, internal CA for internal). Pin certificates only for mobile apps communicating with known backends, not for general web traffic.

### Tokenization

Replace sensitive data (PII, card numbers) with a non-reversible token. The mapping is stored in a secure token vault. Use for: payment card data (PCI compliance), PII in analytics systems. Unlike encryption, tokenized data cannot be reversed without access to the vault.

### Key Management

Use HSM (Hardware Security Module) or cloud KMS (AWS KMS, GCP KMS, Azure Key Vault) for master key storage. Never store keys alongside the data they protect. Rotation schedule: master keys annually, KEKs quarterly, DEKs as needed. Automate rotation -- manual rotation inevitably lapses.

## API Security

### Rate Limiting

**Sliding window**: Count requests in a rolling time window. Smoother than fixed windows but requires more memory.

**Token bucket**: Tokens accumulate at a steady rate up to a maximum. Each request consumes a token. Allows short bursts while enforcing average rate.

Apply rate limits per: API key, user, IP address, and endpoint. Stricter limits on authentication endpoints (prevent credential stuffing).

### Input Validation

Validate on the server side. Client-side validation is a UX feature, not a security control. Validate: data type, length, range, format (regex for emails/phones), and business rules. Reject unexpected fields. Use an allow-list approach, not a deny-list.

### CORS Configuration

Never use `Access-Control-Allow-Origin: *` for authenticated APIs. Explicitly list allowed origins. Do not reflect the Origin header value without validation. Restrict allowed methods and headers.

### CSP Headers

Content-Security-Policy prevents XSS and data injection. Start with a restrictive policy and loosen as needed: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self' api.example.com`. Report violations to a monitoring endpoint using `report-uri` or `report-to`.

## Audit Logging

### What to Log

- Authentication events: login success/failure, logout, MFA challenge/response.
- Authorization decisions: access granted/denied, with user, resource, and action.
- Data access: reads and writes to sensitive data (confidential and restricted classification).
- Configuration changes: role assignments, policy updates, infrastructure changes.
- Administrative actions: user creation/deletion, privilege escalation.

### Immutable Audit Trails

Audit logs must be append-only. No updates or deletes. Ship logs to a separate system with different access controls (the team that manages the application should not be able to modify its audit logs). Use write-once storage (S3 Object Lock, WORM storage). Hash chain entries for tamper detection.

## OWASP Top 10 -- Architectural Mitigations

| Vulnerability | Architectural Mitigation |
|---------------|-------------------------|
| A01 Broken Access Control | Centralized authorization service, default-deny, server-side enforcement |
| A02 Cryptographic Failures | Encryption at rest and transit by default, key management service, data classification |
| A03 Injection | Parameterized queries enforced at the data access layer, input validation middleware |
| A04 Insecure Design | Threat modeling in design phase, security requirements in acceptance criteria |
| A05 Security Misconfiguration | Infrastructure as code, hardened base images, configuration scanning in CI |
| A06 Vulnerable Components | Dependency scanning in CI/CD, automated patching, SBOM generation |
| A07 Auth Failures | Centralized identity provider, MFA enforcement, session management standards |
| A08 Data Integrity Failures | Code signing, CI/CD pipeline integrity, dependency verification |
| A09 Logging Failures | Centralized logging, immutable audit trails, monitoring and alerting |
| A10 SSRF | Allow-list for outbound requests, network segmentation, disable unnecessary protocols |

## Security Review Checklist for Architecture Designs

1. Are all trust boundaries identified and documented?
2. Is authentication enforced at every entry point (not just the primary)?
3. Is authorization checked on every request, at the resource level?
4. Is data classified, and is protection proportional to classification?
5. Are all data flows encrypted in transit (TLS 1.3)?
6. Is sensitive data encrypted at rest with proper key management?
7. Are secrets (API keys, passwords, certificates) managed through a vault, not in code or config files?
8. Is input validation performed server-side for all external inputs?
9. Are audit logs capturing authentication, authorization, and data access events?
10. Are audit logs immutable and stored separately from the application?
11. Is there a dependency scanning and patching strategy?
12. Are rate limits and abuse protections in place for all public endpoints?
13. Has a threat model been completed for this design?
14. Are there monitoring and alerting rules for security-relevant events?
15. Is the blast radius limited? (If one component is compromised, what else is exposed?)
