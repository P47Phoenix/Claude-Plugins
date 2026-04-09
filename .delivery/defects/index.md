# Defect Index

**Last updated**: 2026-04-08
**Total defects**: 3
**Defects/story rate**: 0.25 (2 defects / 8 stories, run-2026-04-02-k3r9)

## Defects by Run

| Run | Type | Defects | Rate | Categories |
|-----|------|:-------:|:----:|------------|
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

## Trend
- First run with defects (all prior runs: 0 defects)
- Both run-2026-04-02-k3r9 defects found and fixed in-pipeline during UAT dogfooding
- **DEFECT-003 is the first systemic plugin defect** — warrants a delivery-flow self-improvement PR
- DEFECT-001, DEFECT-002 already addressed (validate-deck command, CK pricing via Archidekt)

## Active Defects
- **DEFECT-003** (open, Major) — Setup wizard quick-start still asks removed `project_type` question; v2.6 configs not migrated to v2.7. Systemic plugin defect; plugin self-improvement PR required.
