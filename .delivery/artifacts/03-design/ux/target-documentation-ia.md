# Target Documentation Information Architecture

**Designer:** Galadriel, Lady of the Golden Wood (UX, `lotr-full` alias)
**Stage:** 03-design · Project type: DOCS_ONLY
**Paired with:** Bilbo Baggins (Tech Writer) — inventory in `01-idea/tech-writer/`

> *"I give you the light of Eärendil, our most beloved star. May it be a light to you in dark places, when all other lights go out."* So too must these pages become a light for the traveler. Here is the shape of the wood after the pruning.

---

## 1. Convergence Summary — Where Bilbo and I Agree

The four shadows both the Storyteller and I named (highest priority — corroborated):

1. **`mtg-commander` is invisible from the front door.** No `README.md` in the plugin dir; no mention in root `README.md`; absent from `docs/` site. (Bilbo #1 / Galadriel #1, #2)
2. **`docs/` MkDocs site is mis-branded as "Delivery Team"** when the repo is a six-plugin marketplace. (Bilbo #9 / Galadriel #3)
3. **`constraints.yml` primitive has no user-authoring page** — only an internal validator-facing canon in `references/`. (Bilbo #2 / Galadriel #5)
4. **`CLAUDE.md` and root `README.md` have drifted** — Presentation skill stats stale, `mtg-commander` omitted from plugin roster, recent primitives (constraints, Architecture Board, Transformation Planning, paradigm sub-skills) unmentioned. (Bilbo #3, #4 / Galadriel #6)
5. **Recently-shipped capabilities hide in `references/`** — Architecture Board, Transformation Planning, paradigm router have no user-guide tier. (Bilbo #5–7 / Galadriel #5, #6)

---

## 2. Target Doc Tree — The Shape After the Work

**Repo root (unchanged location, refreshed content):**
- `README.md` — add `mtg-commander` row; refresh Presentation row; add "Recently shipped" callout (constraints, Architecture Board, Transformation, paradigms).
- `CLAUDE.md` — extend Available Plugins table to 6; add constraints/Architecture Board/Transformation/paradigm bullets under delivery-flow architecture section.
- `CONTRIBUTING.md` — unchanged (out of scope this cycle unless user requests).
- `.claude-plugin/marketplace.json` — verify all 6 plugins present and descriptions current (sync check only; no schema change).

**Per-plugin `README.md` (plugin-dir level):**
| Plugin | Has README? | Action |
|--------|-------------|--------|
| `delivery-team/` | Yes | Append "Advanced capabilities" section: constraints.yml, Architecture Board, Transformation Planning, paradigm sub-skills |
| `agentic-flow-builder/` | Yes | No change unless drift found |
| `prompt-engineer/` | Yes | No change |
| `prd-quality-gate-flow/` | Yes | No change |
| `research-agent/` | Yes | No change |
| `mtg-commander/` | **No** | **CREATE** — mirror delivery-team README pattern; inline `.mtg-commander.yml` example; price-escalation explainer; quick-start |

**`docs/` MkDocs tree (rebranded + expanded):**
- `docs/index.md` — rebrand subtitle to "Claude Plugins Marketplace"; plugin index grid (6 cards).
- `docs/getting-started/` — keep `installation.md`, `quick-start.md`, `commands.md`; add `mtg-commander-quick-start.md`.
- `docs/user-guide/` — keep `config.md`, `pipeline.md`, `project-types.md`, `collaboration.md`; **add** `constraints.md`, `architecture-board.md`, `transformation-planning.md`, `paradigms.md`, `mtg-config.md`, `troubleshooting.md`.
- `docs/skills/` — keep 12 existing pages; **add** `mtg-commander.md`; fix stale bits in `delivery-flow.md` and `architect.md`.
- `docs/reference/` — keep `aliases.md`, `hooks.md`, `memory.md`; add `constraints-schema.md` (rendered from JSON Schema).
- `mkdocs.yml` — `site_name` → "Claude Plugins"; extend nav to include new pages.

---

## 3. User Journey Alignment — Three Travelers, Three Paths

**Journey A — Pipeline user** ("run delivery on my project"):
`README.md` (plugin roster) → `delivery-team/README.md` → `docs/getting-started/quick-start.md` → `docs/user-guide/pipeline.md` → *(new)* `docs/user-guide/constraints.md` when authoring constraints → `docs/user-guide/architecture-board.md` when board triggers → `docs/user-guide/troubleshooting.md` on failure. **Required new/updated files:** 4.

**Journey B — MTG deck builder** ("build a $100 budget Azorius deck"):
`README.md` (new mtg-commander row) → *(new)* `mtg-commander/README.md` → *(new)* `docs/getting-started/mtg-commander-quick-start.md` → *(new)* `docs/user-guide/mtg-config.md` for `.mtg-commander.yml` authoring → `docs/skills/mtg-commander.md` for reference. **Required new files:** 4. *The unmarked path becomes lit.*

**Journey C — Contributor** ("add a new paradigm sub-skill"):
`README.md` → `CONTRIBUTING.md` → *(new)* `docs/user-guide/paradigms.md` (explains router + how to add a paradigm) → `plugin-dev` skills (unchanged). **Required new files:** 1.

---

## 4. Feature Discoverability Map — Where Each Feature Lives

| Feature | Primary teaching file | Secondary surfaces |
|---------|----------------------|---------------------|
| `constraints.yml` primitive | `docs/user-guide/constraints.md` (new, author-facing) | `delivery-team/README.md` advanced section; `docs/reference/constraints-schema.md`; linked from `pipeline.md` and `config.md` |
| Architecture Board | `docs/user-guide/architecture-board.md` (new) | `delivery-team/README.md`; `CLAUDE.md` architecture bullet; cross-linked from `collaboration.md` |
| Transformation Planning | `docs/user-guide/transformation-planning.md` (new) | `delivery-team/README.md`; `docs/skills/architect.md` Task Types table; `pipeline.md` (clarify 7-vs-8 stage question) |
| Paradigm-as-skill | `docs/user-guide/paradigms.md` (new) | `docs/skills/architect.md` (add "Paradigm sub-skills" section); existing redirect stubs retained |
| MTG Challengers + `.mtg-commander.yml` | `mtg-commander/README.md` (new) + `docs/user-guide/mtg-config.md` (new) | `docs/skills/mtg-commander.md`; `docs/getting-started/mtg-commander-quick-start.md`; root README entry |

---

## 5. Scope Bounds — What This Cycle Will and Will Not Touch

**IN scope (DOCS_ONLY):**
- Root `README.md` + `CLAUDE.md` refresh
- New `mtg-commander/README.md`
- Append-only updates to `delivery-team/README.md`
- New `docs/user-guide/` pages: constraints, architecture-board, transformation-planning, paradigms, mtg-config, troubleshooting
- New `docs/getting-started/mtg-commander-quick-start.md`
- New `docs/skills/mtg-commander.md` + fixes to `delivery-flow.md`, `architect.md`
- New `docs/reference/constraints-schema.md`
- `docs/index.md` + `mkdocs.yml` rebrand and nav expansion
- `marketplace.json` sync verification (descriptions only, no structural change)

**OUT of scope (do not touch):**
- `SKILL.md` files — those are Claude-facing instructions, not user docs
- `references/` directories — internal canon; new user-guide pages link TO them, don't replace
- `CONTRIBUTING.md` expansion (Bilbo/Galadriel rec #8 deferred to a future cycle unless user pulls it in)
- Code changes, schema changes, new features, config-schema version bumps
- ADRs, backlog items, implementation logs
- Rewriting existing per-plugin READMEs that are not drifted

---

## 6. Stop Points — Where the Quill Rests

- **We do not document unshipped features.** Only capabilities present on `main` at cycle start.
- **We do not inline internal canon.** User-guide pages reference `references/*.md` but never copy them.
- **We do not document ADRs or backlog items.** Those are decision records, not user pathways.
- **We stop at the user-guide tier.** Going deeper (architecture internals, validator logic) belongs in `references/`, which is out of scope.
- **We do not rewrite what is accurate.** Append, correct, and cross-link — do not refactor for its own sake.

---

## 7. PO + Architect Design-Sprint Applicability

**No.** This is a Tech Writer + UX paired effort through Plan and Dev. No architectural decisions are made: no new schemas, no new primitives, no structural trade-offs. The Architect should not be convened. PO already briefed; next hand-off is to the Tech Writer at Plan stage for file-by-file authoring order.

---

## 8. Open Questions for Plan Stage

1. **Stage count semantics:** Bilbo flagged that `.delivery/artifacts/08-transform/` exists but `README.md` and `docs/index.md` still say "7 stages." Is transformation an 8th stage, a sub-flow of Architect, or an optional phase? The Tech Writer needs a canonical answer before writing `docs/user-guide/pipeline.md` and `transformation-planning.md`. *Recommended source: ask Architect in a single targeted question, not a full convening.*
2. **`docs/` site rebrand strategy:** expand to cover all six plugins (larger effort) vs. narrow to "Delivery Team" and add a second index for the marketplace? My recommendation: **expand**, since the URL is already `Claude-Plugins`. Confirm with PO before Plan.
3. **`mtg-commander/README.md` depth:** lightweight (pattern-mirror of delivery-team) or full tutorial with example deck? Recommend lightweight; tutorial belongs in `docs/getting-started/mtg-commander-quick-start.md`.
4. **Marketplace.json sync:** is a description refresh in-scope, or verification-only? Recommend verification-only this cycle.

---

> *"The quest stands upon the edge of a knife. Stray but a little, and it will fail."* Hold to these bounds, Storyteller. The light will find the travelers.
