# Documentation Inventory — Claude-Plugins Repository

*Chronicled by Bilbo Baggins, Storyteller of Journeys*
*Stage: 01-idea · Role: Technical Writer*
*Date: 2026-04-14*

> "I think I'm quite ready for another documentation adventure." So I laced up my boots and walked the repo end-to-end. Here is my honest account of what travelers will find, what has gone stale in the pantry, and which shelves are bare.

---

## 1. Executive Summary

The repo has **three parallel documentation surfaces** — root `README.md`, `CLAUDE.md`, and a MkDocs site under `docs/` — and they have drifted from one another and from the code. The Delivery Team plugin is documented reasonably well at the SKILL.md level and in `docs/skills/`, but none of the **recently shipped primitives** (constraints.yml, Architecture Board, Transformation Planning, paradigm-as-skill restructure, MTG challengers and `.mtg-commander.yml`) have made it into user-facing docs. The `mtg-commander` plugin has **zero** presence in the MkDocs site, `README.md`, or `docs/index.md` despite being registered in `marketplace.json`. The biggest discoverability gap: a new user cloning this repo cannot find the constraints primitive, the architecture board, or transformation planning without reading internal `references/` directories.

---

## 2. What's Current (accurate vs. reality)

- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.claude-plugin/marketplace.json` — lists all 6 plugins including `mtg-commander` (v2.22.0). Matches top-level directories exactly.
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/skills/delivery-flow/references/constraints-model-guide.md` — thorough, well-structured authoring canon for the constraints primitive. Internal doc only, but itself accurate.
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/delivery-team/skills/architect/SKILL.md` (lines 162–230) — paradigm router is documented in-skill and matches the actual `paradigms/volatility/` and `paradigms/ddd/` directories on disk.
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/mtg-commander/SKILL.md` (lines 36–77) — the `.mtg-commander.yml` schema is freshly and accurately documented inside the SKILL.
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/docs/getting-started/quick-start.md` — 3-question quick-start flow accurately reflects current setup wizard behavior.
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/CLAUDE.md` (lines 43, 45, 96) — correctly notes paradigm-aware dev patterns, architect's Prior Art Analysis, and config schema v2.7.

---

## 3. What's Stale (concrete discrepancies)

- **`README.md:59`** — Presentation skill described as "4 types... 3 output formats." CLAUDE.md line 51 and actual SKILL.md declare **9 types + 4 formats (incl. pptx) + narrative intelligence + light mode**. README is a full generation behind.
- **`README.md` (entire file)** — zero mention of `mtg-commander`. `marketplace.json` lists it as a registered plugin; README never acknowledges it.
- **`CLAUDE.md:29-35`** — "Available Plugins" table lists only 5 plugins. Missing `mtg-commander/`. The per-plugin table under delivery-team (lines 40–51) is fine, but the outer plugin roster is incomplete.
- **`CLAUDE.md:45`** — architect described as "11 roles + 4 game architecture + 4 decomposition strategies + Prior Art Analysis." It now also hosts the **paradigm-as-skill router** (volatility, ddd sub-skills) and **Transformation Planning** (phases 1a/1b/2/3). Neither surfaces in CLAUDE.md.
- **`CLAUDE.md` "Delivery-flow pipeline architecture" section (lines 90–106)** — no mention of `constraints.yml` primitive, Architecture Board, or Transformation Planning, despite all three being shipped (BACKLOG-001, 003, 006 per recent commits).
- **`docs/index.md`** — subtitle calls the MkDocs site "Delivery Team Plugin." Repo now contains six plugins; the site never even names the other five. `mkdocs.yml:1-2` similarly scopes the site to delivery-team only.
- **`docs/skills/delivery-flow.md:38`** — "Full wizard: 9+ questions covering project type..." The project-type question was removed in v2.7 per `CLAUDE.md:98`. Discrepancy.
- **`docs/skills/architect.md:61-74`** — still lists decomposition strategies as a flat table; no mention of paradigms having been restructured into sub-skills (`paradigms/volatility/SKILL.md`, `paradigms/ddd/SKILL.md`). No transformation-planning entry under Task Types (the table at lines 47-59 lacks it despite `references/transformation-planning.md` existing).
- **`docs/user-guide/pipeline.md`** — referenced by nav; likely does not reflect transformation stage (stage 08) which exists on disk at `.delivery/artifacts/08-transform/`. Worth verifying on follow-up.

---

## 4. What's Missing (user-facing content that should exist)

- **`docs/user-guide/constraints.md`** — no user-facing "how to author a constraints.yml" guide. The internal `constraints-model-guide.md` is 200+ lines of dense canon written for validators, not authors. New users cannot discover that the primitive exists, let alone write one.
- **`docs/user-guide/architecture-board.md`** — Architecture Board (BACKLOG-003) is shipped. `delivery-flow/references/architecture-board-personas.md` exists. User-facing "when do I convene the board, who are the personas, what does it produce" page: missing.
- **`docs/user-guide/transformation-planning.md`** — BACKLOG-006 shipped with `architect/references/transformation-phase-1a-behavioral.md`, `-1b-structural.md`, `-2-to-be.md`, `-3-roadmap.md`, and `transformation-planning.md`. No user-facing explanation of when to use it or how it plugs into the pipeline.
- **`docs/skills/mtg-commander.md`** — the plugin is registered in `marketplace.json:66-73` but has no MkDocs page, no README mention, no `docs/index.md` link. A user cannot discover it through docs at all.
- **`docs/getting-started/mtg-commander-quick-start.md`** — "build my first deck" walkthrough. The 1,179-line SKILL.md is the only entry point.
- **`docs/reference/constraints-schema.md`** — the JSON Schema at `delivery-flow/references/constraints-schema.json` has no user-facing rendered page.
- **`docs/user-guide/paradigms.md`** — paradigm-as-skill restructure (BACKLOG-005) has no user-facing "how paradigms are selected, how to add one" guide. Architect SKILL.md:210-230 has the internal version.

---

## 5. Discoverability Gaps

- **`mtg-commander` is invisible from the front door.** README, docs/index.md, mkdocs.yml nav — none mention it. Only `marketplace.json` and the plugin directory itself.
- **Constraints primitive has no signpost.** A new architect or PO has no way to know `constraints.yml` exists unless they wander into `delivery-flow/references/`. Not named in `docs/user-guide/config.md`, not in `docs/skills/delivery-flow.md`, not in `README.md`.
- **Architecture Board personas buried.** Only reachable via `delivery-flow/references/architecture-board-personas.md`.
- **Transformation stage hidden.** Directory `.delivery/artifacts/08-transform/` exists, but `docs/user-guide/pipeline.md` nav entry and `docs/index.md` still advertise only 7 stages (the 7-stage claim appears in `docs/index.md:12` and `README.md:49`). An 8th transformation stage or sub-flow is not described anywhere user-facing.
- **Paradigm sub-skills are not discoverable.** A user asking "can I add a new architecture paradigm?" finds no README, no docs page — only the inline discussion in `architect/SKILL.md:210-230`.
- **MkDocs site branding mismatch.** Site titled "Claude Plugins - Delivery Team" implies the repo is one plugin. It's six.

---

## 6. Top 10 Documentation Priorities (honest ranking)

1. **Add `mtg-commander` to README, docs/index.md, mkdocs.yml nav, and create `docs/skills/mtg-commander.md`.** It is a shipped, registered plugin with zero user-facing presence. Highest severity.
2. **Write `docs/user-guide/constraints.md`** — authoring guide for the constraints primitive, linked from pipeline and config pages. The primitive is foundational and utterly invisible.
3. **Update `CLAUDE.md` Available Plugins table** (lines 29–35) to include `mtg-commander/` and add constraints/Architecture Board/Transformation bullets to the Delivery-flow architecture section.
4. **Refresh `README.md:59` Presentation row** to reflect 9 types + 4 formats + narrative intelligence + light mode, and add an MTG Commander entry to the plugin roster.
5. **Write `docs/user-guide/transformation-planning.md`** — explains when AS-IS/TO-BE/roadmap phases run, what artifacts they produce, and how they fit with the 7-stage pipeline (or is it 8 now? clarify).
6. **Write `docs/user-guide/architecture-board.md`** — surfaces persona roster, trigger conditions, outputs.
7. **Write `docs/user-guide/paradigms.md`** — explains paradigm router, how selection works, how to contribute a new paradigm sub-skill.
8. **Fix `docs/skills/delivery-flow.md:38`** — remove the stale "project type" wizard question reference (it was removed in v2.7).
9. **Rebrand MkDocs site** from "Delivery Team" to the full "Claude Plugins" marketplace — update `mkdocs.yml:1-2`, `docs/index.md` subtitle, and add top-level plugin index page.
10. **Update `docs/skills/architect.md`** Task Types table to include transformation-planning and add a "Paradigm Sub-Skills" section referencing `paradigms/volatility/` and `paradigms/ddd/`.

---

*"The Road goes ever on and on, down from the door where it began." There is much chronicling left to do, but this is the state of the pantry as I found it.*
