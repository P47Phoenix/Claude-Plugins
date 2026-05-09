# Step 2: Content Gate (Automated)

**Begin**: `[2/6] Validating source artifacts... ({N} required, {M} enhancing to check)`

Validate required artifacts exist per type:

| Type | Required | Enhancing (optional) |
|------|----------|---------------------|
| Sprint Review | Sprint plan, UAT report/completion data | FKCs, metrics, retrospective, defect log |
| Feature Pitch | Idea brief or PRD | Architecture overview, competitive analysis |
| Stakeholder Update | Pipeline state, sprint plan/progress | Risk register, metrics, retrospective |
| Technical Deep-Dive | At least 1 architecture doc or ADR | Design decisions, code examples |
| Investor Pitch | Idea brief or PRD, traction/metrics data | Competitive analysis, financial projections, team bios |
| Roadmap | Sprint plan or backlog, pipeline state | Architecture roadmap, risk register, resource allocation |
| Product Demo | At least 1 feature artifact (FKC, implementation doc, or UAT report) | Screenshots, user feedback, metrics |
| Onboarding | Architecture overview or system documentation, at least 1 ADR or design decision doc | Team topology, dev environment setup, glossary |
| Retrospective Summary | Retrospective notes or action items | Velocity trends, defect data, previous retro actions |

**Gate rules**:
- Missing required artifact: **STOP**. List what is missing, where it should be, how to create it.
- Empty/placeholder artifact: **WARN** + ask user to confirm proceeding.
- Stale artifact (>`staleness_warning_days`, default 7): **WARN** but proceed with notice.

On PASS, show what was found (required + enhancing) and any warnings.

**Complete**: `Content gate passed: {N} required found, {M} enhancing found, {W} warnings`
