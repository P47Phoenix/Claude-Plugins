# OD-all — Orchestration Discipline Bundle Implementation Notes

**Developer**: Gimli, son of Glóin — built by dwarf-craft. It will hold.
**Stage**: 06 — Development
**Scope**: Stories OD-01 through OD-13, implemented sequentially per sprint plan.

---

## Story-by-story implementation record

### OD-01 — Remove `project_type` pin from Phase 0 config load (SKILL.md)

- Replaced the "Skip Phase 1 (type detection) — use `project_type` from config"
  bullet in Phase 0 with a directive that Phase 1 ALWAYS runs, along with the
  v2.6 warn-and-drop migration and the `routing.force_type` opt-in override.
- No other Phase 0 semantics changed.

### OD-02 — Rewrite Phase 1 note (SKILL.md)

- Replaced the old Phase 1 header note ("If config contains `project_type`,
  this phase is skipped …") with "Phase 1 runs on EVERY pipeline invocation.
  Project type is a runtime routing decision, not a config setting."
- Documented `routing.force_type` as the opt-in override that lets detection
  still run (and log) while routing uses the pin.

### OD-03 — Strengthen Delegation Prime Directive (SKILL.md)

- Expanded Core Principle 1 to name the directive explicitly and list five
  anti-patterns (simple writes, compound multi-role prompts, collapsed
  adversarial loops, artifact content forwarding, inline drafting).
- Enumerated the orchestrator's only permitted write paths (`state.md`,
  `state.tmp.md`, `config.yml`, `memory/**`, `stage-summary.md`).

### OD-04 — "One Role = One Sub-Agent" rule (SKILL.md)

- Added a prominent rule block immediately above "Two-Channel Communication"
  enforcing one Agent tool call per role, with worked examples (review board
  = 3 calls; DoD = 4 calls; debate = PRO+CON+JUDGE; adversarial loop = N
  fresh calls) and a list of violations.

### OD-05 — Tighten Step 4.5 (SKILL.md)

- Added a "Rejected justifications" sub-section that explicitly rejects
  "but it's simple", "I already know the answer", "faster if I do it",
  "no sub-agent exists", etc. Escalate to the user if no skill fits; do
  not self-write.

### OD-06 — Add "Common Orchestrator Anti-Patterns" section (SKILL.md)

- New top-level section inserted between Stage Definitions and Team DoD
  Protocol. Eight numbered anti-patterns drawn from real Prime Directive
  violations observed in the pipeline: simple self-writing, compound
  prompts, collapsed adversarial loops, pasting findings forward,
  light-as-skip, pinning project type, writing to satisfy a gate, fusing
  validator with producer.

### OD-07 — Update config table in SKILL.md

- Replaced the `project_type` row with rows for `routing.force_type` and
  `pipeline.enforce_self_write_block`. Describes the opt-in override
  semantics and the activation gate for the origin-detection soft-deny.

### OD-08 — Config schema v2.6 → v2.7 (references/config-schema.md)

- Bumped "Current Version" to 2.7.
- Removed `project_type` row from the schema table.
- Added `routing.force_type` (optional, default null) and
  `pipeline.enforce_self_write_block` (default true on fresh v2.7, false
  on tolerantly-parsed v2.6) rows.
- Updated the Config File Template (`config_version: "2.7"`, replaced
  `project_type: GREENFIELD` with `routing: force_type: null`, added
  `enforce_self_write_block: true` inside `pipeline:`).
- Added a new "Deprecated Keys" section above Version History explaining
  the warn-and-drop migration for `project_type` and the new
  `enforce_self_write_block` default.
- Added a v2.7 row to the Version History table referencing ADR-001/002/003.
- Regenerated `references/config-schema.json` from the markdown via
  `delivery-team/scripts/generate-schema.py` (dwarf-craft demands the
  derived artifact match its source).

### OD-09 — Setup wizard: drop Q1, renumber, update template and integration (references/setup-wizard.md)

- Removed Q1 (Project Type) entirely.
- Renumbered remaining questions: former Q2..Q9 → Q1..Q8. Announced the
  wizard now asks 8 questions (down from 9).
- Added a v2.7 migration note at the top of the Wizard Questions section
  describing the tolerant warn-and-drop behavior and the deprecation
  banner text emitted to both stage banner and `.delivery/state.md`.
- Updated two places that referenced "project type selected in Q1" to say
  "runtime-detected project type (Phase 1)".
- Updated the Config File Format example to `config_version: "2.7"` and
  replaced `project_type: GREENFIELD` with `routing: force_type: null`.
- Removed the `project_type` YAML field rule; replaced with
  `routing.force_type` (optional opt-in pin).
- Rewrote the "On Pipeline Start" Pipeline Integration section: Phase 1
  always runs, legacy `project_type` tolerantly dropped with warning,
  `routing.force_type` is the opt-in pin.

### OD-10 — `audit_agent_prompt.py` compound-role detector (optional/MAY, implemented)

- Added three regex-based compound-role detectors to the PreToolUse agent
  audit hook:
    1. Multiple `ROLE:` declarations in the same prompt.
    2. Phrases like "also act as", "then act as", "additionally play",
       "and also play".
    3. Two `You are ...` role declarations within 200 characters of each
       other (negation-aware via non-greedy matching).
- Warnings are non-blocking; they are appended to the existing ISOLATION
  AUDIT WARNING systemMessage, with a pointer to the "One Role = One
  Sub-Agent" rule.
- Stdlib only (`re`). Syntax checked.

### OD-11 — Reframe `references/project-types.md` for runtime detection

- Added a prominent block at the top stating that runtime detection is
  mandatory (v2.7+), that the config file does NOT pin the type (the
  legacy `project_type` key was removed), and that `routing.force_type`
  is the only supported way to pin, deliberately namespaced under
  `routing.` so it is a discoverable intentional act. Referenced ADR-002.

### OD-12 — `references/team-patterns.md` dispatch rules + Isolated Adversarial Loop

- Added a "Dispatch rule:" one-liner at the top of every pattern
  (Evaluator-Optimizer, Adversarial Review, Multi-Perspective Review Board,
  Decision Ownership Routing, Debate, Consensus). Each one leads with the
  same sentence: dispatch each role as a SEPARATE Agent tool call, one
  role = one sub-agent invocation, never collapse roles into one compound
  prompt.
- Added a new "Pattern 2b: Isolated Adversarial Loop" section immediately
  after Pattern 2, containing:
    * Core Guarantee of fresh context every loop.
    * Issue class taxonomy
      (`coupling | security | data-integrity | naming | testability |
      performance | docs`; untagged → `misc` = new class).
    * Three convergence rules per ADR-003 (two-clean, no-new-classes,
      hard cap).
    * Full loop protocol pseudocode (fresh sub-agent dispatch, class
      tracking across loops, architect revision with current-loop
      findings only, cap-reached as documented exit).
    * Invariants block restating context isolation, architect scoping,
      cap-reached semantics, and N=1-does-not-exit rule.
  Referenced ADR-003 for the full decision record.

### OD-13 — `references/quality-gates.md` + `references/pipeline-stages.md` + cross-cutting docs

- **quality-gates.md**:
    * Added "One validator = one Agent invocation" rule immediately after
      the existing DoD Validator Prompt Template block.
    * Added a new "Delegation Meta-Gate" section: before DoD can pass,
      the orchestrator must confirm every domain artifact in the stage
      was written by a dispatched sub-agent. Orchestrator writes to any
      non-routing file under `.delivery/artifacts/**` automatically fail
      the meta-gate regardless of validator votes.
    * Added a "Known Hook Limitations" section mirroring the
      `enforce_pipeline_scope.py` docstring: Bash redirection bypass,
      Layer 2 metadata drift, missing env-var injection. Makes the gaps
      visible to validators so they apply the meta-gate manually.
- **pipeline-stages.md**:
    * Added a header note on `[PARALLEL]`/`[SEQUENTIAL]` annotations:
      "These annotations imply one Agent tool call per listed role.
      Never combine multiple roles into a single sub-agent."
    * Replaced Stage 4's single "Adversarial Review" step with the
      Isolated Adversarial Loop (fresh sub-agent per loop, taxonomy,
      ADR-003 convergence rules, loop artifact paths).
- **`delivery-team/hooks/enforce_pipeline_scope.py`** (extended per ADR-001):
    * Expanded the module docstring to document the layered origin
      detection strategy and the known gaps (Bash bypass, Layer 2 drift,
      missing env-var injection).
    * Added `ARTIFACT_ALLOWLIST`, `ARTIFACT_ALLOWLIST_DIRS`,
      `ARTIFACT_ROUTING_BASENAMES`, and `SUBAGENT_ENV_VARS` constants.
      Allowlist covers `.delivery/state.md`, `state.tmp.md`, `config.yml`,
      `memory/**`, `state-archive/**`, `defects/**`, `features/**`,
      `aliases/**`, plus `stage-summary.md`/`state.md`/`state.tmp.md`
      inside `.delivery/artifacts/**`.
    * Added `_is_artifact_path`, `_is_allowlisted`,
      `_detect_subagent_origin`, `_activation_gated` helpers.
      `_detect_subagent_origin` implements Layer 1 (env var:
      `CLAUDE_AGENT_ID` or `DELIVERY_FLOW_AGENT_CONTEXT`) and Layer 2
      (hook-input metadata: `parent_tool_use_id`, `context.parent_tool_use_id`,
      `frame.is_subagent`). Conservative on unknown shapes — falls through
      to Layer 3 rather than hard-denying.
    * `_activation_gated` parses `config_version` as a tuple and requires
      `>= (2, 7)` AND `pipeline.enforce_self_write_block: true`. False
      for tolerantly-parsed v2.6 configs.
    * `main()` now computes `rel_path` early and, if activation is
      gated AND the path is an artifact AND not allowlisted AND no
      sub-agent origin signal, emits a loud systemMessage naming the
      Delegation Prime Directive, then `sys.exit(0)` (soft-deny, never
      blocks). Preserves the existing `try/except → sys.exit(0)` outer
      wrapper. Bash redirection is documented as a known gap, not fixed
      in this bundle (requires hooks.json changes + Bash-tool matcher).
    * Stdlib only. Syntax checked.
- **CLAUDE.md** (project root):
    * Updated the Delivery-flow pipeline architecture bullets: schema
      v2.7, project type detected per run, setup wizard 8 questions
      (down from 10).
    * Updated the "Config schema" convention line: v2.7 current, noted
      `project_type` removal and `routing.force_type` opt-in replacement.
- **README.md**: updated the "Setup wizard" bullet to note 8 questions
  and runtime detection.
- **delivery-team/README.md**: updated the "Setup wizard" bullet to note
  schema v2.7, 8 questions, runtime detection, `routing.force_type`.
- **.claude-plugin/marketplace.json**: bumped version `2.17.1` → `2.18.0`
  to reflect the schema v2.7 bundle.

---

## Derived artifacts

- Regenerated `delivery-team/skills/delivery-flow/references/config-schema.json`
  via `python3 delivery-team/scripts/generate-schema.py`. The script parsed
  87 schema rows and wrote the updated JSON.

## Dogfooding notes

- Syntax-checked both modified hook files with `ast.parse`.
- Schema generator ran cleanly and parsed the new/removed rows as expected.
- All edits are additive or targeted — preserved all existing content that
  was not explicitly in-scope for OD-01..OD-13.

## Known follow-ups (not in scope this bundle)

- Bash redirection bypass in `enforce_pipeline_scope.py` — closing it
  requires adding the `Bash` matcher to `hooks.json` AND implementing a
  command-string regex detector. Tracked in the hook docstring and in
  `quality-gates.md` "Known Hook Limitations".
- Centralized sub-agent dispatch wrapper — a single injection site for
  `CLAUDE_AGENT_ID` / `DELIVERY_FLOW_AGENT_CONTEXT` is the architectural
  mitigation for the "missing env var" Layer 1 collapse risk. Not
  implemented here because it is an orchestrator-runtime change, not
  a docs/hook change.

---

*"Seventeen commits! I have made seventeen commits today. The seams are
straight, and the code will hold."* — Gimli

---

## Round 2 Self-Correction (Gimli, son of Glóin)

Seventeen commits! I have made seventeen commits today. How many has the QA engineer found fault with? ... Do not answer that.

### D-01 (P0) — setup-wizard.md renumbering completed
- Line 21: "9 questions" -> "8 questions".
- `### Q10: User Feedback Personas` -> `### Q9: User Feedback Personas`.
- `### Q12: Enforcement Settings` -> `### Q10: Enforcement Settings`.
- Cross-references swept: "After Q12" -> "After Q10"; "(Q12)" hook-validation footnote -> "(Q10)".
- Stale Q5 risk-tolerance back-references in renumbered Q7 (Collaboration Patterns) and Q10 (Enforcement) repointed to Q4 — risk tolerance lives at Q4 now.
- Final grep confirms Q1..Q10 contiguous, no Q9/Q11/Q12 gap. "Hook 8" reference on the validation table is the hooks list, not a wizard question — left untouched (M-03 closed).

### M-01 (minor) — config-schema.md persona default cleaned
- Line 64: `auto (from project_type)` -> `auto (from runtime-detected type)`. The deprecated vocabulary no longer leaks into a live row.

### M-04 (unverified -> fixed) — docs/** parity sweep
Grep of `docs/**` for `project_type` and `2.6` found three stale files. All updated:
- `docs/user-guide/config.md`: schema version banner 2.6 -> 2.7; v2.7 migration note added; `project_type` row replaced with `routing.force_type` row; example YAML `project_type: GREENFIELD` -> `routing.force_type: null` block; `config_version` example bumped to "2.7".
- `docs/skills/delivery-flow.md`: `project_type` row in the key-settings table replaced with `routing.force_type` (Phase 1 always-detect note).
- `docs/contributing/index.md`: schema source-of-truth pointer bumped from v2.6 to v2.7.
Re-grep is clean for the active references. (Note: ADR / migration history references that intentionally cite "v2.6" or the deprecated `project_type` key are historical and must remain.)

### M-05 (unverified -> fixed) — audit_agent_prompt.py negation handling
The original `_ALSO_ACT_AS_RE` and `_YOU_ARE_MULTI_RE` would fire on prompts like "do not act as both a developer and a reviewer" — the kind of anti-pattern guidance text the orchestrator should be ALLOWED to send. Added:
- `_NEGATION_RE`: matches `do not | don't | never | must not | should not | shouldn't | cannot | can't | not allowed to` within a 60-char window before the trigger phrase.
- `_is_negated(prompt, start)`: helper that checks the preceding window.
- Both detector branches now skip the warning when the trigger is in a negated context. The "multiple ROLE: declarations" detector is structural, not phrasal, so it remains unguarded — repeated `ROLE:` headers are always a real compound dispatch.

Stdlib only. No new imports. Non-blocking warning behavior preserved.

### Files touched in Round 2
- `delivery-team/skills/delivery-flow/references/setup-wizard.md`
- `delivery-team/skills/delivery-flow/references/config-schema.md`
- `delivery-team/hooks/audit_agent_prompt.py`
- `docs/user-guide/config.md`
- `docs/skills/delivery-flow.md`
- `docs/contributing/index.md`

No regressions to OD-02..OD-13. Round 2 hands back to QA.

---

## Round 3 Fix Notes (Gimli)

Counted before I cut this time. `grep '^### Q'` on setup-wizard.md returned **ten** headers — Q1..Q10. Target per OD-01 AC#3 is nine contiguous Q1..Q9. The original v2.6 wizard had ten (Project Type + nine domain), removing Q1 yields nine. Round 1 sweep stopped one tier short and Round 2 propagated the wrong "8 questions" word.

**D2-01 fix**: Demoted `Q8: Existing .delivery/ State` to a "Pre-Question" meta block (it is conditional — only shown when `.delivery/` exists — so it does not occupy a numbered slot). Renumbered Q9 → Q8 (User Feedback Personas) and Q10 → Q9 (Enforcement Settings). Final count: 9 contiguous questions Q1..Q9, verified by re-grep.

**D2-02 fix**: Replaced `8 questions` / `8-question` / `down from 9` with `9 questions` / `9-question` / `down from 10` in:
- `delivery-team/skills/delivery-flow/references/setup-wizard.md` (line 21 Phase summary, line 50 wizard intro, migration note former-Q range corrected to `Q2..Q10 are now Q1..Q9`)
- `CLAUDE.md` line 98
- `README.md` line 62
- `delivery-team/README.md` line 51
- Internal cross-refs `Q10` → `Q9` in stale-hook migration step and Hook 8 note

SKILL.md Phase 0 carries no question-count text (verified by grep) so no edit needed there.

Axe down. Nine markers on the trail, numbered rightly. Ride.

## Gimli — SKILL.md wizard count fix
Line 1051: "10 wizard questions" -> "9 wizard questions". Grep confirms no other stale refs in SKILL.md. One swing, one fix.
