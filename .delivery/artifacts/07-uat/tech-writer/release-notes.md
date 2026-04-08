# Release Notes — Orchestration Discipline Bundle

*"Hobbits may be small folk, but the discipline they keep is sturdy as mithril. Sit a while by the fire, and let me tell you what has changed."*
— Bilbo, your tech-writer for the evening

**Release**: delivery-team v2.18.0
**Schema**: `.delivery/config.yml` v2.6 → **v2.7**
**Closes**: #73, #71, #70, #69
**Pipeline run date**: 2026-04-05

---

## In a nutshell

Four small lapses had crept into the delivery-flow orchestrator like mice into a pantry. Individually each was forgivable; together they let the pipeline quietly fib about its own behavior. This bundle sweeps all four out at once — and the orchestrator was made to dogfood the very discipline it is being taught.

If you only read one paragraph: the orchestrator now re-detects project type on **every** run, refuses to write artifacts itself, dispatches **one sub-agent per role** (no compound prompts), and runs an **isolated adversarial loop** at the Architect stage with proper convergence rules.

---

## Breaking change — please read

**`project_type` has been removed from `.delivery/config.yml`.**

- The schema is now **v2.7**. The setup wizard no longer asks for project type and no longer writes the key.
- Legacy v2.6 configs that still carry a top-level `project_type:` will **still load** — they will not error. The key is read once, logged as deprecated in the stage banner and `.delivery/state.md` ("legacy `project_type` ignored — re-detecting from request"), and then dropped. This is the **warn-and-drop** migration.
- If you genuinely want to pin a project type (for instance, a docs-only repo that should never trigger code stages), use the new opt-in override:

  ```yaml
  routing:
    force_type: DOCS_ONLY
  ```

  Phase 1 detection still runs and is logged, but the routing decision uses your pin and announces it in the stage banner. The key is namespaced under `routing.` deliberately, so pinning is a discoverable, intentional act rather than a frozen guess from setup-time.

**What you should do**: nothing urgent. Existing repos keep working. When you next edit your config, drop the bare `project_type` line and (if you need it) add `routing.force_type` instead. Bump `config_version` to `"2.7"` while you are there.

---

## Schema v2.6 → v2.7 migration

- `config_version` bumped from `"2.6"` to `"2.7"`.
- `project_type` removed from the active schema. Documented under a new **Deprecated Keys** section in `references/config-schema.md` with migration notes.
- New: `routing.force_type` (optional, default `null`) — the only supported way to pin project type at the config layer.
- New: `pipeline.enforce_self_write_block` — defaults to `true` on fresh v2.7 configs and `false` on tolerantly-parsed v2.6 configs. This gates the orchestrator self-write soft-deny so legacy repos are never broken by the upgrade.
- `max_self_correction` (already present in v2.6) is now also documented as the cap for Architect adversarial loops. Default remains **3**.
- Setup wizard reduced from 10 questions to **9** (the project-type question is gone; remaining questions renumbered).
- Derived `references/config-schema.json` regenerated from the markdown source via `delivery-team/scripts/generate-schema.py`.
- Documentation parity sweep: `CLAUDE.md`, `README.md`, `delivery-team/README.md`, `.claude-plugin/marketplace.json`, and the `docs/` site (`user-guide/config.md`, `skills/delivery-flow.md`, `contributing/index.md`) all now declare v2.7 as current.

---

## Orchestrator delegation enforcement (Step 4.5 + anti-patterns)

The orchestrator no longer grants itself "this is simple enough" exemptions. The pipeline's whole point — context isolation, role specialization, DoD enforcement — is voided the moment the orchestrator drafts its own artifacts.

What changed:

- **Delegation Prime Directive** (SKILL.md, top of file): *The orchestrator NEVER writes artifacts, source files, or implementation content during a pipeline run. There are no "simple enough" exemptions.* This block is now the first prose section of `SKILL.md` and is referenced from Step 4.5, the stage descriptions, and the anti-patterns section.
- **Step 4.5 tightened**: A new "Rejected justifications" sub-section explicitly turns away "but it's simple", "I already know the answer", "faster if I do it", and "no sub-agent exists". If no skill fits, the orchestrator escalates to the user — it does not self-write.
- **Common Orchestrator Anti-Patterns** (new SKILL.md section): eight named anti-patterns drawn from real Prime Directive violations — Simplicity Shortcut, Compound Reviewer Prompt, Frozen Type Routing, Single-Pass Adversarial, Inline Artifact Authoring, Context Leak Across Loops, Light-as-Skip, and Fusing Validator with Producer. Each entry names the smell, describes it in a line, and gives the correct alternative.
- **`enforce_pipeline_scope.py` extended** with a layered origin-detection strategy:
  - Layer 1 — env var (`CLAUDE_AGENT_ID` / `DELIVERY_FLOW_AGENT_CONTEXT`) on every sub-agent dispatch.
  - Layer 2 — hook-input metadata (`parent_tool_use_id`, `frame.is_subagent`).
  - Layer 3 — soft-deny fallback: a loud `systemMessage` rather than a hard block, preserving the "never break a user pipeline" guarantee.
  - Allowlist for orchestrator-owned routing files: `.delivery/state.md`, `state.tmp.md`, `config.yml`, `memory/**`, plus per-stage routing artifacts.
  - Activation gated on `config_version >= 2.7` AND `pipeline.enforce_self_write_block: true`, so legacy v2.6 repos are unaffected on upgrade.
  - **Known gap (documented, not fixed)**: Bash redirection (`>`, `>>`, `tee`, `cat <<EOF`) is not yet intercepted. Tracked in the hook docstring and in `references/quality-gates.md` "Known Hook Limitations" so DoD validators apply the meta-gate manually.
- **Delegation Meta-Gate** added to `references/quality-gates.md`: before DoD can pass, the orchestrator must confirm every domain artifact in the stage was written by a dispatched sub-agent. Orchestrator-authored artifacts fail the meta-gate regardless of validator votes.

---

## One Role = One Sub-Agent (across every collaboration pattern)

Multi-reviewer patterns were quietly being collapsed into single sub-agent prompts that asked one agent to "play three roles." Context isolation became theater. No more.

What changed:

- **"One Role = One Sub-Agent" rule block** added prominently in `SKILL.md` next to the Delegation Prime Directive, with worked examples: a review board is **3** Agent calls; DoD validation is **4** calls; debate is PRO + CON + JUDGE as **3** calls; an adversarial loop is **N fresh** calls.
- **`references/team-patterns.md`**: every collaboration pattern (Evaluator-Optimizer, Adversarial Review, Multi-Perspective Review Board, Decision Ownership Routing, Debate, Consensus) now leads with the same one-line **Dispatch rule** — separate Agent tool calls per named role, no compound prompts ever.
- **`references/pipeline-stages.md`**: a header note clarifies that `[PARALLEL]` and `[SEQUENTIAL]` annotations imply *one Agent tool call per listed role*, never combined sub-agents.
- **`references/quality-gates.md`**: "One validator = one Agent invocation" rule added immediately after the DoD validator prompt template.
- **`audit_agent_prompt.py`** extended with three compound-role detectors:
  1. Multiple `ROLE:` declarations in a single prompt (structural).
  2. Phrases like "also act as", "then act as", "additionally play", "and also play".
  3. Two `You are ...` declarations within a 200-character window.
  - All detectors are **non-blocking warnings** that append to the existing isolation audit message.
  - **Negation-aware**: the phrasal detectors now skip warnings when the trigger appears in a negated context ("do not act as both…", "never play both…"), so the orchestrator can still send anti-pattern guidance text without tripping its own alarm. Stdlib only.

---

## Isolated Adversarial Loop at the Architect stage

The Architect stage previously ran a single adversarial pass. The reviewer anchored on the first issues found, deeper structural problems slipped through, and a single zero-finding loop was wrongly treated as proof of convergence. The new pattern fixes both halves of the problem.

What changed:

- New **Pattern 2b: Isolated Adversarial Loop** added to `references/team-patterns.md` as a variant of Adversarial Review. Each loop dispatches a **fresh** reviewer sub-agent whose prompt contains *only* the current architecture artifact and the standard adversarial brief — **no findings from prior loops, no summaries of what was fixed, no "this is loop N" hints**. This is the core anti-anchoring guarantee.
- **Issue-class taxonomy** introduced for findings: `coupling | security | data-integrity | naming | testability | performance | docs` (untagged → `misc`, treated as a new class). Used by the convergence rules below.
- **Convergence rules** (a single clean pass is **not** enough — fresh reviewers may surface disjoint critique sets):
  1. **Two-clean** — two *consecutive* loops return zero findings.
  2. **No-new-classes** — the last 2 loops still produced findings, but every finding belongs to an issue class already raised earlier (the architect documents residual same-class issues and proceeds).
  3. **Hard cap** — N reaches `max_self_correction` (default 3). Exit as `cap_reached`. Residual findings are surfaced to the human checkpoint. Cap-reached is a **documented exit**, not a failure.
- **Stage 4 (Architect)** in `references/pipeline-stages.md` now references the Isolated Adversarial Loop pattern by name, calls out the loop cap, and mandates a fresh sub-agent dispatch per iteration.
- **`max_self_correction`** is documented in `references/config-schema.md` v2.7 with "Architect adversarial loop cap" listed among its uses. Default remains **3**.

---

## Files of note

- `delivery-team/skills/delivery-flow/SKILL.md`
- `delivery-team/skills/delivery-flow/references/config-schema.md` (+ regenerated `config-schema.json`)
- `delivery-team/skills/delivery-flow/references/setup-wizard.md`
- `delivery-team/skills/delivery-flow/references/team-patterns.md`
- `delivery-team/skills/delivery-flow/references/pipeline-stages.md`
- `delivery-team/skills/delivery-flow/references/quality-gates.md`
- `delivery-team/skills/delivery-flow/references/project-types.md`
- `delivery-team/hooks/enforce_pipeline_scope.py`
- `delivery-team/hooks/audit_agent_prompt.py`
- `CLAUDE.md`, `README.md`, `delivery-team/README.md`
- `.claude-plugin/marketplace.json` (version → 2.18.0)
- `docs/user-guide/config.md`, `docs/skills/delivery-flow.md`, `docs/contributing/index.md`

---

## Upgrade checklist

- [ ] Pull the new release; no action required for existing pipelines to keep running.
- [ ] When convenient, bump `config_version` in your `.delivery/config.yml` to `"2.7"`.
- [ ] Remove the bare `project_type:` key from your config (it will be warn-and-dropped on next run regardless).
- [ ] If you previously relied on a pinned project type, add `routing.force_type: <TYPE>` under a new `routing:` block.
- [ ] If you maintain a docs-only repo, consider `routing.force_type: DOCS_ONLY` for safety.
- [ ] Skim the new "Common Orchestrator Anti-Patterns" section in `SKILL.md` — it is short and the lessons are hard-won.

---

*"And so the road goes ever on — but it goes through delegation, isolation, iteration, and truth. A second breakfast on the discipline of the pipeline, and the pantry is tidy once more."*

— Bilbo, tech-writer
