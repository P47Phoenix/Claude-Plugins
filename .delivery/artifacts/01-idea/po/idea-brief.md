# Idea Brief: Comprehensive Documentation Site for delivery-team Plugin

**Issue**: #48
**Type**: DOCS_ONLY
**Date**: 2026-04-04
**Author**: Product Owner (Gandalf)

---

> *"All that is gold does not glitter — and all that is documented does not illuminate. Twenty-eight thousand lines of wisdom lie scattered across eighty files, yet the traveler who arrives at our gate finds only a README and a prayer."*

---

## Problem Statement

The delivery-team plugin has grown to 11 skills, 7 hooks, 18+ reference files, 13 alias themes, a 7-stage pipeline with 6 collaboration patterns, and 70+ config keys. The documentation for all of this exists but is fragmented across:

- **README.md** files (top-level and per-plugin) — installation and quick-start only
- **CLAUDE.md** — repo-level context written for the AI, not for human users
- **SKILL.md** files (11 total, ~5,700 lines) — AI-facing implementation instructions, not user-facing documentation
- **Reference files** (80+, ~23,000 lines) — deep technical content buried in skill subdirectories
- **Alias theme YAMLs** (13 files) — undiscoverable without browsing the filesystem

The consequence: new users have no onboarding path beyond "run the wizard." Power users cannot discover config keys, alias themes, or hook behavior without reading AI-facing internals. Contributors must reverse-engineer plugin structure from existing code.

As the team principle states: *"Stale docs are worse than no docs — they teach the wrong thing with authority."* But scattered docs are nearly as bad — they teach the right thing to no one.

## Target Users

| Persona | Pain Point | What They Need |
|---------|-----------|----------------|
| **New User** | Reads README, runs wizard, hits a wall. Doesn't know what 11 skills can do or how pipeline stages work. | Getting Started guide with install-to-first-pipeline-run walkthrough |
| **Power User** | Knows the plugin but can't find specific config keys, alias themes, hook behaviors, or collaboration patterns without reading SKILL.md internals. | Searchable config reference, hooks reference, skills catalog, alias theme gallery |
| **Contributor** | Wants to add a skill, hook, or theme but must reverse-engineer structure from existing files. No structured guide. | Plugin structure guide, dev workflow, PR process, testing conventions |

## Goals

| # | Goal | Measurable Target |
|---|------|-------------------|
| 1 | Single navigable home for all delivery-team documentation | Hosted on GitHub Pages at a predictable URL |
| 2 | Clear onboarding path | New user can go from install to first completed pipeline run following only the docs |
| 3 | Searchable reference | All 70+ config keys, 11 skills, 7 hooks, 13 alias themes findable via search |
| 4 | 3-click discovery | Any feature reachable within 3 navigation clicks from the home page |
| 5 | Zero-touch deployment | Auto-deployed from `main` via GitHub Actions — no manual publish step |
| 6 | Derived from source | All content distilled from existing SKILL.md and reference files — nothing invented |

## Scope

### In Scope

| Section | Content Source | Est. Pages |
|---------|--------------|------------|
| Home / Overview | README.md, CLAUDE.md overview | 1 |
| Getting Started (install, wizard, first run) | `getting-started.md`, `setup-wizard.md`, README | 3-4 |
| User Guide: Pipeline Stages | `pipeline-stages.md`, `project-types.md`, `quality-gates.md` | 4-5 |
| User Guide: Collaboration Patterns | `team-patterns.md` | 1-2 |
| User Guide: Memory & Learning | `memory-protocol.md`, `feature-knowledge.md` | 1-2 |
| Skills Reference (x11) | Each skill's `SKILL.md` + key references | 11 |
| Configuration Reference | `config-schema.md`, `config-schema.json` (70+ keys) | 2-3 |
| Hooks Reference | `hooks.json`, 6 hook scripts, hook table | 1-2 |
| Alias Themes | 13 `.yml` theme files, `alias-creator/SKILL.md`, `theme-format.md` | 1-2 |
| Architecture Overview | `team-patterns.md`, `artifact-contracts.md`, `defect-tracking.md`, `analytics.md` | 2-3 |
| Git & GitHub Integration | `git-integration.md`, `github-integration.md` | 1-2 |
| Contributing Guide | Plugin structure conventions from CLAUDE.md, PR process | 1-2 |
| **Total** | **~28,000 lines of source material** | **~30-36 pages** |

### Out of Scope

- API/SDK integration docs (no public API exists)
- Video tutorials or interactive walkthroughs
- Versioned documentation (single version for now)
- Documentation for other marketplace plugins (agentic-flow-builder, prompt-engineer, etc.)
- Staleness detection CI (future iteration — noted as a follow-up)

## Delivery Format

**MkDocs Material** — team's preferred choice per Issue #48:

- Markdown-based (matches existing content format exactly)
- GitHub Pages hosting (zero infrastructure cost)
- Built-in full-text search, dark mode, responsive navigation tabs
- `mkdocs.yml` configuration for site structure and theme
- GitHub Actions workflow for auto-deploy on push to `main`
- Admonitions, tabs, code highlighting, and table of contents out of the box

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Stale docs after initial publish | Medium | High | Content derived from source files; staleness CI is a documented follow-up |
| Scope creep — temptation to write tutorials for each skill | Medium | Medium | Stick to reference + getting started; tutorials are a future iteration |
| Content quality — AI-facing SKILL.md doesn't translate directly to user docs | Medium | Medium | Technical Writer role reviews all content for user-facing clarity |
| Large page count overwhelms single contributor | Low | Medium | Content is extraction and restructuring, not creation from scratch |

---

> *"A documentation site is not a luxury. It is the road between the knowledge we hold and the travelers who seek it. Without the road, the knowledge may as well not exist."*

---

*Written by Product Owner (Gandalf) — delivery-team:product-delivery*
