# QA Evaluator — Round 2 (Fresh Reviewer)

**Reviewer**: Legolas of the Woodland Realm
**Stage**: 06 — Development (Evaluator-Optimizer Round 2)
**Scope**: All 13 stories (OD-01 through OD-13). Fresh eyes. No memory of round 1.

> *"My eyes have not yet read this work. I judge only what I see in the leaves before me."*

---

## Verdict

**STATUS: NOT_DONE**

Two regressions remain in the setup-wizard renumbering work (OD-01) that have
also propagated into CLAUDE.md and README.md. They are mechanical and small,
but they directly violate an explicit OD-01 acceptance criterion and PRD FR-04,
so I cannot in good conscience pass this round.

Everything else I checked is in order. Round 2 is one targeted fix away from
DONE.

---

## Story-by-story regression check

### OD-01 — Remove `project_type` from config schema and wizard Q1 — **FAIL**

OD-01 AC #3 is unambiguous:

> *"`setup-wizard.md` removes the project-type question (today's Q1) and
> renumbers Q2 – Q10 as Q1 – Q9."*

PRD FR-04 echoes the same number:

> *"Running setup produces a 9-question wizard whose output config has no
> `project_type` field."*

Two defects against this AC:

#### D2-01 (P0) — `setup-wizard.md` still has 10 question headers, not 9

`grep -n '^### Q\d+:' delivery-team/skills/delivery-flow/references/setup-wizard.md`
returns:

```
67:  ### Q1: Tech Stack
88:  ### Q2: Team Size & Composition
109: ### Q3: Deployment Environment
131: ### Q4: Timeline & Risk Tolerance
152: ### Q5: Compliance & Regulatory
175: ### Q6: Human Checkpoints
201: ### Q7: Collaboration Patterns
228: ### Q8: Existing .delivery/ State
248: ### Q9: User Feedback Personas
273: ### Q10: Enforcement Settings
```

That is **ten** question headers (Q1..Q10), not nine. The renumber sweep done
in Round 1 D-01 stopped one tier too early — the headers `### Q9: User
Feedback Personas` and `### Q10: Enforcement Settings` still carry the old
v2.6 numbering that assumed a leading Q1 (Project Type) plus Q2..Q10 = 10
questions. After dropping the project-type question those two headers should
be `### Q8: User Feedback Personas` and `### Q9: Enforcement Settings`.

Note that this also collides with the existing `### Q8: Existing .delivery/
State` — there are now **two Q8s** if you count by intent. The fix is:

- `### Q9: User Feedback Personas` → renumber to `Q9` is wrong; the existing
  `Q8: Existing .delivery/ State` is the renumbered former Q9. Personas needs
  to slot in where the old Q10 lived. The clean target ordering is:

  | New # | Title                               |
  |-------|-------------------------------------|
  | Q1    | Tech Stack                          |
  | Q2    | Team Size & Composition             |
  | Q3    | Deployment Environment              |
  | Q4    | Timeline & Risk Tolerance           |
  | Q5    | Compliance & Regulatory             |
  | Q6    | Human Checkpoints                   |
  | Q7    | Collaboration Patterns              |
  | Q8    | Existing `.delivery/` State         |
  | Q9    | *(see note)*                        |

  The original v2.6 wizard had **ten** questions (Project Type + the nine
  domain questions you currently see at Q2..Q10). Removing Project Type
  yields nine. The current file has Q1..Q10 because the last two headers
  were never decremented.

  **Required fix**: choose one of two consistent layouts —
  - **(a) 9-question layout (matches OD-01 AC #3 and FR-04)**: drop `Existing
    .delivery/ State` to a sub-section under another question, OR fold one of
    the personas/enforcement headers into another. Most surgically: rename
    `### Q9: User Feedback Personas` → keep at Q9 (it is question nine), and
    rename `### Q10: Enforcement Settings` → fold into Q9 as a sub-section, or
    promote it and drop one of the earlier optional questions.
  - **(b) 10-question layout (consistent with current headers)**: explicitly
    revise OD-01 AC #3 and FR-04 to acknowledge that the wizard always had
    10 → 10-minus-1 → 9 was an undercount, and the true result is 10. This
    requires a planned scope change, not a code change.

  Either path requires sign-off from the PO. **Until then OD-01 is failing
  acceptance.**

#### D2-02 (P0) — Question count text says "8" everywhere, but should say "9"

Three live docs declare the wizard asks **8** questions, which is wrong under
either of the two layouts above (real number is either 9 per the plan, or 10
per the current header count — but never 8):

| File | Line | Current text |
|---|---|---|
| `delivery-team/skills/delivery-flow/references/setup-wizard.md` | 21 | `"Present & Ask: Show detected values, ask 8 questions with smart defaults"` |
| `delivery-team/skills/delivery-flow/references/setup-wizard.md` | 50 | `"The wizard asks 8 questions in order (down from 9 in v2.6 — Q1 Project Type was removed in v2.7 …)"` |
| `CLAUDE.md` | 98 | `"Setup wizard with 8 questions (auto-detect + smart options). The former Project Type question was removed in v2.7 …"` |
| `README.md` | 62 | `"Setup wizard: 8-question config wizard with auto-detection from codebase …"` |

The arithmetic is also wrong: the v2.6 wizard had **ten** questions
(Project Type + nine), not nine. So the migration note "down from 9" should
read "down from 10", and the result should be "9 questions" not "8".

This regression has propagated to CLAUDE.md and README.md in Round 1's
documentation parity sweep, so a Round 3 fix must update all four files in
lockstep, plus any docs/** mirrors of the same number (none found in my
sweep — see below).

---

### OD-02 — Phase 1 detection runs every invocation — **PASS**

`SKILL.md` Phase 1 prose was checked. The "One Role = One Sub-Agent" callout
is at line 317; the Common Orchestrator Anti-Patterns section is at line 720;
Frozen Type Routing is named as an anti-pattern; routing.force_type override
is described as "still detect, route on pin". No remaining `config.yml` →
`project_type` routing branch found in SKILL.md. Acceptance criteria 1–5 met.

### OD-03 — `routing.force_type` opt-in override key — **PASS**

`config-schema.md` line 16 documents `routing.force_type` with full enum,
default `null`, namespace rationale, and intentional-pin framing. SKILL.md
Phase 1 prose references it. Both-keys-present precedence (force_type wins,
bare project_type still emits deprecation log) is documented.

### OD-04 — Schema bump v2.6 → v2.7 — **PASS**

`config-schema.md` line 5 reads `## Current Version: 2.7`. Changelog and
Deprecated Keys sections present per Round 1 dev notes. `pipeline.enforce_self_write_block`
documented at line 17 with the dual-default behavior (true on fresh v2.7,
false on tolerantly-parsed v2.6). `max_self_correction` is documented and
referenced by Stage 4 adversarial loop cap (verified in pipeline-stages.md
line 376). One minor cosmetic note from Round 1 — line 64 `auto (from
runtime-detected type)` for `personas.categories` — was correctly cleaned in
Round 2 M-01.

### OD-05 — Strengthen SKILL.md delegation principle + anti-patterns — **PASS**

Delegation Prime Directive language present in SKILL.md and referenced from
multiple downstream sections. "Common Orchestrator Anti-Patterns" section
exists at line 720 and references the Isolated Adversarial Loop (line 738).
Six FR-08 anti-patterns are accounted for; Round 1 dev notes claim eight,
which is additive and acceptable.

### OD-06 — "One Role = One Sub-Agent" rule (callout) — **PASS**

SKILL.md line 317 hosts the rule block under the heading
`### One Role = One Sub-Agent (Prime Directive Corollary)`. The rule is also
referenced from `team-patterns.md` (every pattern leads with "Dispatch
rule:"), `quality-gates.md` ("One validator = one Agent invocation."), and
`pipeline-stages.md` (header note on `[PARALLEL]`/`[SEQUENTIAL]`). FR-10 and
FR-11 satisfied.

### OD-07 — Update SKILL.md config table — **PASS**

Round 1 dev notes describe the change; spot-checked that the config-schema
table no longer has a `project_type` row in the active section, and adds
`routing.force_type` and `pipeline.enforce_self_write_block`. Consistent with
OD-03 and OD-04 acceptance.

### OD-08 — `enforce_pipeline_scope.py` extension — **PASS** (with caveat)

`python3 -c "import ast; ast.parse(...)"` on
`delivery-team/hooks/enforce_pipeline_scope.py` returns clean — syntactically
valid Python. Round 1 dev notes describe the layered detection (env var →
metadata → soft-deny), the activation gate parsing `config_version` as a
tuple `>= (2, 7)` AND `pipeline.enforce_self_write_block: true`, the
allowlist constants, and the soft-deny outer wrapper. The Bash redirection
gap is documented as a known limitation in the hook docstring AND surfaced
in `quality-gates.md` "Known Hook Limitations" — matches FR-09 acceptance
clause (e). This is a documented exit, not a regression.

**Caveat**: I did not exercise the hook end-to-end with a synthetic active
pipeline + orchestrator-attributed write. That is integration test territory
and is out of scope for a markdown evaluator pass; flagged here for the UAT
stage.

### OD-09 — Setup wizard drop Q1 + renumber + integration — **FAIL** (see D2-01, D2-02)

The integration sections (Pipeline Integration, YAML field rules, config
example) are correct: `config_version: "2.7"`, `routing.force_type: null` in
the example, deprecation banner text spelled out, Phase 1 always-runs
language present. Only the question count and the Q9/Q10 headers are wrong.

### OD-10 — `audit_agent_prompt.py` compound-role detector — **PASS**

`ast.parse` is clean. Round 2 M-05 added `_NEGATION_RE` and `_is_negated`
guards, which is the right call — the structural "multiple `ROLE:` headers"
detector correctly remains unguarded since repeated role headers are
unambiguous compound dispatch. Stdlib only, non-blocking warning behavior
preserved per NFR-05. FR-12 (MAY) satisfied.

### OD-11 — Reframe `references/project-types.md` for runtime detection — **PASS**

Round 1 dev notes describe the prominent block at the top, `routing.force_type`
naming, ADR-002 reference, deliberate namespacing rationale. Consistent with
the OD-02 SKILL.md prose.

### OD-12 — `team-patterns.md` Dispatch rules + Isolated Adversarial Loop — **PASS**

Verified by grep:
- Every pattern (Evaluator-Optimizer, Adversarial, Multi-Perspective Review
  Board, Decision Routing, Debate, Consensus) leads with a "Dispatch rule:"
  line — six dispatch rules counted at lines 20, 101, 336, 422, 488, 687.
- Pattern 2b "Isolated Adversarial Loop" exists at line 206 with the Core
  Guarantee, the issue class taxonomy, the two-clean / no-new-classes / hard
  cap convergence rules (lines 286, 294), and the loop protocol pseudocode.

FR-13 fully satisfied. No regression vs Round 1 fixes.

### OD-13 — `quality-gates.md` + `pipeline-stages.md` + cross-cutting docs — **PASS**

- `quality-gates.md`: "One validator = one Agent invocation" rule at line 47;
  "Delegation Meta-Gate" section at line 55; "Known Hook Limitations" at line
  74. All FR-09 known-gaps surfaced where validators will see them.
- `pipeline-stages.md`: Stage 4 adversarial step replaced with the Isolated
  Adversarial Loop (line 363), references ADR-003 and team-patterns.md
  Pattern 2b. Loop cap bound to `pipeline.max_self_correction`.
- `CLAUDE.md`: Schema v2.7 reflected at lines 96, 125. Project type runtime
  detection wording at line 97. (But see D2-02 for the wrong "8 questions"
  count at line 98.)
- `README.md`: Schema bump and runtime detection at line 62. (But see D2-02
  for the wrong "8-question" count.)
- `marketplace.json`: version `"2.18.0"` (line 9) — bumped from 2.17.x per
  the dev's note. FR-16 marketplace.json clause (which OQ-6 flagged as
  potentially a no-op) has been treated as a real version bump rather than
  a no-op; that is a defensible interpretation.
- `docs/**` parity: Round 2 M-04 cleaned the three stale files. I re-grepped
  `docs/` for `project_type` and `2.6`. Only one residual hit:
  `docs/user-guide/config.md` line 5 — the v2.7 migration note that
  intentionally cites `project_type` in the deprecation prose. That is
  correct and must remain.

---

## Cross-cutting checks

### Hook Python validity (NFR-02, NFR-05)

`ast.parse` on both `enforce_pipeline_scope.py` and `audit_agent_prompt.py`
returns clean. Stdlib-only constraint preserved (the dev notes claim no new
imports beyond `re`, which is stdlib).

### Documentation parity (NFR-04, FR-16)

| Surface | Schema version | `project_type` removed from active prose |
|---|---|---|
| `config-schema.md` | 2.7 ✓ | yes (deprecated section only) ✓ |
| `setup-wizard.md` | 2.7 ✓ | yes ✓ |
| `CLAUDE.md` | 2.7 ✓ | yes ✓ |
| `README.md` | n/a | yes ✓ |
| `marketplace.json` | 2.18.0 ✓ | n/a |
| `docs/user-guide/config.md` | 2.7 ✓ | yes (only deprecation prose) ✓ |
| `docs/skills/delivery-flow.md` | n/a | yes ✓ |
| `docs/contributing/index.md` | 2.7 ✓ | yes ✓ |

Doc parity is otherwise complete. The only outstanding parity defect is the
question-count number propagated from `setup-wizard.md` into `CLAUDE.md` and
`README.md` — that is D2-02, not a separate issue.

### FR → file traceability spot-check

| FR | Implementing surface | Present? |
|---|---|---|
| FR-01 | `config-schema.md` deprecated section | yes |
| FR-02 | `config-schema.md` + setup-wizard.md tolerant-parse note | yes |
| FR-03 | `SKILL.md` Phase 1 prose | yes |
| FR-04 | `setup-wizard.md` removed Q1 | partial — count and Q9/Q10 headers wrong (D2-01, D2-02) |
| FR-05 | `references/project-types.md` reframed | yes |
| FR-06 | `SKILL.md` Delegation Prime Directive | yes |
| FR-07 | `SKILL.md` Step 4.5 rejection clause | yes (per dev OD-05 notes) |
| FR-08 | `SKILL.md` Common Orchestrator Anti-Patterns | yes (line 720) |
| FR-09 | `enforce_pipeline_scope.py` + `quality-gates.md` known limits | yes |
| FR-10 | `SKILL.md` line 317 callout | yes |
| FR-11 | team-patterns / quality-gates / pipeline-stages dispatch rules | yes |
| FR-12 | `audit_agent_prompt.py` compound-role detector | yes (with negation guard) |
| FR-13 | `team-patterns.md` Pattern 2b | yes |
| FR-14 | `pipeline-stages.md` Stage 4 reference | yes |
| FR-15 | `config-schema.md` `max_self_correction` doc | yes |
| FR-16 | cross-cutting parity | yes (modulo D2-02) |

Every FR is reflected in at least one file change. Only FR-04 has a partial
implementation that fails its own acceptance.

---

## Summary of required Round 3 fixes

Two defects, both P0, both confined to the setup-wizard renumber. One is
mechanical (decrement two headers); the other is a count word that needs to
be updated in four files in lockstep.

| ID | Severity | File(s) | Fix |
|---|---|---|---|
| D2-01 | P0 | `delivery-team/skills/delivery-flow/references/setup-wizard.md` | Resolve the Q9/Q10 header inconsistency. Either decrement them and reconcile against the existing Q8, OR confirm with PO that the v2.6 wizard had 10 questions and the result is "9 questions" with the current Q1..Q9 layout. Per OD-01 AC #3 ("renumbers Q2 – Q10 as Q1 – Q9") the target is **9 contiguous questions Q1..Q9**. |
| D2-02 | P0 | `setup-wizard.md` (lines 21, 50), `CLAUDE.md` (line 98), `README.md` (line 62) | Replace `"8 questions"` / `"8-question"` / `"down from 9"` with `"9 questions"` / `"9-question"` / `"down from 10"`. The original v2.6 wizard had ten questions (Project Type + nine domain questions); removing Q1 yields nine. |

Optional polish (not blocking):
- The dev's note in OD-13 mentions `delivery-team/README.md` was also updated;
  I did not re-verify that file. If it carries the same "8 questions" string,
  fold it into the D2-02 sweep.

---

## Closing

The bundle is ninety-five percent landed. The hooks are valid, the schema is
clean, the team-patterns and Isolated Adversarial Loop work is solid, the
docs/** parity sweep landed, and the Delegation Prime Directive has the
prominence it needs. The only thing standing between this bundle and an
honest DONE is a renumber the Round 1 sweep started but did not finish, and
a count word that propagated the wrong number into two upstream docs.

Fix D2-01 and D2-02 and I will sign in Round 3 without reservation.

> *"The work is honest, but the count is short. Lift your eyes — there are
> ten markers on the trail, not eight, and not nine. Number them rightly
> before we ride."*
>
> — Legolas
