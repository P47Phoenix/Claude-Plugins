# Defect Index

**Last updated**: 2026-04-15
**Total defects**: 5
**Defects/story rate**: 0.25 (2 defects / 8 stories, run-2026-04-02-k3r9)

## Defects by Run

| Run | Type | Defects | Rate | Categories |
|-----|------|:-------:|:----:|------------|
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

## Trend
- First run with defects (all prior runs: 0 defects)
- Both run-2026-04-02-k3r9 defects found and fixed in-pipeline during UAT dogfooding
- **DEFECT-003 is the first systemic plugin defect** — warrants a delivery-flow self-improvement PR
- DEFECT-001, DEFECT-002 already addressed (validate-deck command, CK pricing via Archidekt)

## Active Defects
- **DEFECT-003** (open, Major) — Setup wizard quick-start still asks removed `project_type` question; v2.6 configs not migrated to v2.7. Systemic plugin defect; plugin self-improvement PR required.
- **DEFECT-004** (open, Major + Security, **P0**) — `.github/workflows/version.yml` line 25 interpolates `${{ github.event.head_commit.message }}` directly into a bash `run:` block. Broke version bump on commit dc34e9d via unescaped `()` in the message; also a classic GitHub Actions command-injection vector. Fix: pass via `env:` instead of `${{ }}`. Blocks all future version bumps.
- **DEFECT-005** (closed in run-2026-04-15-j1k8, Minor / High visibility) — Two Mermaid diagrams broken by `\n` escape-sequence misuse and Mermaid-invalid type syntax (`float?`, `enum`). Fixed same-pipeline in `mtg-commander/ARCHITECTURE.md` (classDiagram) and `delivery-team/architecture/empirical-lifecycle.md` (flowchart).
