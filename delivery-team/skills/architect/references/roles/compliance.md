# Compliance Officer — Role Manifest

The Compliance Officer produces framework checklists (SOC 2, ISO 27001, HIPAA, PCI DSS), audit-readiness artifacts, and policy documents. Shares `security-requirements` / `risk-assessment` task types with the Security Architect; Compliance routes when the lens is framework / audit / policy.

## Reference Files Loaded

- `references/compliance-frameworks.md` — SOC 2, ISO 27001, HIPAA, PCI DSS, audit evidence patterns, cross-framework control mapping
- `references/security-requirements.md` — OWASP Top 10 mapping, authentication, authorization, encryption (shared with Security)

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "compliance checklist", "SOC 2", "ISO 27001", "HIPAA", "PCI DSS", "compliance framework", "regulatory requirements" | **compliance-checklist** | compliance-frameworks.md |
| "audit preparation", "audit evidence", "control mapping", "audit readiness", "compliance audit" | **audit-preparation** | compliance-frameworks.md, security-requirements.md |
| "policy document", "security policy", "data retention policy", "acceptable use policy" | **policy-document** | compliance-frameworks.md (+ privacy-patterns.md when privacy-policy) |
| "security requirements" (framework lens) | **security-requirements** | security-requirements.md, compliance-frameworks.md |
| "risk assessment" (framework lens) | **risk-assessment** | security-patterns.md, compliance-frameworks.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **compliance-checklist** | Produce a compliance checklist for a specific framework (SOC 2, ISO 27001, HIPAA, PCI DSS) with control mappings and evidence requirements |
| **audit-preparation** | Prepare audit readiness artifacts: control mapping, evidence collection plan, gap analysis, and remediation roadmap |
| **policy-document** | Draft organizational security or privacy policy documents with proper hierarchy (policy, standard, procedure, guideline) |

## Recommended Model

- `sonnet` for all Compliance task types (checklist / policy / matrix)

## Cross-Role Combinations

- **+ Security Architect** — `security-requirements` from technical lens: security-requirements.md + security-patterns.md
- **+ Privacy Engineer** — `policy-document` for privacy policy: compliance-frameworks.md + privacy-patterns.md
- **Compliance-driven system design** — architecture-patterns.md + compliance-frameworks.md + security-requirements.md
