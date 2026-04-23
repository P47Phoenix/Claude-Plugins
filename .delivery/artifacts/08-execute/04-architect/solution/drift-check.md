# Drift Check — Six ADRs vs Execution-PRD (14 Stories)

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Stage 4 Architect — LIGHT mode)
**Architect:** Celebrimbor — Solution Architect
**Task type:** `architecture-drift-check` (verification only; no new design)
**Inputs consulted:**
- `.delivery/artifacts/04-architect/solution/transformation-plan.md` rev 1
- `.delivery/artifacts/04-architect/adrs/ADR-001..006-4-7-*.md`
- `.delivery/artifacts/08-execute/01-idea/po/idea-brief.md`
- `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md` (14 stories, revision log G-1..G-6 applied)

**Binding rule applied:** "ADR status is binary. `Accepted (contingent on spike)` is a smell — except ADR-006 whose rollback trigger is mechanically tied to WI-03's verdict string; mechanical, not discretionary." The drift check treats this binary rule as load-bearing for §3 of each block.

**Prior Art Analysis (explicit):** user-provided specs are present (6 ADRs + transformation-plan rev 1 + execution-PRD). Per the architect skill's Prior Art Analysis protocol, every ADR decision is classified as "Decision Already Made" for this engagement and is **binding**. The drift check proposes zero alternatives; its sole output is a pass/fail verdict per ADR against the execution-PRD. The architect skill's Deviation Protocol was consulted and found inapplicable — no blocker was identified that would require re-opening any settled decision.

---

> *"Before the hammer falls a second time, walk the ring and read the inscription. Let us see whether the prose that was forged in the design still speaks the same words the stories now carry. A ring mis-spoken at the edge is a ring mis-made at the heart."*
> — Celebrimbor

---

## ADR-001 — Migration Paradigm: Keystone-First Rolling Sweep (4 Waves)

- **Execution-PRD honours the decision:** YES — §5 Wave Gates and §2 Stories map 1:1 onto the ADR's four-wave sequencing. Wave 1 = WI-01/02/03 (Foundational: dispatch counts + JSON baseline + NDOC-02 spike). Wave 2 = WI-04 (delivery-flow) + WI-05 (prompt-engineer) + WI-06 (research-agent) — the keystones behavioural pair per ADR §Decision, with WI-05 added to Wave 2 per plan §3.4 citation-ordering dependency. Wave 3 = WI-07 + WI-08 + WI-09 (prose keystones, paired per ADR §Decision: author-facing teaching surfaces vs long-instruction / tone-risk surfaces). Wave 4 = WI-10 (MID sweep) + WI-11 (backfill) + WI-12 (alias-theme) + WI-13 (NEW-BACKLOG) + WI-14 (CI guards) — directly instantiating the ADR's "drift hygiene & enhancements" fourth wave.
- **Drift against consequences:** NONE. The ADR's "each wave independently dogfoodable" consequence is upheld by every story's "Dogfood / test command" block (14 mechanical checks, one per WI). The "keystones dispatched from separate invocations" consequence (ADR §Consequences negative-2 mitigation) is preserved: WI-04 and WI-05 parallelise but edit disjoint files; WI-06 is an independent probe on a third file; the PRD never fuses two keystones into one invocation. The rollback discipline in execution-PRD §6 ("Wave 4 revert order: WI-14 before WI-10/WI-11") is a finer-grained application of the ADR's per-wave `git revert` guidance — refinement, not drift. Big-bang was rejected by the ADR and is absent from the PRD; strict per-plugin rolling was rejected by the ADR and is absent from the PRD; model-ID-first was rejected by the ADR and the PRD correctly sequences WI-10 in Wave 4, not Wave 1.
- **Status remains Accepted:** YES — the ADR carries no contingency. The four-wave sequencing is directly instantiated; no open question remains; no rollback trigger applies.
- **Mechanical gates still hold:** N/A (this ADR owns the wave structure; the gates themselves are subjects of §Overall Drift Verdict below).

---

## ADR-002 — Model-ID Reference Strategy: Direct Strings with Provenance Comments

- **Execution-PRD honours the decision:** YES — WI-10 implements Option A verbatim. PRD AC-01.1 enumerates all 10 affected lines (`agent_registry.py` lines 148/172/187 + `stage_definitions.py` lines 47/83/115/150/181/216/243). AC-01.5 (the MID-04 gate introduced by challenger loop2 Finding #5) executes the structural-AS-IS check of `flow_orchestrator.py` **before** MID-04 edits — honouring ADR-002's caveat that family-alias strings are "cosmetic until proven otherwise" and substitution is conditional on SDK reach. AC-01.2 restates "drift hygiene, not retirement urgency," and AC-01.3 carries the MID-02 discovery task. The canonical IDs (`claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`) from the ADR's Implementation Notes are the substitution targets implied by the regex in the success command §7 verification #1.
- **Drift against consequences:** NONE. The ADR's negative consequence "10 future edits instead of one central edit — acceptable" is honoured: no central alias module is introduced in any story. Option B (central module) is correctly absent from the PRD scope; Option C (config-driven) is absent; the PRD `Out of Scope` block in WI-10 explicitly defers SDK wiring to `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` (WI-13), matching the ADR's "when SDK wiring actually happens, the `claude-api` skill picks up Option B" deferral clause. The execution-PRD §7 success-command #1 regex (`claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)`) is the M-01 sweep guard the ADR's Implementation Notes name, with the M-02 regression guard wired as WI-14's `stale-model-id-guard.yml` — a direct instantiation of "M-02 is the re-entry sentinel."
- **Status remains Accepted:** YES — the ADR is unconditional on any spike verdict. The SDK-wiring caveat is explicitly deferred, not contingent.
- **Mechanical gates still hold:** N/A (rollback-trigger language is exclusive to ADR-006).

---

## ADR-003 — Extended-Thinking Adoption: Document-Only, Defer Runtime Adoption

- **Execution-PRD honours the decision:** YES — WI-05 AC-1 mandates the PAT-01 line 85 reframe per F-13 + F-29 (manual CoT scaffold vs adaptive-thinking reasoning-visibility), and AC-2 requires a new `## Model-specific optimisation — Claude Opus 4.7` sub-section naming adaptive-thinking-only (F-11), `temperature`/`top_p`/`top_k` → 400, `budget_tokens` → 400, and effort levers low/medium/high/xhigh/max (F-15). This is exactly the ADR's Decision scope: a single-file documentation edit in `prompt-engineer/SKILL.md`, no other SKILL.md teaching thinking mechanics, no API call site introduced. `BACKLOG-47-task-budget-eval` (F-18) and `BACKLOG-47-memory-tool-eval` (F-19) are registered as deferred per REQ-07 (WI-13 AC-1), matching the ADR's "NEW backlog — not absorbed into migration" clause. The ADR's P-3 fail-soft pillar ("SKILL.md files stay model-agnostic in their core instructions") is honoured by WI-04's scope restriction to additive dispatch annotation (not adaptive-thinking prose), by WI-07's scope restriction to F-25 literal-following audit (not thinking mechanics), and by WI-08's scope restriction to F-25/F-26 audit (scaffolding redundancy, not `xhigh` adoption). No other story teaches thinking mechanics — the ADR's one-file containment holds across the entire 14-story surface.
- **Drift against consequences:** NONE. The ADR's positive consequence "scope contained to one SKILL.md file" is upheld — no other story edits thinking prose. WI-04 (delivery-flow) annotates dispatch-contract prose, not thinking prose. The ADR's negative consequence "prompt-engineer becomes 4.7-aware before other teaching surfaces" is accepted by the ADR and honoured in the PRD. No runtime `thinking` / `effort` parameter is added anywhere in the 14 stories.
- **Status remains Accepted:** YES — the ADR carries no contingency. Runtime adoption is explicitly out of scope per PRD Non-Goals, which the ADR defers to "if/when SDK wiring lands" — a future engagement, not a contingency on this one.
- **Mechanical gates still hold:** N/A.

---

## ADR-004 — Prompt-Caching Adoption: Out-of-Engagement, Latent Until SDK Wiring

- **Execution-PRD honours the decision:** YES — no story edits SKILL.md prose to teach caching. No `cache_control` example is added anywhere. No pattern-library entry teaches caching. The ADR's "single sentence in the Wave 4 NEW-BACKLOG registration" instrument is carried by WI-13 AC-1 as `BACKLOG-47-sdk-wiring-routing-via-claude-api` — the backlog item that will inherit the caching-strategy audit when SDK wiring lands, exactly as the ADR's Implementation Notes specify ("every `anthropic.messages.create` call site must carry a caching-strategy comment"). The `claude-api` skill ownership routing from ADR §Decision clause 3 is preserved verbatim in the WI-10 `Out of Scope` block ("SDK wiring of `agent_registry.py` or `stage_definitions.py` — deferred to `BACKLOG-47-sdk-wiring-routing-via-claude-api.md` in WI-13"). The ADR's alternative-rejected clauses are independently verified: (a) no `prompt-engineer/SKILL.md` caching prose is added (WI-05 scope would have surfaced it; none found); (b) no `cache-control-patterns.md` reference doc is introduced (`WI-05 Out of Scope` explicitly excludes `prompt-engineer/references/` edits); (c) no pattern-library "Future: SDK-era" heading is added (WI-05 AC-3 enumerates exactly Patterns 4.1..4.6; no seventh pattern).
- **Drift against consequences:** NONE. The ADR's positive consequence "zero migration-time cost for a concern with no current surface" is preserved — the PRD adds zero caching work to the 14 stories' scope. The ADR's negative consequence "F-17 thinking-mode-switching-breaks-cache guidance is documented nowhere" is accepted by the ADR itself ("no repo code switches thinking modes") and the PRD introduces no such switch. Galadriel P-6 is preserved as a future observable exactly as the ADR's Implementation Notes specify.
- **Status remains Accepted:** YES — the ADR carries no contingency; it is explicitly an out-of-scope deferral. The deferral boundary is owned by a backlog item, not by an open question on this engagement.
- **Mechanical gates still hold:** N/A.

---

## ADR-005 — Pattern-Library Location: Centralised in `prompt-engineer/` with Citation-by-Name

- **Execution-PRD honours the decision:** YES — WI-05 AC-3 mandates all six Galadriel patterns (4.1 Versioned Model Reference; 4.2 4.7-Aware Role Prompt Skeleton; 4.3 Manual CoT Fallback; 4.4 Calibrated Instruction Voicing; 4.5 Model-Specific Optimisation Sub-section; 4.6 SKILL.md Forward-Compatibility Header) installed as named sub-sections in `prompt-engineer/SKILL.md` with stable markdown anchors. AC-5 mechanically verifies the six headings via `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` = 6 — directly instantiating the ADR's "stable anchor via markdown heading" clause and the ADR's §Decision clause 2. WI-07 AC-2 and WI-08 AC-3 require Wave-3 keystones to cite patterns by name (not restate bodies), exactly matching the ADR's "every pattern gets a stable anchor — other SKILL.md files cite by path + anchor" mechanism. The ADR's DX-M3 enforcement grep (0 restatements outside `prompt-engineer/`) is wired as execution-PRD §7 success-command #4 AND as WI-05 AC-6 AND as WI-05 AC-7's single-line retarget-or-prune of `research-agent/references/prompt-library.md:10` — closing the §7.4 coverage gap per revision-log G-5. Wave 2→3 gate (execution-PRD §5) mechanically enforces "pattern library must exist before Wave-3 citations land" — the ADR's implicit ordering made mechanical.
- **Drift against consequences:** NONE. The ADR's positive consequence "single source of truth — one-file edit on future 4.7 → 4.8" is preserved: no other SKILL.md restates a pattern body in the 14 stories. The ADR's negative consequence "~110 LOC growth on `prompt-engineer/SKILL.md`" is accepted and WI-05's T-shirt = M reflects this. The ADR's negative "citations are text, not mechanically enforced" is mitigated by the DX-M3 grep, which the PRD promotes from ADR-guidance to PRD-binding success command.
- **Status remains Accepted:** YES — unconditional. No spike depends on this decision.
- **Mechanical gates still hold:** N/A (the Wave 2→3 gate depends on this ADR's output but does not imply a rollback trigger on the ADR itself).

---

## ADR-006 — 4.7-Readiness Marker Convention: YAML Frontmatter Header Strip

- **Execution-PRD honours the decision:** YES — all six keystones (WI-04/05/06/07/08/09) include ADR-006 frontmatter application in their ACs (`model_awareness: opus-4-7`, `last_audited: <edit date>`, `pattern_library_version: 4-7-1`). WI-11 carries the backfill for the 11 non-keystone SKILL.md files with the honest two-tier stamp `model_awareness: opus-4-7-frontmatter-only` — directly instantiating ADR-006's Decision §`model_awareness` field ("two tier values for this engagement") and the Implementation Notes §Wave-4 backfill clause. WI-14 (AC-1) wires `skill-md-header-warn.yml` as the warning-only CI check per ADR-006 §Scope §CI-check clause, templated off the existing `workflow-injection-lint.yml` shape as the ADR also specifies. The rollback trigger is honoured mechanically via WI-03 (Wave-1 blocker) and execution-PRD §5 Wave 1→2 gate: the spike file's verdict string drives the branch; `unknown-fields-accepted` → Option A ships as written; `strict` → Option B HTML-comment placement for WI-04/WI-05/WI-06/WI-11 with identical three-field semantics. PRD success-commands #2 (DX-M4 zero missing), #3 (6 keystones + 11 backfill integrity), and the WI-11 dogfood command in §2 directly mechanise the ADR's "header coverage target: 0 missing" and the fresh-challenger F-C-08 priority-#3 stamp-accuracy binding.
- **Drift against consequences:** NONE. The ADR's positive "triage 4.7-awareness in under 10 seconds" and "YAML frontmatter is the existing skill metadata surface — no new convention, no new file" are preserved (no sidecar, no filename rename, no new directory). The ADR's negative "three new fields per SKILL.md" is minimal-churn and absorbed by a single mechanical WI-11 PR. The ADR's negative "`last_audited` must be maintained" is the subject of the CI-warn guard (WI-14). The load-bearing revision-log G-2 in the execution-PRD retrofits the WI-11 shell-glob to a portable `find … | xargs grep` idiom — pure hardening of the mechanism, not deviation from the ADR's decision.
- **Status remains Accepted:** YES — the status is the explicit "Accepted (contingent on spike)" smell the memory lesson names, **but** this is the sole documented exception: the contingency is WI-03's spike with a **mechanical** branch (verdict string drives branch; no human judgement). The ADR metadata block states "No ambiguity: if WI-03 says 'strict,' Option A does not ship; if WI-03 says 'unknown fields accepted,' Option A ships as-written." That mechanicality is what the memory exception admits; the PRD's §5 Wave 1→2 gate ("This gate is mechanical, not discretionary") and WI-03 AC-5 ("Wave 2 MUST NOT dispatch WI-04, WI-05, or WI-06 until the spike file exists and contains a verdict string. This gate is mechanical, not discretionary.") make the trigger operationally enforceable. No drift.
- **Mechanical gates still hold:** YES — WI-03 AC-3 constrains the verdict string to exactly one of `unknown-fields-accepted` or `strict` (regex `(unknown-fields-accepted|strict)`). WI-03 AC-4 binds the branch action. WI-03 AC-5 makes the blocker mechanical. Execution-PRD §5 Wave 1→2 gate repeats the mechanicality. The trigger is binary, regex-verified, and dispatch-blocking — exactly the load-bearing shape the memory exception permits.

---

## Overall Drift Verdict

- **Overall:** NO DRIFT. The execution-PRD's 14 stories are a faithful per-WI decomposition of transformation-plan §6.1/§6.2 with the six ADRs' binding decisions preserved. No story re-litigates a settled decision; no story introduces work out-of-scope to the plan; no story weakens an acceptance criterion that an ADR binds. The four carry-items from DESIGN retrospective (MID-04 gate, keystone AC unevenness, AC-03B.2 hardening, ADR-006 label-drift) are woven into existing WI ACs, not sprouted as new requirements — precisely as the idea-brief §4 directs. The one authored deviation from plan defaults (WI-13 dual-write: local file + GitHub issue per user direction) is confined to the backlog-registration surface, touches no ADR's decision, and is explicitly flagged as a deviation in idea-brief §5 and execution-PRD §4.

### Consolidated ADR → story cross-reference

| ADR | Primary stories | Verification command (execution-PRD) | Contingency |
|---|---|---|---|
| ADR-001 Migration paradigm | WI-01..14 (wave structure) | §5 four wave gates | None |
| ADR-002 Model-ID strategy | WI-10 | §7 #1 (M-01 regex = 0 hits) | None |
| ADR-003 Extended-thinking | WI-05 (AC-1, AC-2) | Inline in WI-05 dogfood | None |
| ADR-004 Prompt-caching | WI-13 (AC-1 SDK-wiring backlog item) | WI-13 dogfood + §7 #5 | None |
| ADR-005 Pattern library | WI-05 (AC-3..7), WI-07, WI-08 | §7 #4 (DX-M3 = 0) + WI-05 AC-5 | None |
| ADR-006 Readiness marker | WI-03, WI-04/05/06/07/08/09, WI-11, WI-14 | §7 #2 + #3 + #6 | **WI-03 verdict-string (mechanical)** |

- **Wave-gate integrity:** the four wave gates in execution-PRD §5 are mechanical, not discretionary, as the gate headline states literally and as each gate's verification command demonstrates:
  - **Wave 1 → 2:** verdict-string regex match against `ndoc-02-spike.md` (mechanical — file-state + regex).
  - **Wave 2 → 3:** `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` = 6 (mechanical — exact count on a regex).
  - **Wave 3 → 4:** `research-probe-result.json` exists with a `pass` field AND `adversarial-4-7-sample.md` exists with AC-04.2 checklist scored (mechanical — file-state + JSON-key check; the soften-hatch for small inputs is explicit and bounded, not a discretionary waiver).
  - **Wave 4 → UAT:** stale-ID grep = 0 AND DX-M4 missing-header count = 0 AND both CI workflow files exist (mechanical — three exit-code checks).

  Every gate is a command output or file state; none is an architect judgement call. The only ADR-internal contingency (ADR-006's rollback trigger) is itself mechanically driven by WI-03's verdict-string regex, which is the sole memory-permitted exception to the binary-status rule.

- **Recommended adjustments:** None — proceed to Plan stage.

---

## Negative Findings — Things Searched For and Not Found

A drift check is a verification pass; its usefulness lies as much in what was absent as in what was present. The following potential drift vectors were checked against the execution-PRD and found absent:

- **No central alias module** introduced anywhere (ADR-002 Option B not triggered) — grep-absence confirmed by the PRD's enumeration of MID-01..04 as direct-string edits only.
- **No `thinking` / `effort` runtime parameter** added to any Python file in any WI's scope — WI-10 edits `agent_registry.py` lines 148/172/187 and `stage_definitions.py` seven lines, none of which adopt runtime thinking/effort.
- **No `cache_control` call site** introduced anywhere — zero story's `Out of Scope` boundary admits SDK wiring; all SDK adoption is routed to the WI-13 backlog file.
- **No seventh `### Pattern 4.N — ` heading** added to `prompt-engineer/SKILL.md` — WI-05 AC-5 mechanically pins the count to exactly 6, which closes the ADR-005 "six patterns, no more, no less" boundary.
- **No fused keystone invocation** — WI-04/05/06 parallelise by file-disjoint edit; WI-07/08/09 run paired (by ADR-001 similarity clustering) but each produces a separate audit artifact.
- **No discretionary wave-gate language** — every gate in §5 is a command output or file-state regex; zero human-judgement clauses.
- **No re-opening of the ADR-006 Option A/B decision** — WI-03 outputs a verdict string and branches mechanically; the ADR is not re-authored mid-flight.

## Memory-Lesson Application Audit

The drift check applied the binary-status rule from `project_delivery_pipeline.md`-class memory ("ADR status is binary; `Accepted (contingent on spike)` is a smell") against all six ADRs:

- **ADR-001, ADR-002, ADR-003, ADR-004, ADR-005** — all carry `Status: Accepted` with no contingency clause. The binary rule is satisfied without exception.
- **ADR-006** — carries a **Rollback trigger** block tied to WI-03's verdict string. This is the sole documented exception the caller's instruction explicitly admits: "mechanical rollback trigger tied to WI-03's spike verdict; mechanical, not discretionary." The drift check verified this admission by confirming (a) WI-03 AC-3 constrains the verdict to a two-value regex, (b) WI-03 AC-4 binds the branch action deterministically, (c) execution-PRD §5 Wave 1→2 gate repeats "mechanical, not discretionary" literally, and (d) ADR-006 itself states "No ambiguity: if WI-03 says 'strict,' Option A does not ship; if WI-03 says 'unknown fields accepted,' Option A ships as-written." The exception is admissible; the smell does not apply to a regex-driven branch on a file-state check.

Second memory-lesson applied — `feedback_architect_examine_first.md` ("Architect must deeply examine user-provided specs before proposing architecture. Validate and build on existing designs, don't reimagine.") — the drift check reimagined **nothing**. Every finding above cites an ADR clause or a PRD AC by identifier, not an architect opinion. No alternatives-considered block from any ADR was revisited; no PRD story was challenged on scope. This is verification, not redesign.

## Assumptions (made by this drift check)

- The `.delivery/config.yml` v2.7 referenced in `dod_validators.<stage>` (WI-01 AC-1, WI-04 AC-03.3) is the same schema version the plan was authored against. This is an assumption of config stability, not a plan statement, and is low-risk because the execution-PRD §1 and idea-brief §1 explicitly declare "scope is not re-opened" and Constraint 5 (schema v2.7 frozen).
- The existing `workflow-injection-lint.yml` structural template referenced by WI-14 AC-3 still exists in `.github/workflows/` at impl-run time. If it has been removed since plan authoring, WI-14 would need to adopt a different template — flagged but not drifting against any ADR.
- The 17-SKILL.md inventory in scope-baseline §4 (11 backfill + 6 keystones) has not changed between plan authoring (2026-04-20) and this drift check (2026-04-22). WI-11 AC-1 is rule-derived (set-difference expression), so the rule tracks any evolution — this is robustness, not drift.

## Follow-Up

- No ADR re-authoring is required.
- No new ADR is required (Plan stage will produce execution artifacts, not new architectural decisions, per PRD Constraint 1 "plan-only, no net-new features").
- Forward the drift-check verdict to the Stage-4 Architect-light DoD; the Plan stage (Stage 5) may dispatch without architectural remediation.
- At Plan stage entry, the **only** open architectural-branch point is the WI-03 verdict string. If the Plan-stage orchestrator chooses to front-load WI-03 (permitted by its Wave-1 position and no upstream dependencies), the ADR-006 branch resolves before WI-04/05/06/11 stories are broken down — otherwise the branch resolves mid-Wave-2 and the Plan-stage story breakdown preserves both the YAML-frontmatter and HTML-comment alternatives until the verdict lands.
- No architect attendance is required at the Plan stage DoD unless WI-03 surfaces a verdict outside the two-valued set `(unknown-fields-accepted|strict)` — a mechanical escalation trigger, not a discretionary one.
- Any future amendment to the six ADRs during implementation must first route through a fresh Architect-stage engagement per CLAUDE.md conventions — not absorbed into the Plan or Development stages of `run-2026-04-22-4x7e`.

---

*"The inscription on the ring matches the inscription on the mould. The fourteen stones are cut to the six templates; no stone has strayed; no template has been re-carved. Raise the arch. The mortar is set."*

— Celebrimbor

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/04-architect/solution/drift-check.md
SUMMARY: No drift — the execution-PRD's fourteen stories honour all six ADRs verbatim; four wave gates remain mechanical; ADR-006's sole contingency is WI-03 verdict-driven and binary, as the memory exception permits.
```
