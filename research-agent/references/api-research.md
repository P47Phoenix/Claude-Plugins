# API Research Patterns

Reference guide for evaluating APIs, SDKs, and integration approaches.

## API Evaluation Dimensions

### 1. Authentication & Authorization

| Aspect | Questions to Answer | Evidence Sources |
|--------|---------------------|------------------|
| Auth Method | OAuth2, API Key, JWT, mTLS? | Official docs, OpenAPI spec |
| Token Lifecycle | Expiration, refresh mechanism? | Auth documentation |
| Scopes/Permissions | Granularity of access control? | API reference |
| Rate Limiting by Auth | Different limits per auth tier? | Rate limit docs |

### 2. Rate Limiting & Quotas

| Aspect | Questions to Answer | Evidence Sources |
|--------|---------------------|------------------|
| Request Limits | Requests per second/minute/day? | Rate limit headers, docs |
| Quota Types | Per-endpoint, global, per-user? | API documentation |
| Retry Strategy | Backoff recommendations? | Error handling docs |
| Burst Handling | Burst capacity vs sustained? | Performance docs |

### 3. Error Handling

| Aspect | Questions to Answer | Evidence Sources |
|--------|---------------------|------------------|
| Error Format | Standard format (RFC 7807, custom)? | Error response examples |
| Error Codes | Documented error codes list? | API reference |
| Retry Guidance | Which errors are retryable? | Error handling docs |
| Degradation | Graceful degradation patterns? | Best practices docs |

### 4. SDK Quality Assessment

| Aspect | Questions to Answer | Evidence Sources |
|--------|---------------------|------------------|
| Official SDKs | Languages supported officially? | SDK documentation |
| Maintenance | Last update, open issues count? | GitHub repo |
| Type Safety | TypeScript/type definitions? | Package inspection |
| Documentation | Quickstart, examples, API docs? | SDK readme |
| Dependencies | Dependency count, security? | Package manifest |

### 5. Versioning & Stability

| Aspect | Questions to Answer | Evidence Sources |
|--------|---------------------|------------------|
| Version Strategy | URL path, header, query param? | API documentation |
| Deprecation Policy | Notice period, migration guides? | Changelog, announcements |
| Breaking Changes | History of breaking changes? | Changelog, release notes |
| SLA/Uptime | Availability guarantees? | SLA documentation |

### 6. Documentation Quality

| Aspect | Questions to Answer | Evidence Sources |
|--------|---------------------|------------------|
| Completeness | All endpoints documented? | API reference |
| Examples | Request/response examples? | Documentation |
| Changelog | Detailed change history? | Changelog |
| OpenAPI/Swagger | Machine-readable spec available? | API spec endpoint |

## API Comparison Template

```markdown
## API Comparison: [Topic]

### Overview
| Criteria | API A | API B | API C |
|----------|-------|-------|-------|
| Auth Method | | | |
| Rate Limits | | | |
| SDK Languages | | | |
| Pricing Model | | | |
| Documentation Score | | | |

### Authentication Comparison
...

### Rate Limiting Comparison
...

### SDK Quality Comparison
...

### Recommendation
Based on [criteria], recommend [API] because:
- ...
- ...

Risks:
- ...
```

## Common API Research Queries

### Discovery Queries
- `<service> API documentation`
- `<service> OpenAPI spec`
- `<service> API rate limits`
- `<service> SDK <language>`

### Evaluation Queries
- `<service> API vs <competitor> API`
- `<service> API reliability issues`
- `<service> API breaking changes`
- `<service> API migration guide`

### Implementation Queries
- `<service> API authentication example`
- `<service> API error handling best practices`
- `<service> API pagination`
- `<service> webhook setup`

## API Documentation Red Flags

Flag these issues when found:

- Missing error code documentation
- No rate limit information
- Outdated SDK (>1 year without updates)
- No versioning strategy documented
- Missing authentication examples
- No changelog or release notes
- Broken example code
- Inconsistent endpoint naming

---

## PICO Application for API Evaluation

Use PICO framing to sharpen API evaluation questions before research begins.

**Mapping API concepts to PICO:**

| PICO Component | API Research Equivalent | Example |
|----------------|------------------------|---------|
| Population (P) | The application or team context | "Node.js microservices handling 10k req/min" |
| Intervention (I) | The API or SDK being evaluated | "Stripe Payments API with official Node SDK" |
| Comparison (C) | The alternative or current approach | "vs. Braintree API / vs. custom payment handling" |
| Outcome (O) | The measurable success criteria | "Integration time, error rate, ongoing maintenance burden" |

**Example reformulated question:**
> "In Node.js microservices handling 10k req/min (P), does the Stripe Payments API with official Node SDK (I) compared to Braintree API (C) result in lower integration time and error rate (O)?"

This forces explicit success criteria before gathering evidence, preventing post-hoc rationalization of a preferred API.

**When PICO doesn't fit:** Pure discovery questions ("what payment APIs exist?") are Descriptive research — skip PICO and use the Landscape Map pattern instead.

---

## API-Specific Bias Detection

Apply these bias checks during the Bias Audit phase (Phase 7) when researching APIs:

### Vendor Documentation Bias
- **Risk:** Official docs emphasize happy-path scenarios; failure modes, edge cases, and breaking change history are underrepresented
- **Mitigation:** Seek community reports (GitHub issues, Stack Overflow, HN discussions) to surface real-world friction
- **Flag:** "Documentation source is 100% vendor-produced — community validation absent [BIAS RISK: vendor documentation]"

### Recency Bias in Version Examples
- **Risk:** Code examples may be for an older SDK version; behavior described may not apply to current release
- **Mitigation:** Always check the example's SDK version against the current release; look at changelog for breaking changes between them
- **Flag:** If example SDK version differs from current by a major version: "[BIAS RISK: recency — example uses v{X}, current is v{Y}]"

### Selection Bias in Comparisons
- **Risk:** Comparison criteria chosen after seeing the results (cherry-picking metrics where preferred API wins)
- **Mitigation:** Define evaluation criteria (PICO outcome) before gathering evidence; document criteria in Phase 3 Scope Definition
- **Flag:** If criteria were added mid-research: "[BIAS RISK: selection — criterion added after initial findings]"

### Availability Bias
- **Risk:** Well-documented APIs appear superior because more evidence is findable, not because they are actually better
- **Mitigation:** Distinguish evidence quantity from evidence quality; note when low evidence count reflects poor documentation, not poor API quality
- **Flag:** "Low source count for [API B] may reflect documentation gaps rather than quality differences [BIAS RISK: availability]"

---

## Evidence Grading for API Research (4-Level GRADE)

| GRADE | Symbol | API Research Criteria |
|-------|--------|-----------------------|
| High | ⊕⊕⊕⊕ | Official documentation + working code sample confirmed against current SDK version + independent community validation |
| Moderate | ⊕⊕⊕◯ | Official documentation only (current version), or community-validated workarounds for documented gaps |
| Low | ⊕⊕◯◯ | Documentation for a prior major version, or a single community source without official corroboration |
| Very Low | ⊕◯◯◯ | Forum post, unofficial blog, or conflicting information across sources |
