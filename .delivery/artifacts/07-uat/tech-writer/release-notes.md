# Release Notes — Comprehensive Documentation Site

**Version**: 2.17.0 (Documentation Release)
**Date**: 2026-04-04
**Project Type**: DOCS_ONLY
**Source Issue**: [#48](https://github.com/P47Phoenix/Claude-Plugins/issues/48)
**Skill**: `delivery-team:operations` (Technical Writer)

---

*"There's a great deal of wisdom in this Fellowship -- scattered across eighty files, mind you, and none of it easy to find without a very long walk and a bit of luck. This release, if I may say so, builds the road."*

Twenty-eight thousand lines of knowledge lived in SKILL.md files, reference documents, and YAML configs -- all written for the AI, none of it navigable by a human traveler. New users hit a wall after the setup wizard. Power users hunted through internals for config keys. Contributors reverse-engineered plugin structure from existing code. This release gives them all a proper front door.

---

## What's New

### MkDocs Material Documentation Site (25 Pages)

A complete, searchable documentation site covering the full delivery-team plugin, built with MkDocs Material and deployed automatically to GitHub Pages at [p47phoenix.github.io/Claude-Plugins](https://p47phoenix.github.io/Claude-Plugins/).

Every page is distilled from existing source material -- SKILL.md files, reference documents, config schemas, and theme YAMLs. Nothing invented; everything restructured for human readers.

### Getting Started (3 pages)

- **Installation** -- From `claude plugin add` to first confirmed load
- **Quick Start** -- Install-to-first-completed-pipeline-run walkthrough, fulfilling Goal #2 from the idea brief
- **Commands** -- Slash commands reference for triggering skills and pipeline operations

### User Guide (4 pages)

- **Pipeline Stages** -- All 7 stages (Idea through UAT) with entry conditions, sub-flows, DoD validators, and output artifacts
- **Project Types** -- The 6 auto-detected types (GREENFIELD, FEATURE, BUG_FIX, GAME_DEV, SPIKE, DOCS_ONLY) with stage routing tables
- **Collaboration Patterns** -- All 6 patterns: evaluator-optimizer, adversarial review, review board, decision ownership, debate, and consensus
- **Configuration Reference** -- All 70+ config keys from config-schema v2.3, searchable and categorized

### Skills Reference (12 pages)

- **Skills Overview** -- Catalog of all 11 skills with role mappings and trigger phrases
- **Individual skill pages** (11) -- Each skill documented with roles, capabilities, trigger phrases, and key behaviors. Covers delivery-flow, product-delivery, developer, architect, quality, operations, UI/UX, user-feedback, godot, alias-creator, and presentation

### Reference (3 pages)

- **Hooks** -- All 7 hooks across 5 event types with trigger conditions and behavior
- **Alias Themes** -- Gallery of all 13 built-in themes with character-to-role mappings
- **Memory System** -- Tiered chunked retrieval, memory structure, and self-learning protocol

### Architecture (1 page)

- **Overview** -- Two-channel architecture, agent isolation model, orchestrator routing, and artifact flow

### Contributing (1 page)

- **Guide** -- Plugin structure conventions, skill/hook/theme creation process, PR workflow

### Zero-Touch Deployment

A GitHub Actions workflow (`.github/workflows/docs.yml`) auto-deploys the site on every push to `main` that touches `docs/**` or `mkdocs.yml`. No manual publish step. Fulfills Goal #5.

---

## Site Features

| Feature | Details |
|---------|---------|
| **Full-text search** | Built-in MkDocs search with suggestions and highlighting |
| **Dark mode** | Toggle between light (default) and slate dark scheme |
| **Navigation tabs** | Top-level sections accessible via tabs with expandable side nav |
| **Code highlighting** | Syntax highlighting with copy-to-clipboard on all code blocks |
| **Admonitions** | Info, warning, and tip callouts throughout |
| **Permalink anchors** | Every heading gets a permalink for direct linking |
| **3-click discovery** | Any feature reachable within 3 clicks from the home page (Goal #4) |
| **Responsive** | Full mobile and tablet support via Material theme |

---

## What Did Not Change

- **Plugin behavior**: Zero changes to any SKILL.md, hook, config schema, or pipeline logic. This is a purely additive documentation layer.
- **README.md**: The existing README remains as-is. The docs site supplements it; it does not replace it.
- **CLAUDE.md**: AI-facing repo context is unchanged. The docs site is for humans; CLAUDE.md is for Claude.
- **Config schema**: Remains at v2.3. No new keys.

---

## Breaking Changes

**None.** This release adds documentation files and a deployment workflow. No existing behavior is modified.

---

## Files Added

| Path | Purpose |
|------|---------|
| `mkdocs.yml` | Site configuration: theme, navigation, extensions, plugins |
| `docs/index.md` | Home page with at-a-glance summary and quick links |
| `docs/getting-started/*.md` (3 files) | Installation, quick start, commands |
| `docs/user-guide/*.md` (4 files) | Pipeline, project types, collaboration, config reference |
| `docs/skills/*.md` (12 files) | Skills overview + 11 individual skill pages |
| `docs/reference/*.md` (3 files) | Hooks, alias themes, memory system |
| `docs/architecture/overview.md` | Architecture overview |
| `docs/contributing/index.md` | Contributor guide |
| `.github/workflows/docs.yml` | GitHub Actions auto-deploy on push to main |

**Total**: 25 documentation pages + 1 config file + 1 workflow = 27 new files, ~2,261 lines of user-facing documentation.

---

## Goals Achieved

| # | Goal | Status |
|---|------|--------|
| 1 | Single navigable home for all delivery-team documentation | Achieved -- hosted on GitHub Pages |
| 2 | Clear onboarding path (install to first pipeline run) | Achieved -- 3-page Getting Started section |
| 3 | Searchable reference (70+ config keys, 11 skills, 7 hooks, 13 themes) | Achieved -- full-text search + dedicated reference pages |
| 4 | 3-click discovery | Achieved -- tab navigation + expandable sections |
| 5 | Zero-touch deployment | Achieved -- GitHub Actions on push to main |
| 6 | Derived from source | Achieved -- all content distilled from existing files |

---

## Known Limitations

- **Staleness detection**: No CI job yet to detect when source files drift from documentation. Noted as a follow-up in the idea brief.
- **Single version**: No versioned docs. The site reflects the current state of `main`.
- **Scope**: Covers delivery-team plugin only. Other marketplace plugins (agentic-flow-builder, prompt-engineer, prd-quality-gate-flow, research-agent) are not documented here.

---

## References

- **Issue #48**: [Comprehensive Documentation Site](https://github.com/P47Phoenix/Claude-Plugins/issues/48)
- **Idea Brief**: `.delivery/artifacts/01-idea/po/idea-brief.md`
- **Site URL**: [https://p47phoenix.github.io/Claude-Plugins/](https://p47phoenix.github.io/Claude-Plugins/)

---

*"Now, I won't pretend that writing twenty-five pages of documentation is quite as thrilling as burgling a dragon's hoard. But I will say this: a well-organized table of contents is its own kind of treasure map. And unlike Smaug's gold, this one is meant to be shared."*

---

*Generated by Technical Writer (Bilbo) -- delivery-team:operations*
