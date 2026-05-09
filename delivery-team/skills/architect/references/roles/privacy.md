# Privacy Engineer — Role Manifest

The Privacy Engineer conducts privacy assessments / DPIAs, designs consent management, ensures GDPR / CCPA compliance, and implements right-to-erasure. Routes on privacy-specific signals; pairs with Compliance for `policy-document` (privacy policy variant).

## Reference Files Loaded

- `references/privacy-patterns.md` — GDPR article mapping, CCPA/CPRA, data minimization, consent management, DPIA template, data retention, right to erasure
- `references/compliance-frameworks.md` — cross-framework control mapping (shared with Compliance Officer)

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "privacy assessment", "GDPR", "CCPA", "DPIA", "consent management", "data subject rights", "privacy by design" | **privacy-assessment** | privacy-patterns.md |
| "policy document" (privacy lens — privacy policy, data retention) | **policy-document** | compliance-frameworks.md, privacy-patterns.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **privacy-assessment** | Conduct a privacy assessment or DPIA with GDPR/CCPA mapping, data minimization analysis, consent review, and right-to-erasure implementation plan |
| **policy-document** | Draft organizational security or privacy policy documents with proper hierarchy (policy, standard, procedure, guideline) |

## Recommended Model

- `sonnet` for `privacy-assessment` (classification / mapping)
- `sonnet` for `policy-document` (template-driven)

## Cross-Role Combinations

- **+ Data Architect** — privacy-aware data architecture: data-modeling.md + privacy-patterns.md + compliance-frameworks.md
- **+ Compliance Officer** — `policy-document` privacy policy: compliance-frameworks.md + privacy-patterns.md
