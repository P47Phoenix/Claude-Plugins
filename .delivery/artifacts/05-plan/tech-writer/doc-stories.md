# Documentation Stories — DOCS_ONLY Cycle

**Author:** Bilbo Baggins, Storyteller (Tech Writer, `lotr-full` alias)
**Stage:** 05-Plan · Project type: DOCS_ONLY · Tier: markdown
**Sources:** Bilbo priorities `01-idea/tech-writer/documentation-inventory.md` · Galadriel IA `03-design/ux/target-documentation-ia.md` · Galadriel UX recs `01-idea/ux/documentation-ux-review.md`

> "Short cuts make long delays, but plans make short journeys." Here is the map.

---

## Capacity Declaration

- **Sprint ceiling:** 4 pts · **Hard cap:** 5 pts · **Tier:** markdown (small estimates)
- **Planned total:** 8 stories · **8 pts** across **2 sprints** (4 pts + 4 pts)
- **Out of scope:** SKILL.md rewrites, code changes, new features, ADR rewrites, internal `references/` rewrites
- **Forbidden-vocabulary watch:** no impl-detail leaks (e.g., paradigm restructure described as "how paradigms are selected," not "sub-skill router refactor")

## Open Questions Resolved (from Galadriel §8)

- **Q1 stage count (7 vs 8):** Transformation is an **optional Architect sub-flow**, not a pipeline stage. `.delivery/artifacts/08-transform/` is an artifact bucket, not a new stage. Pipeline remains **7 stages**. Documented this way in US-5 and `transformation-planning.md` guidance (deferred page — see note below).
- **Q2 docs/ rebrand:** **EXPAND** to all plugins (URL is `Claude-Plugins`). Deferred to a later cycle — too heavy for 4-pt ceiling; this cycle touches only `README.md`, `CLAUDE.md`, new `mtg-commander/README.md`, and marketplace.json verification. MkDocs rebrand + new `docs/user-guide/*` pages are **NOT** in this cycle.
- **Q3 mtg-commander README depth:** **Lightweight** pattern-mirror of `delivery-team/README.md`. Inline `.mtg-commander.yml` example. Full tutorial deferred.
- **Q4 marketplace.json:** **Verification + description touch-ups only.** No schema changes.

**Cycle narrowing:** Galadriel's IA is the north star, but this cycle delivers the **highest-leverage slice**: the root-level discoverability fixes + the mtg-commander README + the constraints user-guide entry + CLAUDE.md/README refresh. New `docs/user-guide/*` MkDocs expansion is a follow-on cycle. This keeps us inside 4-pt sprint ceilings and honors the DOCS_ONLY markdown tier.

---

## Stories

### US-1 — Create `mtg-commander/README.md` (2 pt)

**Traces:** Bilbo #1 · Galadriel #1 · Convergence #1
**Why:** Shipped plugin, registered in `marketplace.json`, zero user-facing presence. Largest first-contact gap.
**Deliverable:** `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/mtg-commander/README.md`
**Acceptance:**
- File exists at above path
- Mirrors `delivery-team/README.md` structure (What is this · Install · Quick start · Advanced)
- Includes inline `.mtg-commander.yml` example block with `max_card_price`, `escalation`, and comments
- Links to `mtg-commander/SKILL.md` for deep reference
- Has a "Troubleshooting pointers" bullet list (3–5 common failure modes, one-liner each)
- No impl-detail vocabulary (no "sub-agent dispatch guardrail" etc.)
**Dependencies:** none
**Sprint:** 1

### US-2 — Add `.mtg-commander.yml.example` + README walkthrough section (1 pt)

**Traces:** Bilbo #2 (priming discoverability) · Galadriel #5 · Feature map row "MTG Challengers"
**Why:** Config file is user-authored but only documented inside SKILL.md. Example file + walkthrough closes the authoring gap without a full `docs/user-guide/mtg-config.md` page (deferred).
**Deliverable:** `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/mtg-commander/.mtg-commander.yml.example` + "Configuration" section inside US-1 README
**Acceptance:**
- Example file exists with every documented key, sensible defaults, commented explanations
- README "Configuration" section explains: where to place the file, each key's purpose, when to tune, how to validate (pointer to SKILL.md schema)
- Real YAML that parses (`python3 -c "import yaml; yaml.safe_load(open('mtg-commander/.mtg-commander.yml.example'))"`)
**Dependencies:** US-1 (same file)
**Sprint:** 1

### US-3 — Update `CLAUDE.md` plugin inventory + delivery-flow primitives (1 pt)

**Traces:** Bilbo #3 · Galadriel #6 · Convergence #4
**Why:** Available Plugins table lists 5; repo has 6. Delivery-flow architecture bullets omit constraints, Architecture Board, Transformation Planning, paradigm sub-skills. Stale feature list.
**Deliverable:** Edits to `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/CLAUDE.md`
**Acceptance:**
- Available Plugins table (lines ~29–35) includes `mtg-commander/` row with accurate description
- Architect row under delivery-team skills references paradigm sub-skills + Transformation Planning (without impl-detail vocabulary — describe as "paradigm selection" and "AS-IS → TO-BE planning")
- Delivery-flow architecture section (lines ~90–106) gains bullets for: `constraints.yml` primitive, Architecture Board, Transformation Planning sub-flow
- Grep for stale tokens: `project_type` should appear only in the v2.7 removal note; no new occurrences implying it is active
- No content removed that is still accurate
**Dependencies:** none
**Sprint:** 1

### US-4 — Update root `README.md` plugin roster + recent additions (1 pt)

**Traces:** Bilbo #1, #4 · Galadriel #2, rec #6 · Convergence #1, #4
**Why:** README advertises 5 plugins, never names `mtg-commander`. Presentation row is a generation stale (says 4 types / 3 formats; actual is 9 types / 4 formats + narrative intelligence + light mode).
**Deliverable:** Edits to `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/README.md`
**Acceptance:**
- Plugin list/table includes `mtg-commander` row with one-sentence description + link to `mtg-commander/README.md` (created in US-1)
- Presentation row updated: `9 types · 4 formats (incl. pptx) · narrative intelligence · light mode`
- New "Recently shipped" or "Recent additions" short section (≤6 bullets) naming: constraints primitive, Architecture Board, Transformation Planning, paradigm selection, MTG Commander plugin
- Link from Recently-shipped bullets to the relevant plugin README or (for delivery-flow features) to `delivery-team/README.md`
**Dependencies:** US-1 (link target)
**Sprint:** 2

### US-5 — Append "Advanced capabilities" section to `delivery-team/README.md` (1 pt)

**Traces:** Bilbo #5–7 · Galadriel rec #6 · Feature map rows "constraints / board / transformation / paradigms"
**Why:** Shipped capabilities (constraints.yml, Architecture Board, Transformation Planning sub-flow, paradigm selection) have no README footprint. This is the single delivery-team surface a user opens after reading root README.
**Deliverable:** Append-only edit to `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/README.md`
**Acceptance:**
- New section titled "Advanced capabilities" (or "Recent additions") appended near end
- Four short subsections (2–4 lines each): Constraints, Architecture Board, Transformation Planning, Paradigm Selection
- Each subsection: what it does in plain English + "when to use" + link to the authoritative internal reference (`delivery-flow/references/constraints-model-guide.md`, `delivery-flow/references/architecture-board-personas.md`, `architect/references/transformation-planning.md`, `architect/skills/paradigms/` index)
- States clearly that the pipeline is **7 stages** (Transformation is an optional Architect sub-flow, not stage 8) — resolves Q1
- No rewrite of accurate existing content
**Dependencies:** none
**Sprint:** 2

### US-6 — Verify `marketplace.json` + description touch-ups (0.5 pt)

**Traces:** Bilbo top-10 implicit · Galadriel IA §2 · Q4 resolution
**Why:** Ensure registered plugins match on-disk directories and descriptions reflect current capability.
**Deliverable:** Possible edits to `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.claude-plugin/marketplace.json`
**Acceptance:**
- Every top-level plugin directory matches a registered entry and vice versa (no orphans either direction)
- `mtg-commander` description mentions synergy-first deck building + price controls (so Journey B discovery works from `/plugin` browsing)
- `delivery-team` description references constraints / architecture board / transformation if space permits (optional; no harm if unchanged)
- File passes `python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"`
- No structural schema change (no new keys)
**Dependencies:** none
**Sprint:** 1

### US-7 — Cross-link audit + stub integrity (0.5 pt)

**Traces:** Bilbo §5 discoverability gaps · Galadriel §2 dead ends
**Why:** Ensure new user-facing surfaces link both directions (root README ↔ plugin README ↔ SKILL.md for deep reference; existing redirect stubs confirmed working).
**Deliverable:** Edits across touched files from US-1, US-4, US-5
**Acceptance:**
- Root README links to `mtg-commander/README.md`
- `mtg-commander/README.md` links back up to root README and over to `SKILL.md`
- `delivery-team/README.md` Advanced section links to the 4 authoritative internal references (US-5 ACs)
- Existing paradigm redirect stubs (`architect/references/volatility-decomposition.md`, `architect/references/strategic-ddd.md`) still resolve to current targets (grep verification only, no edits unless broken)
- No new dead links introduced (every new `[text](path)` points to an existing file)
**Dependencies:** US-1, US-4, US-5
**Sprint:** 2

### US-8 — Troubleshooting quick-reference placement decision + inline bullet (1 pt)

**Traces:** Galadriel rec #4 · Bilbo §5 discoverability
**Why:** No top-level troubleshooting surface exists. A full `docs/user-guide/troubleshooting.md` is deferred to the MkDocs expansion cycle; this cycle delivers a **lightweight inline troubleshooting block** in the two most-landed-on READMEs.
**Deliverable:** New "Troubleshooting" short section appended to root `README.md` and to `delivery-team/README.md`
**Acceptance:**
- Root README troubleshooting block (≤8 lines) covers: pipeline abort recovery pointer, config drift (v2.7 migration pointer), defect tracking location (`.delivery/defects/`), common error pattern (hook block → check `.claude/settings.local.json`)
- `delivery-team/README.md` troubleshooting block references the same bullets + pipeline-specific: state resume (`/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/state.md` pattern), retrospective enforcement hook behavior
- Both blocks include a "See also" line pointing at `CONTRIBUTING.md` and relevant SKILL.md sections
- Explicitly marked as quick-reference; full page deferred to MkDocs cycle
**Dependencies:** US-5 (same file)
**Sprint:** 2

---

## Story Summary

| ID | Title | Pts | Sprint |
|----|-------|-----|--------|
| US-1 | mtg-commander/README.md | 2 | 1 |
| US-2 | .mtg-commander.yml.example + walkthrough | 1 | 1 |
| US-3 | CLAUDE.md refresh | 1 | 1 |
| US-6 | marketplace.json verification | 0.5 | 1 |
| US-4 | README.md roster + recent additions | 1 | 2 |
| US-5 | delivery-team/README.md Advanced section | 1 | 2 |
| US-7 | Cross-link audit | 0.5 | 2 |
| US-8 | Troubleshooting inline blocks | 1 | 2 |

**Total:** 8 stories · 8 pts · 2 sprints (4 pts each — honors ceiling exactly)

---

## Deferred to Follow-on Cycle (explicitly NOT in this plan)

Galadriel's IA §2 includes these additional surfaces; this cycle defers them because they exceed the 4-pt markdown-tier sprint ceiling:

- `docs/user-guide/constraints.md`, `architecture-board.md`, `transformation-planning.md`, `paradigms.md`, `mtg-config.md`, `troubleshooting.md` (6 new user-guide pages)
- `docs/getting-started/mtg-commander-quick-start.md`
- `docs/skills/mtg-commander.md` + fixes to `delivery-flow.md`, `architect.md`
- `docs/reference/constraints-schema.md` (rendered JSON Schema)
- `mkdocs.yml` + `docs/index.md` rebrand to "Claude Plugins Marketplace"

**Recommended next cycle:** DOCS_ONLY "MkDocs expansion" — 2 sprints, markdown tier, addresses the deferred list.

> *"The Road goes ever on and on." This plan lights the first mile. The rest waits for its season.*
