# Step 3: Draft (Parallel — 5 Roles)

**Begin**: `[3/6] Drafting slide content... ({N} roles contributing{, light mode if active})`

In **light mode**: only required roles are dispatched. Optional/enhancing role slots are skipped. The role count in the progress indicator reflects the reduced set.

Dispatch sub-agents **in parallel** based on the outline's role assignments. Only dispatch roles that have assigned slides.

| Sub-agent | Skill | Contributes |
|-----------|-------|-------------|
| Product Owner | `delivery-team:product-delivery` | Narrative slides (goals, priorities, next steps) |
| Data Analyst | `delivery-team:product-delivery` | Metric slides (velocity, completion, trends) |
| Developer | `delivery-team:developer` | Feature slides (implementation highlights) |
| Architect | `delivery-team:architect` | Architecture slides (decisions, diagrams) |
| QA Engineer | `delivery-team:quality` | Quality slides (test results, defect data) |

Each sub-agent receives:
- Its assigned slide numbers and titles from the outline
- Paths to its relevant source artifacts only
- Presentation type, audience mode, and content rules

Each sub-agent writes output to: `.delivery/artifacts/presentations/.drafts/{role}-slides.md`

**Content rules for all sub-agents**:
- Every data point must cite its source artifact
- Missing data: use `[TBD]` — never fabricate
- Stay within assigned slide scope
- Write at the detail level appropriate for audience

Show the user which roles contribute to which slides (progress indicator), then proceed silently.

**Complete**: `Draft complete: {role names} contributed {N} slides`
