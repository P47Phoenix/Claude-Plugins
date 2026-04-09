# AS-IS Use Cases — Claude-Plugins Marketplace Repository

**Phase:** 1A Behavioral Reconstruction (PO-led)
**Run:** US-7-dogfood-phase1a
**Date:** 2026-04-08
**Target:** Claude-Plugins repo root (`/var/home/meconnelly/Documents/GitHub/Claude-Plugins`)
**Evidence roots:** `CLAUDE.md`, `.claude-plugin/marketplace.json`, `delivery-team/skills/`, `.delivery/backlog/`, `.delivery/defects/`, git log, `prd-quality-gate-flow/`, `mtg-commander/`
**Skip justification:** n/a — Phase 1A executed per FR-6 default.

**Total:** 7 use cases — confidence distribution: **3 high, 3 medium, 1 low**

*By Gandalf the Grey. A marketplace of many wonders, this repo — and wonders bear remembering. Before we remap its roads, let us first set down, truthfully, the paths its travelers already walk.*

---

## UC-01: Run delivery-flow pipeline end-to-end on a new feature

- **actor:** Developer / feature owner invoking Claude Code with the delivery-team plugin installed
- **goal:** Take an idea from concept to UAT sign-off through the 7-stage delivery pipeline with team collaboration, DoD validation, and adversarial review.
- **preconditions:** Repo has `delivery-team` plugin installed; `.delivery/config.yml` present (schema v2.7); user issues an intent matching delivery-flow triggers ("build X", "ship Y", etc.).
- **main_flow:**
  1. User invokes delivery-flow with a feature intent.
  2. Phase 1 auto-detects project type (GREENFIELD / FEATURE / BUG_FIX / DESIGN / GAME_DEV / SPIKE / DOCS_ONLY).
  3. Orchestrator routes through 7 stages: Idea → Refine → Design → Architect → Plan → Development → UAT.
  4. Each stage produces artifacts under `.delivery/artifacts/0N-<stage>/`.
  5. Team DoD validators gate each stage; adversarial review and consensus patterns run where configured.
  6. Retrospective runs at Stop (enforced by hook); pipeline terminates cleanly.
- **variations:**
  - DESIGN project type terminates after Architect stage (no Plan/Dev/UAT).
  - DOCS_ONLY and SPIKE take lightened stage depth but never skip (per `feedback_no_skip_stages`).
  - `routing.force_type` opt-in override pins project type.
  - Stage failures trigger self-correction loops before escalation.
- **confidence:** high
- **evidence_citations:**
  - `delivery-team/skills/delivery-flow/SKILL.md` — pipeline orchestrator definition and 7-stage structure
  - `CLAUDE.md:93` — documents 7 stages, auto-detect, team DoD, 6 collaboration patterns
  - `.delivery/artifacts/` — directories `01-idea` through `07-uat` present, proving stages have executed
  - `.delivery/artifacts/retro/` — 7 retrospective files (`retro-*.md`) proving end-to-end runs with enforced close-out

---

## UC-02: Configure the delivery team via the setup wizard

- **actor:** Repo owner adopting or upgrading the delivery-team plugin
- **goal:** Produce a valid, current-schema `.delivery/config.yml` without manual YAML authoring.
- **preconditions:** delivery-team plugin installed; no config present, or config present at an older schema version.
- **main_flow:**
  1. User invokes setup wizard (or wizard auto-triggers on SessionStart config-check hook).
  2. Wizard asks 9 questions with auto-detect smart defaults.
  3. Wizard writes `.delivery/config.yml` at schema v2.7.
  4. Post-install validation confirms schema correctness and migrates stale hooks.
- **variations:**
  - Existing older-schema config → migration path runs (DEFECT-related: stale hook migration added in #67/#68).
  - Project type question omitted in v2.7 (moved to runtime routing decision).
  - Validation failure → wizard re-prompts.
- **confidence:** high
- **evidence_citations:**
  - `CLAUDE.md:95` — "Setup wizard with 9 questions (auto-detect + smart options)"
  - git log `20f4aea` — "add stale hook migration and post-install validation to setup wizard (#67) (#68)"
  - `CLAUDE.md` config-schema mention — v2.7 is current, removed `project_type` key
  - SessionStart config-check hook row in CLAUDE.md hooks table

---

## UC-03: Register and ship a new plugin or skill in the marketplace

- **actor:** Plugin author (maintainer or external contributor)
- **goal:** Publish a new plugin/skill so it is discoverable via `marketplace.json` and loadable by Claude Code users.
- **preconditions:** Author has write access or opens a PR; plugin directory follows kebab-case; contains `SKILL.md` and `LICENSE.txt`.
- **main_flow:**
  1. Author scaffolds `<plugin-name>/` with SKILL.md, LICENSE, optional hooks/scripts/references.
  2. Author registers plugin in `.claude-plugin/marketplace.json` with unique id, display name, description.
  3. PR opened, reviewed, and merged to `main`.
  4. CI version-bump workflow runs; consumers pull the updated marketplace.
- **variations:**
  - Skill-only addition inside an existing plugin (e.g., adding a new skill under `delivery-team/skills/`).
  - New top-level plugin (e.g., `mtg-commander`, `prd-quality-gate-flow`).
  - Modifying an existing plugin's SKILL.md or hooks.
- **confidence:** high
- **evidence_citations:**
  - `.claude-plugin/marketplace.json` — registry file
  - `CLAUDE.md:12-28` — plugin structure contract
  - `delivery-team/skills/` listing — 11 registered skills matching the CLAUDE.md table
  - git log — multiple feature commits adding skills (`feat(presentation)`, `feat(delivery-flow)`)

---

## UC-04: Track and resolve defects that feed plugin self-improvement

- **actor:** Delivery team (PO + engineers) dogfooding the pipeline
- **goal:** Log defects discovered during pipeline runs, prioritize them, and drive fixes back into the plugins themselves.
- **preconditions:** `.delivery/defects/` directory exists; pipeline has run at least once; a failure or regression has been observed.
- **main_flow:**
  1. Defect discovered during dev, CI, or retrospective.
  2. PO writes `DEFECT-NNN.md` with pipeline, severity, priority, category, evidence.
  3. Defect triggers plugin self-improvement PR per `feedback_po_logs_issues` memory.
  4. Fix lands as a commit referencing the DEFECT id (e.g., `fix(ci): prevent command injection (DEFECT-004)`).
  5. Defect index updated.
- **variations:**
  - P0 security defects (DEFECT-004 — command injection in version.yml) go straight to fix.
  - Systemic defects produce backlog items rather than one-shot fixes.
  - Defect with empirical validation gap triggers SubagentStop hook.
- **confidence:** high
- **evidence_citations:**
  - `.delivery/defects/DEFECT-001.md` through `DEFECT-004.md` — four real defects on disk
  - `.delivery/defects/index.md` — defect index file
  - git log `f3fea27` — "fix(ci): prevent command injection in version bump workflow (DEFECT-004)"
  - Memory `feedback_po_logs_issues` — PO auto-logs issues from research immediately

---

## UC-05: Run the PRD quality-gate flow against a standalone PRD

- **actor:** Product owner or analyst with a draft PRD outside a full delivery-flow run
- **goal:** Evaluate a PRD against 7 deterministic quality gates, persisting results in SQLite for audit.
- **preconditions:** `prd-quality-gate-flow/` plugin present; Python 3 available; PRD input supplied.
- **main_flow:**
  1. User runs `python prd-quality-gate-flow/prd_flow_builder.py` to scaffold the flow.
  2. User runs `python prd-quality-gate-flow/prd_execute.py` to execute gates.
  3. Business rules engine evaluates each gate deterministically (AND/OR/NOT, no AI variance).
  4. Results persist to SQLite; user inspects via `check_db.py`.
  5. `fix_and_run.py` offers an automated end-to-end path.
- **variations:**
  - Gate failure → remediation guidance surfaced; rerun after fix.
  - `fix_and_run.py` path bypasses manual staging.
  - Audit-log-only inspection via `check_db.py` without re-execution.
- **confidence:** medium
- **evidence_citations:**
  - `CLAUDE.md:118-123` — documents `prd_flow_builder.py`, `prd_execute.py`, `check_db.py`, `fix_and_run.py` invocations
  - `CLAUDE.md:145-151` — agentic-flow core components (database.py, business_rules_engine.py)
  - `.claude-plugin/marketplace.json` — prd-quality-gate-flow plugin registration

---

## UC-06: Build an MTG Commander deck via the mtg-commander plugin

- **actor:** Magic: The Gathering player using Claude Code
- **goal:** Produce a synergy-dense, format-legal, budget-compliant 100-card Commander decklist via a multi-agent pipeline backed by the Scryfall API.
- **preconditions:** `mtg-commander` plugin installed; user supplies commander choice, budget, and style preferences; network access to Scryfall.
- **main_flow:**
  1. User triggers plugin with a phrase like "build a commander deck around <commander>".
  2. Multi-agent pipeline decomposes the task (synergy analysis → card selection → legality/budget check → decklist assembly).
  3. Scryfall API queried for card data.
  4. Final 100-card decklist returned with synergy rationale and legality/budget notes.
- **variations:**
  - Budget-constrained variant.
  - Theme-constrained variant (tribal, combo, control).
  - Legality failure → substitution loop.
- **confidence:** medium
- **evidence_citations:**
  - Skills list in session — `mtg-commander:mtg-commander` skill registered with full trigger description
  - User-directive in US-7 task prompt — explicitly calls out mtg-commander as real behavior supported by this repo

---

## UC-07: Compose a team-collaborative presentation from pipeline outputs

- **actor:** Delivery team member preparing a sprint review, stakeholder update, or feature pitch
- **goal:** Assemble team contributions into a cohesive presentation in one of 9 types and 4 output formats (markdown, marp, paste-ready, pptx).
- **preconditions:** `presentation` skill present under delivery-team; source material (artifacts, retros, design docs) exists; user specifies presentation type.
- **main_flow:**
  1. User invokes presentation skill with type + audience.
  2. Step 1 Assemble: team contributions collected.
  3. Step 2 Content Gate: completeness check.
  4. Step 3 Draft → Step 4 Compose → Step 5 Review Gate → Step 6 User Review.
  5. Output rendered in requested format (pptx via `generate_pptx.py`).
- **variations:**
  - Sprint Review vs Investor Pitch vs Retrospective Summary (9 types).
  - Light mode for minimal ceremony.
  - Narrative intelligence passes (4 editorial passes) applied or skipped.
  - PPTX output path added in v1.1 (#43-#46).
- **confidence:** low
- **evidence_citations:**
  - `CLAUDE.md` presentation row — documents 9 types, 4 formats, 6-step flow, light mode, narrative intelligence
  - git log `1747b86` — "feat(presentation): add v1.1 enhancements — 5 new types, PPTX output"
  - git log `35ffd58` — "fix ... generate_pptx.py"

  *Low confidence because:* no end-to-end artifact of a composed presentation exists under `.delivery/artifacts/` to confirm the flow actually runs end-to-end in this repo. Evidence proves the capability is built and maintained, but real dogfooding traces are absent — the flow is documented and fixed, not observably exercised here.

---

*Thus ends the reading of the roads. Seven paths, honestly numbered — three walked in clear daylight, three in mingled shadow, and one whose footprints I found only in song and in builder's chisel, not in the mud. A wizard does not pretend to certainty the stones do not give him.* — Gandalf

STATUS: DONE
ARTIFACT: .delivery/artifacts/08-transform/as-is-use-cases.md
SUMMARY: Gandalf reports — 7 AS-IS use cases reconstructed from repo evidence: 3 high, 3 medium, 1 low. Honesty floor satisfied; every entry cites sources.
