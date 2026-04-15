# Documentation UX Review — First-Time User Discovery Experience

**Reviewer:** Galadriel, Lady of the Golden Wood (UX Designer alias — lotr-full)
**Stage:** 01-idea (discovery, parallel to Bilbo's inventory)
**Scope:** Navigation, discoverability, progressive disclosure — NOT completeness

---

> *"I know what it was that you last saw. For it is also in my mind. Do not be afraid. But do not think that only by singing amid the trees, nor even by the slender arrows of elven-bows, is this land of Lothlórien maintained and defended against its Enemy."*

So too is a repository defended — or betrayed — by its first pages. The traveler who arrives in Caras Galadhon of code must be welcomed, oriented, led. Let us see what this marketplace offers the pilgrim who has only just dismounted.

---

## 1. First-Contact Assessment — The First Sixty Seconds

The traveler arrives at `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/`. What greets them?

- **`README.md` — PRESENT and substantial** (166 lines). Opens with a clear "What is this?" section, an install snippet, and a plugin-by-plugin table. This is a strong first welcome. The path to "install and try" is visible within fifteen seconds.
- **`CLAUDE.md` — PRESENT, scannable.** Heavy use of tables (plugin inventory, hook events, skills matrix). It orients the AI, not the human, but a human reading it will comprehend.
- **`CONTRIBUTING.md` — PRESENT** (223 lines). Strong structural quality — prerequisites, quick start, plugin layout, PR process.
- **`docs/` site (mkdocs material)** — present at repo root, published to `p47phoenix.github.io/Claude-Plugins/`. Index invites "new here?" to `getting-started/installation.md`.

**First impression: warm.** A traveler has three valid entry points (`README.md`, `docs/index.md`, `CONTRIBUTING.md`) and will not be lost in the first minute.

**BUT — the shadow in the mirror:** The README advertises **five plugins**. Only the **delivery-team** plugin is represented in `docs/`. `mtg-commander`, referenced throughout `.delivery/artifacts/` and registered in `marketplace.json`, **is not mentioned in `README.md` at all**. A user who arrives expecting to find it will feel the Enemy's misdirection.

---

## 2. Navigation Hierarchy — Dead Ends, Broken Paths, Orphan Doors

### Strong paths
- `README.md` → `CONTRIBUTING.md` → `plugin-dev` skills — linked, honest.
- `README.md` → per-plugin `README.md` — `delivery-team/README.md`, `agentic-flow-builder/README.md`, `prompt-engineer/README.md`, `research-agent/README.md`, `prd-quality-gate-flow/README.md` all exist.
- `delivery-team/README.md` → `skills/delivery-flow/references/getting-started.md` — explicit cross-link.
- `.delivery/README.md` exists and orients the pipeline-state directory.

### Dead ends and orphans
- **`mtg-commander/` has NO README.md.** Its `SKILL.md` is the ONLY entry point. Someone browsing the repo on GitHub and clicking into `mtg-commander/` sees a directory with four items and no introduction. This is the single largest first-contact gap.
- **`docs/` site is delivery-team-only.** `mkdocs.yml` site_name reads "Claude Plugins - Delivery Team." There is no section in `docs/` for `mtg-commander`, `research-agent`, `agentic-flow-builder`, `prd-quality-gate-flow`, or `prompt-engineer`. The published site actively misleads: it markets itself as the plugin marketplace documentation but covers one-fifth of the plugins.
- **`docs/index.md` opens with "Delivery Team Plugin"** — not "Claude Plugins." A user who reached the site expecting the marketplace finds themselves in a single-plugin pamphlet with no bridge back.
- **Redirect stubs at `architect/references/volatility-decomposition.md` and `architect/references/strategic-ddd.md`** — these DO work correctly. They announce the move, give the new path (`paradigms/volatility/SKILL.md`, `paradigms/ddd/SKILL.md`), and label themselves as backward-compatibility stubs. Good navigation hygiene. A reader will not be stranded.
- **No top-level `docs/troubleshooting.md` or FAQ.** The word "troubleshoot" appears only in operations references and a prompt-engineer README. When a pipeline aborts, a config drifts, or a hook blocks a session, the user has no designated surface to consult.

---

## 3. Progressive Disclosure — Is the Three-Level Convention Honored?

CLAUDE.md declares the three-level loading convention: metadata → SKILL.md → references/on-demand.

- **Level 1 (metadata / `marketplace.json`)** — I did not verify the file directly here, but READMEs consistently mirror marketplace entries. Clear enough for humans scanning from GitHub.
- **Level 2 (SKILL.md front-loading)** — Mixed. `mtg-commander/SKILL.md` opens with name/description/license YAML, then the role, then immediately dives into a **Sub-Agent Dispatch Guardrail** in the first 30 lines. Mechanics precede a "why you might use this" narrative. A human skimming it gets a compliance lecture before a product promise. The delivery-flow SKILL.md (not re-read here, but evident from the ecosystem) is more purpose-forward.
- **Level 3 (references/ on-demand)** — Reasonably discoverable from each SKILL.md for the plugins I examined. `architect/references/` has 27 files covering ADRs, patterns, transformation phases. `delivery-flow/references/` is similarly rich. The question is not whether they exist but whether a user would know which to open first. They would not. There is no "reference index" or "what to read when" map in either references/ directory.

---

## 4. Feature Discoverability — Per-Feature Verdict

Can a first-time user discover each feature **without reading ADRs, backlog items, or implementation logs?**

| Feature | Discoverable? | Via | Gap |
|---------|--------------|----|-----|
| **`constraints.yml` primitive** | Partially | `delivery-flow/references/constraints-model-guide.md` + templates under `references/templates/` | Not surfaced from `README.md` or `docs/`. A user writing one for the first time must already know the word "constraints" to find it. |
| **Architecture Board config block** | Poorly | Only inside `references/architecture-board-personas.md` + schema. No user-guide-level "how to enable the architecture board" page. | No README-visible entry; users must spelunk config-schema.md. |
| **`.mtg-commander.yml` user-repo config** | Inside SKILL.md only | `mtg-commander/SKILL.md` has the schema inline | Zero README teaching. A user who installs `mtg-commander` and never invokes it won't learn this file exists. **Biggest user-config discoverability gap.** |
| **Transformation planning capability** | Barely | `architect/references/transformation-planning.md` + 4 phase files | Not announced in `README.md`, `delivery-team/README.md`, or `docs/`. Only `BACKLOG-006` tells the origin story. A brownfield user will not know the pipeline supports AS-IS → TO-BE. |
| **Paradigm sub-skills (volatility, ddd)** | Via redirect stubs | Stubs present; new paths stated | Parent architect SKILL.md must advertise the router. Needs verification that the SKILL.md points at `paradigms/` — the stubs do their job but a user who never loads the old path never learns paradigms exist. |

---

## 5. User Journey Walkthroughs

### Journey A — "I want to use the delivery pipeline on my project"
`README.md` (install block) → `/plugin install delivery-team` → `delivery-team/README.md` → "quick start" instruction → `delivery-flow/references/getting-started.md` → wizard runs. **Friction: low.** `docs/getting-started/quick-start.md` is a clean mirror. The traveler reaches the wizard in three clicks. *Well-lit.*

### Journey B — "I want to build an MTG deck with price controls"
`README.md` → **silence.** The plugin is not listed. The user must already know the phrase "mtg commander" to grep for it, or discover it through `marketplace.json` or `/plugin` browsing. Once inside `mtg-commander/`, there is **no README** — only `SKILL.md`. The price-control schema (`.mtg-commander.yml`, `max_card_price`, `escalation`) lives inside SKILL.md but is not referenced in any repo-root or plugin-level entry. **Friction: severe.** A user cannot configure price goals without reading the agent-facing SKILL.md end-to-end. *The path into the wood is unmarked.*

### Journey C — "I want to add a new plugin to this marketplace"
`README.md` → "Contributing" link → `CONTRIBUTING.md`. `CONTRIBUTING.md` is strong: prerequisites, structure template, marketplace.json example, hooks.json example, plugin-dev skill list, config extension protocol. **Friction: low-to-moderate.** Gap: there is no worked example of a minimum-viable new plugin PR, and no "first contribution" checklist. A motivated contributor gets there; a tentative one may hesitate.

---

## 6. Top UX Recommendations (Ranked, Complementing Bilbo's Inventory)

1. **Write `mtg-commander/README.md`.** Mirror the pattern of `delivery-team/README.md`. Include the `.mtg-commander.yml` example inline. Closes the largest discoverability hole in the repo. *One hour of work, enormous return.*
2. **Add `mtg-commander` (and the other three plugins) to `README.md`.** A four-line section each. Stop advertising a marketplace and delivering a solo act.
3. **Rebrand `docs/` site.** Either (a) rename to "Delivery Team Documentation" and link it from README under delivery-team specifically, OR (b) expand nav to cover every plugin. Today it deceives by presenting itself as the whole.
4. **Add `docs/troubleshooting.md`** (or `docs/user-guide/troubleshooting.md`). Cover: pipeline abort recovery, config validation errors, hook failures, `.delivery/state.md` corruption. Link from `README.md` and every per-plugin README.
5. **Surface user-facing primitives in user-guide tier.** `constraints.yml` and `.mtg-commander.yml` are user-authored YAML. They deserve `docs/user-guide/constraints.md` and `docs/user-guide/mtg-config.md` pages — not burial in `references/`. References are for the AI; user-guide is for the human.
6. **Add feature announcements to `delivery-team/README.md`.** Transformation planning, architecture board, paradigm skills (volatility/DDD) are all live capabilities with no README footprint. One "Recent additions" or "Advanced capabilities" section would catch them.
7. **Front-load purpose in `mtg-commander/SKILL.md`.** Move the "why you'd use this" two-sentence summary above the Sub-Agent Dispatch Guardrail. Guardrails are for the agent; purpose is for the human reading the file on GitHub.
8. **Add a "first contribution" walkthrough to `CONTRIBUTING.md`.** A narrated example PR (e.g., "add a new reference file to developer skill") lowers the activation energy for drive-by contributors.

---

> *"Even the smallest person can change the course of the future."* A README is the smallest thing. Write one for `mtg-commander` and the course bends.

**End of review.**
