# Defect Index

**Last updated**: 2026-05-13
**Total defects**: 7
**Defects/story rate**: 0.25 (2 defects / 8 stories, run-2026-04-02-k3r9)

## Defects by Run

| Run | Type | Defects | Rate | Categories |
|-----|------|:-------:|:----:|------------|
| cross-run (5 waves, surfaced 2026-05-13) | INITIATIVE (skill-token-economy) | 1 | n/a | Documentation-process / Release-management (1, systemic) |
| run-2026-05-05-tk3 | FEATURE (caveman-lite) | 1 | 1.0 (1/1; P1 non-blocking) | Run-record hygiene / stale artifacts (1) |
| run-2026-04-15-j1k8 | DOCS | 1 | n/a | Documentation / diagram syntax (1) |
| ci-2026-04-08 | CI (version workflow) | 1 | n/a | CI workflow / security (1, systemic) |
| setup-2026-04-08 | SETUP (quick-start) | 1 | n/a | Wizard/schema drift (1, systemic) |
| run-2026-04-02-k3r9 | GREENFIELD | 2 | 0.25 | Agent validation gap (1), Incomplete pricing (1) |
| run-2026-04-01-m7v3 | BUG_FIX | 0 | 0.00 | — |
| run-2026-04-01-p8n5 | FEATURE | 0 | 0.00 | — |
| run-2026-03-30-r4x2 | FEATURE | 0 | 0.00 | — |
| run-2026-03-29-h3k7 | BUG_FIX | 0 | 0.00 | — |

## Category Breakdown

| Category | Count | Runs | Systemic? |
|----------|:-----:|------|:---------:|
| Agent validation gap | 1 | k3r9 | No (single occurrence) |
| Incomplete pricing | 1 | k3r9 | No (single occurrence) |
| Wizard/schema drift | 1 | setup-2026-04-08 | **Yes — systemic plugin defect** (wizard out of sync with v2.7 schema + missing migration) |
| CI workflow / security | 1 | ci-2026-04-08 | **Yes — systemic repo defect** (GitHub Actions command-injection sink in `version.yml`; regression guard warranted) |
| Documentation / diagram syntax | 1 | run-2026-04-15-j1k8 | No (single occurrence; same-pipeline fix) — authoring-pattern misuse of `\n` escapes in Mermaid labels |
| Run-record hygiene / stale artifacts | 1 | run-2026-05-05-tk3 | Borderline-systemic — second occurrence of `07-uat/dod/` directory drift would warrant SKILL.md Stage 7 entry-step; first occurrence handled in-PR with Option A banner-prepend |
| Documentation-process / Release-management | 1 | cross-run (5 waves) | **Yes — systemic process defect** (no CHANGELOG.md produced across 5 waves; Stage 7 UAT has no CHANGELOG promotion step; same-PR fix lands CHANGELOG.md, systemic fix carried to next initiative's backlog) |

## Trend
- First run with defects (all prior runs: 0 defects)
- Both run-2026-04-02-k3r9 defects found and fixed in-pipeline during UAT dogfooding
- **DEFECT-003 is the first systemic plugin defect** — warrants a delivery-flow self-improvement PR
- DEFECT-001, DEFECT-002 already addressed (validate-deck command, CK pricing via Archidekt)

## Active Defects
- **DEFECT-007** (open, P2 non-blocking) — No published CHANGELOG.md across 5 waves (Wave 0, 1, 2, caveman, Wave 3) of skill-token-economy initiative. Tech-Writer `release-notes.md` is run-scoped scratch at `.delivery/artifacts/07-uat/tech-writer/` and never promoted to repo-root `CHANGELOG.md`. No Stage 7 step exists to produce a published changelog; cross-doc-consistency UAT gate cannot catch the gap because CHANGELOG was never in scope. Fix: parallel Tech-Writer Bilbo dispatch authors `CHANGELOG.md` (Keep-a-Changelog format) same PR. Systemic fix carried forward to next initiative's backlog (BACKLOG-105 WI or BACKLOG-106 standalone) — add CHANGELOG promotion step to delivery-flow Stage 7 UAT.
- **DEFECT-006** (open, P1 non-blocking) — Three stale Wave-2 DoD review files share `.delivery/artifacts/07-uat/dod/` with this run's tk3 reviews without archive demarcation. PO review (po-review.md) overwritten this run; qa-review.md, devops-review.md, techwriter-review.md residual. Recommended fix: Option A banner-prepend (zero-risk, this PR) OR Option B move-to-_archive-tk2 (follow-on). Systemic-fix candidate if pattern repeats next wave.
- **DEFECT-003** (open, Major) — Setup wizard quick-start still asks removed `project_type` question; v2.6 configs not migrated to v2.7. Systemic plugin defect; plugin self-improvement PR required.
- **DEFECT-004** (open, Major + Security, **P0**) — `.github/workflows/version.yml` line 25 interpolates `${{ github.event.head_commit.message }}` directly into a bash `run:` block. Broke version bump on commit dc34e9d via unescaped `()` in the message; also a classic GitHub Actions command-injection vector. Fix: pass via `env:` instead of `${{ }}`. Blocks all future version bumps.
- **DEFECT-005** (closed in run-2026-04-15-j1k8, Minor / High visibility) — Two Mermaid diagrams broken by `\n` escape-sequence misuse and Mermaid-invalid type syntax (`float?`, `enum`). Fixed same-pipeline in `mtg-commander/ARCHITECTURE.md` (classDiagram) and `delivery-team/architecture/empirical-lifecycle.md` (flowchart).
