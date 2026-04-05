# Sprint Plan: Comprehensive Documentation Site

**Version**: 1.0
**Date**: 2026-04-04
**Scrum Master**: Aragorn
**Idea Brief**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Stories**: `.delivery/artifacts/05-plan/po/stories.md` v1.0 (GOVERNING)
**Issue**: #48
**Team Size**: 1 developer (Technical Writer / DevOps)
**Pipeline Type**: DOCS_ONLY

---

> *"The road is long, but it is a road of words, not war. Thirty pages of documentation, one configuration file, one deployment workflow. We have walked harder paths. Let us walk this one with discipline."*

---

## 1. Sprint Goal

**Build and deploy a comprehensive MkDocs Material documentation site for the delivery-team plugin, covering all 11 skills, 7-stage pipeline, configuration reference, hooks, alias themes, architecture, and contributor guide — auto-deployed to GitHub Pages from `main`.**

---

## 2. Capacity Declaration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Team size | 1 contributor | Solo — Technical Writer with DevOps for CI/CD |
| Sprint length | 2 sprints | Large content volume (~30-36 pages from ~28,000 lines of source) |
| Velocity baseline | 8 SP/sprint = 16 SP total | Established from prior sprints |
| Utilization ceiling | 80% = 12.8 SP | Reserve 20% for interrupts and context switching |
| Story committed | US-01 (13 SP) | Only story in scope |
| Utilization | 81% (13 / 16) | At ceiling — no additional work should be added |

**Estimation tier**: DOCS_ONLY — pure markdown content extraction/writing plus YAML config and GitHub Actions workflow. No code, no tests, no API changes. The 13 SP reflects the sheer volume of pages to produce, each requiring reading and distilling source material.

**Sprint 1** (8 SP): Infrastructure + Getting Started + User Guide + Skills Reference
**Sprint 2** (5 SP): Config Reference + Hooks + Themes + Architecture + Contributing + Polish

---

## 3. Recommended Site Structure

```
docs/
├── index.md                          # Home / Overview
├── getting-started/
│   ├── installation.md               # Install the plugin
│   ├── setup-wizard.md               # Config wizard walkthrough
│   └── first-pipeline-run.md         # End-to-end first run guide
├── user-guide/
│   ├── pipeline-stages.md            # 7 stages with inputs/outputs/checkpoints
│   ├── project-types.md              # 6 project types with routing rules
│   ├── collaboration-patterns.md     # 6 collaboration patterns
│   ├── quality-gates.md              # Team DoD and quality gate criteria
│   └── git-integration.md            # Git/GitHub branching, commits, PRs
├── skills/
│   ├── index.md                      # Skills overview / catalog
│   ├── delivery-flow.md              # Pipeline orchestrator
│   ├── product-delivery.md           # PO, Scrum Master, Data Analyst
│   ├── developer.md                  # 14 languages, paradigms, clean code
│   ├── godot.md                      # Godot 4.x game dev
│   ├── architect.md                  # 11 roles, 4 decomposition strategies
│   ├── quality.md                    # QA engineering
│   ├── operations.md                 # DevOps, Release Manager, Tech Writer
│   ├── ui.md                         # UX/UI/Game UI
│   ├── user-feedback.md              # Persona-based testing
│   ├── alias-creator.md              # Theme creation and management
│   └── presentation.md               # Presentation composer
├── reference/
│   ├── configuration.md              # Full config.yml reference (70+ keys)
│   ├── hooks.md                      # 7 hooks with event types, behavior
│   └── alias-themes.md              # 13 built-in themes, custom theme guide
├── architecture/
│   ├── overview.md                   # Pipeline architecture, artifact flow
│   ├── memory-system.md             # Self-learning memory, tiered retrieval
│   ├── feature-knowledge.md          # FKCs, Impact Analysis Gate
│   └── artifact-contracts.md         # Artifact format contracts
└── contributing/
    ├── index.md                      # Getting started as a contributor
    └── plugin-structure.md           # Skill/hook/theme creation guide
```

**Total**: ~32 pages across 6 sections + home page.

**Navigation depth**: Home > Section > Page = 2 clicks maximum (meets AC-20's 3-click requirement).

---

## 4. Task Breakdown and Sequencing

### Phase 1: Infrastructure (1.5 SP) — Sprint 1

> *"Before the words, the walls. Before the tome, the table."*

| Task | Description | Est | Depends On | AC |
|------|-------------|-----|------------|-----|
| T-01 | Create `mkdocs.yml` with Material theme config: site name, theme (palette, dark mode, search, navigation tabs, TOC), plugins (search, minify), full `nav` tree matching site structure above | 0.75 SP | — | AC-01, AC-03 |
| T-02 | Create `.github/workflows/docs.yml` GitHub Actions workflow: trigger on push to `main` (paths: `docs/**`, `mkdocs.yml`), build with `mkdocs build`, deploy to GitHub Pages using `mkdocs gh-deploy` or `peaceiris/actions-gh-pages` | 0.5 SP | T-01 | AC-02 |
| T-03 | Create `docs/index.md` home page: plugin overview, key stats (11 skills, 7 stages, 13 themes), quick links to Getting Started and Skills Reference | 0.25 SP | T-01 | AC-20 |

### Phase 2: Getting Started (1.5 SP) — Sprint 1

> *"The first step is always the hardest. We must make it easy."*

| Task | Description | Est | Source Files | AC |
|------|-------------|-----|-------------|-----|
| T-04 | Write `docs/getting-started/installation.md`: plugin install command, prerequisites, verification | 0.25 SP | README.md | AC-04 |
| T-05 | Write `docs/getting-started/setup-wizard.md`: wizard walkthrough, 10 questions explained, quick-start (3 questions), config output | 0.5 SP | `setup-wizard.md` | AC-04, AC-05 |
| T-06 | Write `docs/getting-started/first-pipeline-run.md`: end-to-end walkthrough from config to completed pipeline run, what to expect at each stage, how to respond at checkpoints | 0.75 SP | `getting-started.md`, `pipeline-stages.md` | AC-04, AC-05 |

### Phase 3: User Guide (2.5 SP) — Sprint 1

> *"The guide through the mines — each passage marked, each danger noted."*

| Task | Description | Est | Source Files | AC |
|------|-------------|-----|-------------|-----|
| T-07 | Write `docs/user-guide/pipeline-stages.md`: all 7 stages with purpose, inputs, outputs, human checkpoints, stage-specific behavior | 1.0 SP | `pipeline-stages.md`, `quality-gates.md` | AC-06, AC-09 |
| T-08 | Write `docs/user-guide/project-types.md`: all 6 project types with stage routing rules, auto-detection logic | 0.5 SP | `project-types.md` | AC-07 |
| T-09 | Write `docs/user-guide/collaboration-patterns.md`: all 6 patterns with description, when to use, how they work | 0.5 SP | `team-patterns.md` | AC-08 |
| T-10 | Write `docs/user-guide/git-integration.md`: branching strategies, conventional commits, issue/PR automation | 0.5 SP | `git-integration.md`, `github-integration.md` | — |

### Phase 4: Skills Reference (2.5 SP) — Sprint 1

> *"Eleven skills. Eleven pages. Each one a window into a different craft."*

| Task | Description | Est | Source Files | AC |
|------|-------------|-----|-------------|-----|
| T-11 | Write `docs/skills/index.md`: skills catalog with summary table, invocation syntax overview | 0.25 SP | README.md | AC-10 |
| T-12 | Write `docs/skills/delivery-flow.md`: pipeline orchestrator page — stages, setup wizard, collaboration patterns, state management | 0.5 SP | `delivery-flow/SKILL.md` (1,232 lines) | AC-10, AC-11, AC-12 |
| T-13 | Write `docs/skills/product-delivery.md`: PO, Scrum Master, Data Analyst roles — task types, examples | 0.25 SP | `product-delivery/SKILL.md` (685 lines) | AC-10, AC-11, AC-12 |
| T-14 | Write `docs/skills/developer.md`: 14 languages, OOP/FP paradigms, clean code, Nx monorepo | 0.25 SP | `developer/SKILL.md` (490 lines) | AC-10, AC-11, AC-12 |
| T-15 | Write `docs/skills/architect.md`: 11 roles, 4 decomposition strategies, ADR lifecycle | 0.25 SP | `architect/SKILL.md` (612 lines) | AC-10, AC-11, AC-12 |
| T-16 | Write `docs/skills/godot.md`, `quality.md`, `operations.md`, `ui.md`: 4 skill pages (mid-sized skills, similar structure) | 0.5 SP | Respective SKILL.md files | AC-10, AC-11, AC-12 |
| T-17 | Write `docs/skills/user-feedback.md`, `alias-creator.md`, `presentation.md`: 3 skill pages (specialized skills) | 0.5 SP | Respective SKILL.md files | AC-10, AC-11, AC-12 |

### Phase 5: Reference Section (2.5 SP) — Sprint 2

> *"The index at the back of the book — where the scholar goes when they know what they seek."*

| Task | Description | Est | Source Files | AC |
|------|-------------|-----|-------------|-----|
| T-18 | Write `docs/reference/configuration.md`: all 70+ config keys organized by section, with type, default, valid values, description. Include full annotated example config. | 1.5 SP | `config-schema.md` (312 lines), `config-schema.json` | AC-13, AC-14 |
| T-19 | Write `docs/reference/hooks.md`: all 7 hooks with event type, purpose, behavior, implementation details | 0.5 SP | `hooks.json`, hook scripts, README hook table | AC-15 |
| T-20 | Write `docs/reference/alias-themes.md`: 13 built-in themes with role mappings, custom theme creation guide | 0.5 SP | 13 `.yml` files, `theme-format.md`, `alias-creator/SKILL.md` | AC-16, AC-17 |

### Phase 6: Architecture & Contributing (1.5 SP) — Sprint 2

> *"For those who would extend the realm, they must first understand its foundations."*

| Task | Description | Est | Source Files | AC |
|------|-------------|-----|-------------|-----|
| T-21 | Write `docs/architecture/overview.md`: pipeline architecture, artifact flow, two-channel communication | 0.5 SP | `SKILL.md` (delivery-flow), `artifact-contracts.md` | AC-18 |
| T-22 | Write `docs/architecture/memory-system.md` and `feature-knowledge.md`: memory protocol, FKCs, Impact Analysis Gate | 0.5 SP | `memory-protocol.md`, `feature-knowledge.md` | AC-18 |
| T-23 | Write `docs/architecture/artifact-contracts.md`: artifact format contracts per stage | 0.25 SP | `artifact-contracts.md` | AC-18 |
| T-24 | Write `docs/contributing/index.md` and `plugin-structure.md`: contributor guide, plugin structure, skill/hook creation, PR process, plugin-dev skills requirement | 0.25 SP | CLAUDE.md conventions, plugin-dev skill descriptions | AC-19 |

### Phase 7: Polish & Deploy (1.0 SP) — Sprint 2

> *"The final mile. Review, refine, release."*

| Task | Description | Est | Depends On | AC |
|------|-------------|-----|------------|-----|
| T-25 | Review all pages for consistency: heading hierarchy, link integrity, search indexing, navigation flow | 0.5 SP | T-01 through T-24 | AC-20, AC-21 |
| T-26 | Test deployment: push to main, verify GitHub Actions triggers, verify site renders on GitHub Pages, verify search works | 0.25 SP | T-25 | AC-02, AC-03 |
| T-27 | 3-click audit: verify every page is reachable within 3 clicks from home. Fix any navigation gaps. | 0.25 SP | T-26 | AC-20 |

---

## 5. Dependency Graph

```
T-01 (mkdocs.yml)
├── T-02 (GH Actions workflow)
├── T-03 (Home page)
├── T-04..T-06 (Getting Started — 3 pages)
├── T-07..T-10 (User Guide — 4 pages)
├── T-11..T-17 (Skills Reference — 12 pages)
├── T-18..T-20 (Reference — 3 pages)
├── T-21..T-24 (Architecture + Contributing — 5 pages)
└── T-25 (Review) ──> T-26 (Test deploy) ──> T-27 (3-click audit)
```

**Critical path**: T-01 > T-07 (largest User Guide page) > T-18 (largest Reference page) > T-25 > T-26 > T-27

Content pages (T-03 through T-24) are independent of each other — only T-01 is a prerequisite. This allows parallel work if capacity is available.

---

## 6. Sprint Allocation

### Sprint 1 (8 SP): Infrastructure + Content Core

| Phase | Tasks | SP |
|-------|-------|----|
| Infrastructure | T-01, T-02, T-03 | 1.5 |
| Getting Started | T-04, T-05, T-06 | 1.5 |
| User Guide | T-07, T-08, T-09, T-10 | 2.5 |
| Skills Reference | T-11 through T-17 | 2.5 |
| **Sprint 1 Total** | | **8.0** |

### Sprint 2 (5 SP): Reference + Architecture + Polish

| Phase | Tasks | SP |
|-------|-------|----|
| Reference | T-18, T-19, T-20 | 2.5 |
| Architecture + Contributing | T-21, T-22, T-23, T-24 | 1.5 |
| Polish & Deploy | T-25, T-26, T-27 | 1.0 |
| **Sprint 2 Total** | | **5.0** |

---

## 7. Sprint Summary

| Sprint | Stories | SP Committed | Ceiling | Utilization | Buffer |
|--------|---------|-------------|---------|-------------|--------|
| Sprint 1 | US-01 (partial) | 8 | 6.4 | 100% | 0 SP |
| Sprint 2 | US-01 (completion) | 5 | 6.4 | 63% | 1.4 SP |
| **Total** | US-01 | **13** | **12.8** | **81%** | — |

> **Note**: Sprint 1 is at ceiling. If blockers arise, T-16 or T-17 (skill pages) can slide to Sprint 2 — Sprint 2 has 1.4 SP buffer to absorb.

---

## 8. File Impact Summary

| File/Directory | Change Type | Tasks |
|----------------|------------|-------|
| `mkdocs.yml` (new) | Create | T-01 |
| `.github/workflows/docs.yml` (new) | Create | T-02 |
| `docs/` directory (new, ~32 files) | Create | T-03 through T-24 |

No existing files are modified. All new files. No config schema changes. No SKILL.md changes.

---

## 9. Definition of Done

A story is DONE when ALL of the following are true:

| # | Criterion |
|---|-----------|
| DoD-1 | All 27 tasks are complete |
| DoD-2 | All 21 acceptance criteria from stories.md are met |
| DoD-3 | `mkdocs build` succeeds with zero errors |
| DoD-4 | Site is live on GitHub Pages and accessible |
| DoD-5 | All 11 skills have dedicated pages with roles, task types, invocation, and examples |
| DoD-6 | Configuration reference covers all keys from `config-schema.md` |
| DoD-7 | Search returns relevant results for test queries |
| DoD-8 | Every page is reachable within 3 clicks from home |
| DoD-9 | Content is derived from existing source files, not invented |

---

## 10. Risk Assessment

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|-----------|------------|
| R1 | Sprint 1 overcommitted (at ceiling) | Medium | Medium | Skill pages T-16/T-17 can slide to Sprint 2 (1.4 SP buffer) |
| R2 | Config reference is larger than estimated (70+ keys) | Low | Medium | T-18 has 1.5 SP allocation — generous for a single reference page |
| R3 | GitHub Pages setup requires repo settings change | Low | Low | Standard process, well-documented by GitHub |
| R4 | Content quality varies across 32 pages | Medium | Medium | T-25 (review pass) catches inconsistencies before deploy |

---

> *"Twenty-seven tasks. Thirty-two pages. Two sprints. The road is mapped. The burden is clear. And when the last page is written and the site stands lit upon GitHub Pages, every traveler who seeks our knowledge shall find it — not scattered in the wind, but gathered in a single place, searchable, navigable, and true."*

---

*Planned by Scrum Master (Aragorn) — delivery-team:product-delivery*
