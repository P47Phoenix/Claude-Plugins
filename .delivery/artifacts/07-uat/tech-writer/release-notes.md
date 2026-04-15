# Release Notes — Documentation Harmonization

**Tech Writer**: Bilbo | **Stage**: 7 UAT | **Date**: 2026-04-14 | **Run**: run-2026-04-11-f7g4

## What Changed

A focused docs-only release that harmonizes discoverability and usability across the Claude-Plugins marketplace. No code, no behavior changes — only clearer paths for users to find and configure what's already shipped.

## New

- **`mtg-commander/README.md`** — plugin landing page: feature summary, Challenger agent mechanics, config surface (`.mtg-commander.yml`), and closure notes for DEFECT-001 (deterministic validation) and DEFECT-002 (price divergence).
- **`mtg-commander/.mtg-commander.yml.example`** — fully-commented example config covering `loops:`, `price_rules:`, and `escalation:` sections.
- **`mtg-commander/references/config-walkthrough.md`** — step-by-step walkthrough of the example config with rationale for each knob.
- **`delivery-team/skills/delivery-flow/references/constraints-quickstart.md`** — user-facing quickstart for constraint authoring, linking `constraints-model-guide.md` and `validate_constraints.py`.
- **`delivery-team/skills/delivery-flow/references/troubleshooting.md`** — SYMPTOM/DIAGNOSIS/FIX triage reference covering common pipeline failure modes.

## Updated

- **`CLAUDE.md`** — surfaces mtg-commander, paradigms/ structure, transformation-planning sub-workflow, constraints.yml.
- **`README.md` (root)** — What's new section + mtg-commander inclusion.
- **`.claude-plugin/marketplace.json`** — 6 plugins registered (verified).
- **Architect redirect stubs** — `volatility-decomposition.md` and `strategic-ddd.md` repaired to `../paradigms/` (caught in US-7 cross-link audit).

## Credits

- **Galadriel + Bilbo** — parallel Stage 1 discovery produced convergent priorities.
- **Gandalf (PO)** — overrode default routing to include UX + Tech Writer in Plan.
- **Aragorn** — Stage 6 cross-link audit caught the redirect stub regression.
- **Legolas** — 30/30 TC UAT sweep.

## Compatibility

No breaking changes. All additions are additive; all edits preserve existing anchors and cross-links.
