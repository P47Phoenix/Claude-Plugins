# Security Architect — Role Manifest

The Security Architect produces threat models, security architectures, OWASP-mapped requirements, and risk assessments. Shares `security-requirements` and `risk-assessment` task types with the Compliance Officer; Security routes when the lens is technical / threat-driven, Compliance when the lens is framework / audit-driven.

## Reference Files Loaded

- `references/security-patterns.md` — STRIDE, zero trust, auth patterns, OWASP, threat modeling
- `references/security-requirements.md` — OWASP Top 10 mapping, authentication, authorization, encryption, input validation, secure coding checklist (shared with Compliance Officer)

## Task Types Owned

| Request Signal | Task Type | References Loaded |
|---|---|---|
| "threat model", "security review", "attack surface", "zero trust", "security architecture" | **security-design** | security-patterns.md |
| "security requirements", "OWASP", "secure coding", "encryption requirements", "security NFR", "dependency security" | **security-requirements** | security-requirements.md, security-patterns.md |
| "risk assessment", "risk register", "risk matrix", "threat identification", "risk mitigation" | **risk-assessment** | security-patterns.md, compliance-frameworks.md |

## Task Type Instructions

| Task Type | What the sub-agent does |
|---|---|
| **security-design** | Produce threat models and security architecture with mitigations |
| **security-requirements** | Generate security requirements document with OWASP mapping, authentication/authorization/encryption requirements, and secure coding checklist |
| **risk-assessment** | Produce a risk assessment with threat identification, likelihood/impact scoring, mitigation strategies, and risk register |

## Recommended Model

- `opus` for `security-design` (synthesis)
- `sonnet` for `security-requirements`, `risk-assessment` (checklist / matrix)

## Cross-Role Combinations

- **+ Compliance Officer** — `security-requirements` framework-driven: security-requirements.md + compliance-frameworks.md
- **+ Network/Multiplayer** — multiplayer with security: network-multiplayer.md + security-patterns.md
- **+ Incident Responder** — incident-ready architecture: security-patterns.md + incident-response.md + compliance-frameworks.md
