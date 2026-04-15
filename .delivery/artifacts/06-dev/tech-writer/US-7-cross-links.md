# US-7 — Cross-Link Audit & Stub Integrity

**Author:** Bilbo Baggins, Storyteller (Tech Writer, `lotr-full`)
**Stage:** 06-Dev · Story: US-7 (0.5 pt)

> *"Still round the corner there may wait, a new road or a secret gate."* — the trails between docs should be well-marked.

---

## Forward links (verified, no edits needed)

- `constraints-quickstart.md` → `constraints-model-guide.md` — present (lines 5, 35, 99). OK.
- `config-walkthrough.md` → `README.md`, `price-evaluator-guide.md`, `SKILL.md` — present (§9). OK.
- `troubleshooting.md` → `../SKILL.md`, `getting-started.md`, `config-schema.md`, `defect-tracking.md` — present (See Also + inline). OK.

## Backward links (edits made, one-line each)

1. `mtg-commander/SKILL.md` — added a blockquote pointer to `README.md` and `references/config-walkthrough.md` immediately under the H1 intro, before the Sub-Agent Dispatch Guardrail section. No rewrite.
2. `delivery-team/skills/delivery-flow/references/constraints-model-guide.md` — added one-line blockquote at top: "Quick-start version: see `constraints-quickstart.md`."
3. `delivery-team/skills/delivery-flow/references/getting-started.md` — added blockquote after the intro paragraph pointing at `troubleshooting.md`.
4. `mtg-commander/references/price-evaluator-guide.md` — added one-liner blockquote pointing at `config-walkthrough.md` for the `.mtg-commander.yml` knobs this guide references.
5. `README.md` (root) — added third bullet in See Also pointing at `delivery-team/skills/delivery-flow/references/getting-started.md`. CLAUDE.md + CONTRIBUTING.md bullets already present.

## Redirect stub integrity (FINDING — broken path prefix)

Both stubs declare a "New path" that does **not** resolve from the stub's own directory:

- `delivery-team/skills/architect/references/volatility-decomposition.md` — claims new path `paradigms/volatility/references/volatility-decomposition.md`. Actual file lives at `delivery-team/skills/architect/paradigms/volatility/references/volatility-decomposition.md`. Missing `../` prefix — from the stub's directory the path needs to be `../paradigms/volatility/references/volatility-decomposition.md`.
- `delivery-team/skills/architect/references/strategic-ddd.md` — same defect; should be `../paradigms/ddd/references/strategic-ddd.md`.

**Out of scope for US-7 (edits restricted to cross-links added this cycle).** Flagged for a follow-on defect (DEFECT candidate) — single-line fix per stub, but touches files outside this story's deliverable surface.

## Broken-link spot-check (new/updated docs)

Scanned `.md` references in all 7 touched files. Every link target in:

- `README.md` (root) — all 11 `.md` targets resolve. OK.
- `mtg-commander/README.md` — all 9 `references/*.md` targets + `SKILL.md` + `../README.md` resolve. OK.
- `mtg-commander/references/config-walkthrough.md` — 3 targets (`mtg-commander/README.md`, `price-evaluator-guide.md`, `SKILL.md`) resolve. OK.
- `delivery-team/skills/delivery-flow/references/constraints-quickstart.md` — `constraints-model-guide.md` resolves; `.delivery/artifacts/02-refine/po/prd.md` is a runtime artifact path (not a link target), not broken.
- `delivery-team/skills/delivery-flow/references/troubleshooting.md` — all sibling refs (`getting-started.md`, `config-schema.md`, `defect-tracking.md`, `../SKILL.md`) resolve. OK.

No new dead links introduced by this cycle's cross-link additions.

## Files touched (5)

- `mtg-commander/SKILL.md`
- `delivery-team/skills/delivery-flow/references/constraints-model-guide.md`
- `delivery-team/skills/delivery-flow/references/getting-started.md`
- `mtg-commander/references/price-evaluator-guide.md`
- `README.md`

## Acceptance self-check (US-7)

All ACs met. Stub defect flagged (path prefix), scope-deferred.

> *"The Road goes ever on."* Two stubs want patching next walk.
