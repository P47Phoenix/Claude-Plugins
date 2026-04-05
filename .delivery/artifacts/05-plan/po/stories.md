# User Stories: Comprehensive Documentation Site

**Version**: 1.0
**Date**: 2026-04-04
**Author**: Product Owner (Gandalf)
**Idea Brief**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Source Issue**: #48
**Pipeline Type**: DOCS_ONLY

---

> *"I will not say: do not weep; for not all docs are an evil. But this one shall be a beacon — a single flame of knowledge where before there were only scattered embers."*

---

## US-01: Comprehensive Documentation Site for delivery-team Plugin

**As a** delivery-team plugin user (new user, power user, or contributor),
**I want** a comprehensive, searchable documentation site hosted on GitHub Pages using MkDocs Material that covers all 11 skills, the 7-stage pipeline, configuration reference, hooks, alias themes, and contributor guide,
**So that** I can discover, learn, and use the full capability of the delivery-team plugin without reading AI-facing SKILL.md files or navigating scattered reference directories.

**Issue**: #48
**Tier**: DOCS_ONLY (markdown + YAML config)
**Story Points**: 13

---

### Acceptance Criteria

#### Group A: MkDocs Setup & Deployment

| AC | Criterion |
|----|-----------|
| AC-01 | **Given** the repo root, **When** `mkdocs build` is run, **Then** the site builds without errors from a valid `mkdocs.yml` using the Material theme. |
| AC-02 | **Given** a push to the `main` branch that modifies files under `docs/` or `mkdocs.yml`, **Then** a GitHub Actions workflow automatically builds and deploys the site to GitHub Pages. |
| AC-03 | **Given** the deployed site, **When** a user visits the GitHub Pages URL, **Then** the site loads with Material theme, dark mode toggle, full-text search, and responsive navigation. |

#### Group B: Getting Started

| AC | Criterion |
|----|-----------|
| AC-04 | **Given** a new user on the docs home page, **When** they navigate to Getting Started, **Then** they find: installation instructions, quick-start wizard walkthrough, and a step-by-step first pipeline run guide. |
| AC-05 | **Given** the Getting Started content, **When** compared to `getting-started.md` and `setup-wizard.md` source files, **Then** the content is derived from those sources — restructured for user-facing clarity, not invented. |

#### Group C: User Guide (Pipeline)

| AC | Criterion |
|----|-----------|
| AC-06 | **Given** the User Guide section, **When** a user navigates to Pipeline Stages, **Then** they find documentation for all 7 stages (Idea, Refine, Design, Architect, Plan, Development, UAT) with purpose, inputs, outputs, and human checkpoints for each. |
| AC-07 | **Given** the User Guide section, **When** a user navigates to Project Types, **Then** they find documentation for all 6 project types (GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY) with stage routing rules. |
| AC-08 | **Given** the User Guide section, **When** a user navigates to Collaboration Patterns, **Then** they find documentation for all 6 patterns (evaluator-optimizer, adversarial review, review board, decision ownership, debate, consensus). |
| AC-09 | **Given** the User Guide section, **When** a user navigates to Quality Gates, **Then** they find documentation for the Team DoD validation process and quality gate criteria. |

#### Group D: Skills Reference

| AC | Criterion |
|----|-----------|
| AC-10 | **Given** the Skills Reference section, **When** a user browses it, **Then** they find a dedicated page for each of the 11 skills: delivery-flow, product-delivery, developer, godot, architect, quality, operations, ui, user-feedback, alias-creator, presentation. |
| AC-11 | **Given** any skill reference page, **When** a user reads it, **Then** it includes: skill name, roles/capabilities, supported task types, invocation syntax, and at least one usage example. |
| AC-12 | **Given** skill content, **When** compared to the corresponding SKILL.md, **Then** the content is derived from the source — distilled for user-facing clarity, not copy-pasted verbatim or invented. |

#### Group E: Configuration Reference

| AC | Criterion |
|----|-----------|
| AC-13 | **Given** the Configuration Reference page, **When** a user searches for a config key, **Then** all 70+ keys from `config-schema.md` are documented with: key name, type, default value, valid values, and description. |
| AC-14 | **Given** the Configuration Reference, **When** a user wants to see a complete example, **Then** a full annotated `config.yml` example is provided. |

#### Group F: Hooks Reference

| AC | Criterion |
|----|-----------|
| AC-15 | **Given** the Hooks Reference page, **When** a user reads it, **Then** all 7 hooks are documented with: hook name, event type (SessionStart, Stop, PreToolUse, PostToolUse, SubagentStop), purpose, behavior, and any customization options. |

#### Group G: Alias Themes

| AC | Criterion |
|----|-----------|
| AC-16 | **Given** the Alias Themes page, **When** a user browses it, **Then** all 13 built-in themes are listed with: theme name, character-to-role mappings, and personality description. |
| AC-17 | **Given** the Alias Themes page, **When** a user wants to create a custom theme, **Then** instructions for custom theme creation are provided (derived from `alias-creator/SKILL.md` and `theme-format.md`). |

#### Group H: Architecture & Contributing

| AC | Criterion |
|----|-----------|
| AC-18 | **Given** the Architecture section, **When** a user reads it, **Then** they find: pipeline architecture overview, memory system, artifact contracts, defect tracking, and Feature Knowledge System documentation. |
| AC-19 | **Given** the Contributing section, **When** a contributor reads it, **Then** they find: plugin structure conventions, skill/hook creation guidance, PR process, and the requirement to use plugin-dev skills. |

#### Group I: Navigation & Discoverability

| AC | Criterion |
|----|-----------|
| AC-20 | **Given** the site navigation, **When** a user starts from the home page, **Then** any feature/page is reachable within 3 clicks. |
| AC-21 | **Given** the site, **When** a user types a search query (e.g., "config key", "architect skill", "lotr theme"), **Then** MkDocs Material search returns relevant results. |

---

### Test Cases

| TC | Covers AC | Test | Expected Result |
|----|-----------|------|-----------------|
| TC-01 | AC-01 | Run `mkdocs build` from repo root | Build succeeds with zero errors, site output in `site/` directory |
| TC-02 | AC-02 | Push a change to `docs/index.md` on `main` | GitHub Actions workflow triggers, site deploys to GitHub Pages |
| TC-03 | AC-03 | Visit deployed site URL | Material theme renders, dark mode toggle visible, search bar functional, navigation tabs present |
| TC-04 | AC-04, AC-05 | Navigate to Getting Started > First Pipeline Run | Step-by-step guide present, content traceable to `getting-started.md` and `setup-wizard.md` |
| TC-05 | AC-06 | Navigate to User Guide > Pipeline Stages | All 7 stages documented with purpose, inputs, outputs, checkpoints |
| TC-06 | AC-07 | Navigate to User Guide > Project Types | All 6 project types documented with stage routing |
| TC-07 | AC-08 | Navigate to User Guide > Collaboration Patterns | All 6 patterns documented with description and when to use |
| TC-08 | AC-10, AC-11 | Navigate to Skills Reference, click each of the 11 skills | Each skill page has: name, roles, task types, invocation syntax, usage example |
| TC-09 | AC-13, AC-14 | Navigate to Configuration Reference, search for `aliases.theme` | Key found with type, default, valid values, description. Full example config present. |
| TC-10 | AC-15 | Navigate to Hooks Reference | All 7 hooks documented with event type, purpose, behavior |
| TC-11 | AC-16, AC-17 | Navigate to Alias Themes | 13 themes listed with role mappings. Custom theme creation instructions present. |
| TC-12 | AC-18 | Navigate to Architecture | Pipeline architecture, memory system, artifact contracts documented |
| TC-13 | AC-19 | Navigate to Contributing | Plugin structure, skill/hook guidance, PR process documented |
| TC-14 | AC-20 | From home page, attempt to reach the `godot` skill page | Reachable in <=3 clicks (Home > Skills > Godot) |
| TC-15 | AC-21 | Use search bar to search "retrospective" | Search returns relevant results from appropriate pages |

---

### Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| MkDocs + Material theme | External (pip install) | Available, well-maintained |
| GitHub Pages | External (GitHub) | Available, repo-level setting |
| GitHub Actions | External (GitHub) | Available, workflow to be created |
| Existing SKILL.md files (x11) | Internal | Complete, content source |
| Existing reference files (80+) | Internal | Complete, content source |
| Alias theme YAMLs (x13) | Internal | Complete, content source |

---

### Estimation Rationale

**13 story points** — This is a significant content project:
- ~30-36 documentation pages to write
- Each page requires reading the source SKILL.md/reference files and distilling user-facing content
- MkDocs configuration (mkdocs.yml with full nav tree, theme settings, plugins)
- GitHub Actions workflow for deployment
- All content must be derived from source, not invented — requires careful reading of ~28,000 lines

This is not a code project. No tests to write, no APIs to implement. But the volume of content extraction and restructuring is substantial.

---

> *"Thirteen points for a project that gathers scattered wisdom into a single tome. Not a small task — but a necessary one. And when it is done, no traveler shall wander our lands without a map."*

---

*Written by Product Owner (Gandalf) — delivery-team:product-delivery*
