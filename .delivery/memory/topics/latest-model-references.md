# Latest-Model References — Binding Decisions
# BACKLOG-108 | Initiative Memory File
# Authored: 2026-05-28 (retargeted to Opus 5: 2026-09-19; reframed to latest-version references: 2026-09-20) | PO: Gandalf (Michael Connelly)
# Status: AUTHORITATIVE — every future pipeline stage reads this as binding context
# File renamed from opus-5-migration.md on 2026-09-20 (Revision 3). Sections 1-6 below are the historical rulings;
# Section 0 records what Revision 3 superseded. Where they conflict, Section 0 wins.

---

## Section 0: Revision 3 — latest-version references (user decision 2026-09-20, BINDING, supersedes pinning)

**BINDING-0.1 — Say "latest version of model X", never a version string.**
The repo stops hard-pinning model versions in prose, stamps and guards. It refers to the latest version of a family
("latest Opus", "latest Sonnet"). Opus 5 is the effective current model on 2026-09-20; it appears only in dated citations
and in observed baselines. BACKLOG-108 is reframed: remove version pinning, adopt latest-version references, migrate today's
stale 4.7 pins to that scheme.

**BINDING-0.2 — Scheme (PRD Revision 3, section 3 Convention).**
- Prose names families only. Stamps: `model_awareness: latest`, `pattern_library_version: rev-1`, `last_audited: <date>`.
  The 9 unstamped SKILL.md stay unstamped.
- Tier labels in code use the Claude Code CLI aliases `opus`, `sonnet`, `haiku`, defined ONCE in `MODEL_TIER_ALIAS`
  (`agentic-flow-builder/scripts/agent_registry.py`). Verified: https://code.claude.com/docs/en/model-config and local `claude --help`.
- The Claude API has NO evergreen alias for current models (every ID is a pinned snapshot; https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions).
  Code that must call the API reads ONE config value. No repo code calls the API today.
- Tests and doc examples use synthetic IDs with no digit and no `-latest` suffix (for example `claude-opus-fixture`).
- Baselines record the concrete model observed (`model_requested`, `model_resolved`, `model_pin_env`); a regression run WARNs on `model moved`.

**BINDING-0.3 — Guard forbids pins (amended by Revision 4, 2026-09-20).** The patterns `PIN_RE`, `STAMP_RE`, `PROSE_RE`, `BARE_RE`
live in ONE place, `scripts/check_model_pins.py` (no ID allowlist; the workflow only calls the script). PIN_RE is family-agnostic
and case-insensitive. No comment, blockquote, heading or code-fence exemption. Allowlisted locations: `CHANGELOG.md`, `.delivery/**`,
and a line carrying the marker `model-pin-ok` (forbidden at ship). Scope: tracked py, md, yml, yaml, txt, sh; `.json` excluded
(baselines record observed IDs). The workflow triggers on push to main, pull_request and workflow_dispatch; because ship is a
direct push, the blocking gate is the LOCAL run of the same script before the push (PRD FR-1.5, FR-7.3).

**BINDING-0.4 — Observed model, never `unknown` (Revision 4).** Baselines record `model_resolved[0]` = the `system/init` model
(observed top-level `model` on CLI 2.1.278). An `unknown` or empty model fails the capture. The smoke parser must read the real
stream shape (`message.model`, `message.usage`, result `total_cost_usd`); the hand-written fixture shape was wrong.
Caveats: serving infrastructure can change behaviour under a fixed ID; `claude -p` without `--bare` loads host context.

**Superseded rulings**
| Ruling | Status |
|--------|--------|
| BINDING-1.1, 1.2 (canonical heavy ID, positive allowlist of three IDs) | SUPERSEDED by 0.1 to 0.3: no ID is canonical in the tree; the lineup table is history |
| BINDING-1.3 (4-7 / 4-8 retired, one provenance comment) | SUBSUMED: any versioned ID is rejected; the `#` provenance comments in `agent_registry.py` are NOT exempt under Revision 4 and are reworded (provenance moves to CHANGELOG) |
| BINDING-1.4 (prd-quality-gate-flow aliases exempt) | UNCHANGED |
| BINDING-2.1 (positive-allowlist guard, no dual-allow) | REPLACED by 0.3; "no dual-allow window / squash so the guard never sees a partial state" still holds |
| BINDING-2.2 (full prose review, no `-frontmatter-only`) | RETAINED (PRD OQ-9 asks Michael whether to narrow); `-frontmatter-only` stamps are removed entirely |
| BINDING-2.3 (stamps after prose DoD) | RETAINED with new stamp values |
| BINDING-2.4 (registry `claude-opus-5` + provenance comment) | REPLACED by `MODEL_TIER_ALIAS` central dict |
| BINDING-2.5, 3.x, 4.1 to 4.6, 5.x | RETAINED. 4.3 `--effort xhigh` stays a project choice; runner also gains `--model opus`. 4.4 baseline re-capture stays, now records observed model. 5.5 ADR name may be made version-free by the Architect |
| Section 6 OPEN-2 (Sonnet tier) | MOOT: `sonnet` alias tracks latest; restated in PRD as the haiku-alias question (OQ-6) |
| Section 6 OPEN-3 (CLI accepts `--model claude-opus-5`) | RESOLVED: CLI accepts alias `--model opus` (verified, `claude --help`, CLI 2.1.278) |

Citations in Sections 3 and 6 are dated 2026-09-19 and describe Opus 5, the latest at that time; they inform S2 prose but are
not shipped with a version number.

---

## Section 1: Model IDs (historical; superseded by Section 0)

**BINDING-1.1 — Canonical model ID for heavy tier**
`claude-opus-5` is the canonical model ID for heavy-tier dispatch.
No variant spellings. No abbreviation `opus-5` without the `claude-` prefix in prose strings.

**BINDING-1.2 — Full approved lineup (positive allowlist)**
| Tier | Canonical ID | Status |
|------|-------------|--------|
| Heavy | `claude-opus-5` | ACTIVE |
| Mid | `claude-sonnet-4-6` | ACTIVE |
| Light | `claude-haiku-4-5-20251001` | ACTIVE |
| Heavy (prior) | `claude-opus-4-7` | RETIRED — flagged as stale |
| Heavy (prior) | `claude-opus-4-8` | RETIRED for this repo (docs list it as a legacy model still available) — flagged as stale |

Retarget note (2026-09-19): user decision moved the target from 4.8 to Opus 5. Mid tier stays
`claude-sonnet-4-6` and light tier `claude-haiku-4-5-20251001` per the original ruling; docs list
`claude-sonnet-5` as the current Sonnet and `claude-sonnet-4-6` as a legacy-available model
(see Section 6, OPEN-2). No change to mid/light tiers is made by this retarget.

**BINDING-1.3 — `claude-opus-4-7` and `claude-opus-4-8` are retired**
`claude-opus-4-7` MUST NOT appear in any non-comment string in the codebase after this initiative ships.
`claude-opus-4-8` MUST NOT appear either (0 occurrences today; guard rejects it going forward).
Sole exception: provenance comment in `agent_registry.py` (see BINDING-2.4), carrying `claude-opus-4-7` only.

**BINDING-1.4 — prd-quality-gate-flow routing aliases are exempt**
`"claude-sonnet"` and `"claude-haiku"` family alias strings in `prd-quality-gate-flow/` are
version-agnostic routing labels (not model ID literals). Leave as-is. They are NOT stale.

---

## Section 2: Scope Decisions

**BINDING-2.1 — CI guard: positive-allowlist pattern, no dual-allow window**
File: `.github/workflows/stale-model-id-guard.yml`
Strategy: positive allowlist — only `claude-opus-5`, `claude-sonnet-4-6`,
`claude-haiku-4-5-20251001` are approved. `claude-opus-4-7` triggers a CI failure.
Ship pattern: squash-rebase + ff-merge in ONE atomic commit so the guard never fires
on a partial mid-merge state. NO dual-allow transition window. NO PR — direct push
to origin/main post-squash. (Rationale: allowlist-over-deny CI guard pattern,
validated in Hot Lesson 3 and gate-patterns.md ADR-002.)

**BINDING-2.2 — Full prose review for ALL SKILL.md files**
ALL ~25 SKILL.md files receive a full prose review — not a stamp-only pass.
The `-frontmatter-only` qualifier is RETIRED for this initiative. There is no two-tier
stamp (`opus-5` vs `opus-5-frontmatter-only`). Every file ships reviewed.
(Rationale: honest readiness markers beat uniform markers — but this initiative's
scope explicitly funds the full review. The two-tier stamp was the right call for
the prior wave's budget constraint; that constraint does not apply here.)

**BINDING-2.3 — Stamps applied uniformly after full prose review**
Every SKILL.md receives these frontmatter stamps after prose review passes:
```yaml
model_awareness: opus-5
pattern_library_version: 5-0-1
last_audited: 2026-09-19
```
Stamps are applied AFTER prose edits are DoD-complete, not before.

**BINDING-2.4 — agent_registry.py heavy-tier update**
File: `agentic-flow-builder/scripts/agent_registry.py:190` (verified 2026-09-19; the original "delivery-team/scripts" path was inexact)
Change: `claude-opus-4-7` → `claude-opus-5` in the heavy-tier model assignment.
Add the provenance comment on the line IMMEDIATELY ABOVE the changed line (Revision 2 clarification: a
comment-only line is already exempt from the guard because it starts with `#`; a trailing same-line
comment would still be flagged by the guard's line-prefix exemption, see PRD D2-1):
```python
# prior: claude-opus-4-7 (retired 2026-09-19, BACKLOG-108)
```
This is the only permitted non-stale-flagged reference to `claude-opus-4-7`.

**BINDING-2.5 — Keystone edit order**
Edit keystones first, then cascade:
1. `delivery-team/skills/delivery-flow/SKILL.md` (sub-agent dispatch keystone — DISP-01 section)
2. `prompt-engineer/SKILL.md` (prompt-pattern keystone)
3. `delivery-team/skills/product-delivery/SKILL.md` (PO/SM/Analyst keystone)
4. All remaining ~22 SKILL.md files (parallel dispatch by file-scope group)
Cache-prefix re-fingerprint runs AFTER all SKILL.md edits are final (see BINDING-6.1).

---

## Section 3: Behavioral-Claims Protocol

**BINDING-3.1 — Doc-verify before prose commit**
ANY behavioral claim about `claude-opus-5` (e.g., context window, thinking mode,
tool-use patterns, dispatch behavior, speed characteristics) MUST be verified via
WebFetch against official Anthropic documentation before being written into any SKILL.md.
No provisional text. No "verbatim from training data" claims. No placeholders left in
shipped files.
Source (live URLs fetched 2026-09-19):
  https://platform.claude.com/docs/en/about-claude/models/overview (primary)
  https://platform.claude.com/docs/en/models/opus-5/migration-guide
  https://platform.claude.com/docs/en/build-with-claude/effort
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5

**BINDING-3.2 — Adversarial reviewer independently re-fetches load-bearing claims**
For any claim about Opus 5 that is load-bearing (informs dispatch strategy, budget
allocation, or capability guidance), the adversarial reviewer dispatches a FRESH Agent
call that independently re-fetches the Anthropic source URL and cross-checks the claim.
Minimum: 3 load-bearing claims verified independently. This is not optional.
(Rationale: PRD citation discipline is load-bearing for migration PRDs — Hot Lesson 2,
validated across 11 runs.)

**BINDING-3.3 — No provisional behavioral text ships**
If a behavioral claim cannot be doc-verified at time of authoring, the prose MUST either:
(a) omit the claim entirely, or
(b) frame it with explicit hedging: "Pending doc verification — do not treat as binding."
No hedged claim may remain in a file that passes DoD review.

---

## Section 4: Smoke-Test Decisions

**BINDING-4.1 — Confirmed-observable metrics (track always)**
These metrics are confirmed observable from the smoke-test runner output and MUST be
tracked in every run:
- `tokens.cache_hit_ratio` — cache efficiency signal
- `model_usage.<model>.dispatches` — per-model dispatch count (all three canonical IDs)

**BINDING-4.2 — Aggressive/best-effort metrics (tolerate nulls)**
These metrics are tracked in best-effort mode. Runner MUST warn (not fail) when absent:
- `thinking_tokens` — may not surface in all response shapes. Opus 5 change: adaptive thinking is ON by
  default and `thinking.display` defaults to `"omitted"` (thinking blocks arrive with an empty `thinking`
  field), so the token count may still be absent from stream output; keep best-effort (VERIFIED, Section 6)
- `stop_details` refusal codes — present only when model signals refusal
- Speed / `fast` indicators — model-version-dependent; tolerate null

**BINDING-4.3 — Runner invocation adds `--effort xhigh`**
Smoke-test runner invocation for this initiative adds `--effort xhigh` to the call.
This applies to both baseline capture and regression comparison runs.
Re-verified for Opus 5 (2026-09-19), CORRECTED RATIONALE: `xhigh` is a valid effort level on
`claude-opus-5` (effort doc, `xhigh` row lists Claude Opus 5). BUT the Opus 5 section of the effort doc
says "Start with `high`, the default ... step up to `xhigh` for demanding coding and agentic work" and
"run a fresh effort sweep on your evals rather than reusing" carried-over settings. The 4.8-era claim
"xhigh is the recommended starting point for coding/agentic" is TRUE ONLY for Opus 4.7/4.8 and is NOT
carried to Opus 5. Ruling stands as a project choice (xhigh for the smoke run, since the smoke scenario
is a long agentic pipeline), not as a doc-recommended default. The `claude` CLI documents `--effort`
with values low/medium/high/xhigh/max/ultracode ("Available levels depend on the model").
Side effects on Opus 5 (VERIFIED): thinking cannot be disabled at `xhigh`/`max` (400 error); set a large
`max_tokens` (start at 64k). OPEN-1 (Section 6): whether baseline should use `high` instead.

**BINDING-4.4 — Baseline invalidation and re-capture**
Step 1: Mark existing baseline with `sample_status: invalidated-model-migration` before
any edits to baseline.py or metrics.py.
Step 2: After all SKILL.md edits and agent_registry.py update are committed, run
`--init-baseline` live against `claude-opus-5` (5 samples).
Step 3: Commit baseline with these fields populated:
```yaml
last_captured_utc: <ISO-8601 timestamp>
last_captured_git_sha: <sha of HEAD at capture time>
n_samples: 5
model: claude-opus-5
```

**BINDING-4.5 — Producer-validator separation for smoke-test fixtures**
Meta-test fixtures (regression detectors, fault-injection fixtures, golden-output
assertions) that test `metrics.py` / `baseline.py` MUST be authored in a SEPARATE
Agent dispatch from the one editing the producer files.
Observable invariant: `git status` during validator dispatch shows producer files
unchanged.
(Rationale: producer-validator two-dispatch pattern — Hot Lesson 7, validated in tk5.)

**BINDING-4.6 — No CI smoke-test workflow**
No `.github/workflows/smoke-*.yml` file. CI runners do not have the `claude` CLI.
Smoke tests are local-only. This is a hard constraint, not a preference.

---

## Section 5: Delivery Decisions

**BINDING-5.1 — Ship pattern: squash-rebase + ff-merge + push origin/main**
No PR. One squash commit. Squash before merge so the CI guard never inspects a
partial mid-merge state where both `claude-opus-4-7` and `claude-opus-5` are
simultaneously present.
Sequence:
1. All edits complete and locally committed in working branches/stash.
2. `git rebase --autosquash` or interactive squash to single commit.
3. Fast-forward merge to main.
4. `git push origin main`.
Guard validates clean state on the single squash commit only.

**BINDING-5.2 — Local-only directive (all tooling)**
No workflow file that shells out to `claude` CLI goes into `.github/workflows/`.
This extends beyond smoke tests: any script, runner, or validator that invokes
the `claude` binary is local-only. CI is permitted for static guards (YAML lint,
model-ID allowlist grep, budget checks) only.

**BINDING-5.3 — Cache-prefix re-fingerprint after all SKILL.md edits**
After all SKILL.md edits are final and committed (but before the squash):
1. Re-run `sha256sum` on `governance/cache-prefix-hash.txt`.
2. Architect records in ADR-5-0-001 whether the fingerprint set expands beyond
   `delivery-team/SKILL.md` given that this wave includes full prose review of
   all ~25 SKILL.md files.
3. ADR-5-0-001 is binding; Developer MUST implement the fingerprint decision
   without re-debating scope.

**BINDING-5.4 — Self-referential dispatch invariant**
This pipeline's dispatch rule is model-independent (carried over unchanged). CORRECTED RATIONALE
(2026-09-19): the 4.8-era premise "the new model under-dispatches sub-agents" is NOT carried to Opus 5.
The Opus 5 docs say the opposite: "Claude Opus 5 delegates to subagents more readily than prior models"
(prompting-claude-opus-5#controlling-subagent-spawning; migration guide 4.8->5 recommended change 6).
The invariant now guards against BOTH fusing roles (quality) and uncontrolled over-dispatch (cost);
the dispatch count equal to the `dod_validators` list length is the deterministic cap. The following
invariant is non-negotiable:
- One Role = One Sub-Agent dispatch
- Dispatch count MUST equal `dod_validators.<stage>` list length
- Roles MUST NOT be fused in a single dispatch to save tokens
Violation: if two roles are dispatched together, the stage fails DoD regardless of
artifact quality. QA validator MUST enumerate role-dispatch correspondence explicitly.

**BINDING-5.5 — ADR-5-0-001 is the cache-prefix decision record**
The Architect owns ADR-5-0-001. It must answer:
- Does full-prose-review of all ~25 SKILL.md files expand the cache-prefix fingerprint
  set beyond the prior scope (delivery-flow/SKILL.md only)?
- What files are included in the updated set?
- What is the new `sha256sum` value?
This ADR must be committed with the same squash commit as the SKILL.md edits.

**BINDING-5.6 — No decisions re-debated during stage execution**
This file is loaded as binding context at every stage. Pipeline stages MUST NOT
re-debate any ruling in this file. If a stage-level validator flags a conflict with
a ruling here, the ruling here wins and the validator notes the ruling reference
(e.g., "BINDING-2.2 governs; no two-tier stamp permitted").

---

## Section 6: Opus 5 Re-verification Log (Revision 2 retarget, fetched 2026-09-19)

Model-independent rulings carried over UNCHANGED: local-only (BINDING-4.6, 5.2), producer-validator
separation (4.5), squash-rebase + ff-merge + push (2.1, 5.1), one role = one sub-agent (5.4 invariant),
no dual-allow window, full prose review (2.2), keystone order (2.5), no rulings re-debated (5.6).

Rulings that rested on a 4.8-specific behavioural claim, re-checked against live docs:

| Prior claim / ruling | Status for Opus 5 | Evidence (URL) |
|---|---|---|
| "4.8 dispatches fewer sub-agents than 4.7" (idea brief; PRD OQ-1) | CORRECTED, reversed: Opus 5 delegates MORE readily than prior models | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning |
| "4.8 follows instructions more literally" (PRD OQ-2) | REFRAMED: the docs document literalism as a 4.7 trait ("Claude Opus 4.7 interprets prompts more literally and explicitly than Claude Opus 4.6", More literal instruction following, 4.6-and-earlier section), and one Opus 5 note that a "be conservative" review prompt may be followed literally. No doc statement that Opus 5 is more literal than 4.8/4.7. Do not ship a general Opus 5 literalism claim | prompting-claude-opus-5 (Code review bullet); migration guide (4.6-and-earlier section) |
| `--effort xhigh` recommended start (BINDING-4.3) | CORRECTED: valid on Opus 5, but recommended start is `high` (default); xhigh for demanding coding/agentic work | https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5 |
| Effort levels recalibrated vs 4.7 (old PRD, 4.8 guide item 7) | RE-VERIFIED for Opus 5: "The token allocation behind each effort level changes on Claude Opus 5 compared to Claude Opus 4.7 ... Run a fresh effort sweep" (4.7 to 5 section, Effort levels recalibrated). 4.8 to 5 delta section states no recalibration, only "fresh effort sweep" | https://platform.claude.com/docs/en/models/opus-5/migration-guide (section: Migrating to Claude Opus 5 from Claude Opus 4.7) |
| Adaptive thinking off unless requested (old PRD) | REVERSED: on Opus 5 thinking is on by default (adaptive); `thinking.display` defaults to `omitted`; disabling thinking at xhigh/max returns 400 | migration guide "Migrating to Claude Opus 5 from Claude Opus 4.8", breaking changes 1 and 2 |
| Prompt-cache minimum 1,024 tokens (old PRD) | CORRECTED: 512 tokens on Opus 5 | migration guide, recommended change 3 |
| Model ID literal `claude-opus-5` | VERIFIED: "fixed model ID with no date suffix" | overview table; migration guide |
| 1M context, 128K max output | VERIFIED | https://platform.claude.com/docs/en/about-claude/models/overview |
| Reliable knowledge cutoff | CORRECTED: May 2026 (was Jan 2026) | overview table |
| Refusal `stop_details` public; mid-conversation system messages accepted | VERIFIED as documented features of Opus 5 | migration guide (4.7 section: "adds mid-conversation system messages and publicly documents refusal stop details") |
| Opus 4.8 status | Listed under "Legacy models (still available)" | overview |

Additional Opus 5 facts relevant to prose review (VERIFIED, same sources): Opus 5 verifies its own work
and "explicit verification instructions ... cause over-verification"; default responses and written
deliverables run longer; effort does not reliably shorten visible responses (prompt for length);
Priority Tier and web fetch tool not supported on Opus 5.

Open questions carried from this retarget:
- OPEN-1: use `high` (doc default) instead of `xhigh` for smoke baseline? Owner: Architect, Stage 4.
- OPEN-2: docs list `claude-sonnet-5` as current Sonnet; allowlist mid tier is `claude-sonnet-4-6` (legacy-available). Not changed by this retarget. Owner: user/Architect.
- OPEN-3: UNVERIFIED that the local `claude` CLI at the installed version accepts `--model claude-opus-5` (CLI docs page fetched shows `--effort` with xhigh but no `claude-opus-5` example). Verify by running the CLI at S5.
- OPEN-4: UNVERIFIED whether the Claude Code default effort on Opus 5 is `high` (API default is documented; the 4.8-era PRD row claimed Claude Code default too).

---

## Appendix A: Ruling Index

| ID | Topic | Section |
|----|-------|---------|
| BINDING-1.1 | Canonical heavy-tier model ID | §1 |
| BINDING-1.2 | Full approved lineup (positive allowlist) | §1 |
| BINDING-1.3 | claude-opus-4-7 retired | §1 |
| BINDING-1.4 | prd-quality-gate-flow aliases exempt | §1 |
| BINDING-2.1 | CI guard: positive-allowlist, no dual-allow window | §2 |
| BINDING-2.2 | Full prose review, -frontmatter-only qualifier retired | §2 |
| BINDING-2.3 | Stamps applied after prose review | §2 |
| BINDING-2.4 | agent_registry.py heavy-tier update + provenance comment | §2 |
| BINDING-2.5 | Keystone edit order | §2 |
| BINDING-3.1 | Doc-verify behavioral claims before commit | §3 |
| BINDING-3.2 | Adversarial reviewer re-fetches ≥3 load-bearing claims | §3 |
| BINDING-3.3 | No provisional behavioral text ships | §3 |
| BINDING-4.1 | Confirmed-observable metrics (always track) | §4 |
| BINDING-4.2 | Aggressive/best-effort metrics (tolerate nulls) | §4 |
| BINDING-4.3 | --effort xhigh added to runner invocation | §4 |
| BINDING-4.4 | Baseline invalidation and re-capture protocol | §4 |
| BINDING-4.5 | Producer-validator separation for fixtures | §4 |
| BINDING-4.6 | No CI smoke-test workflow | §4 |
| BINDING-5.1 | Ship pattern: squash-rebase + ff-merge + push origin/main | §5 |
| BINDING-5.2 | Local-only directive for all claude-CLI tooling | §5 |
| BINDING-5.3 | Cache-prefix re-fingerprint after all SKILL.md edits | §5 |
| BINDING-5.4 | Self-referential dispatch invariant (One Role = One Agent) | §5 |
| BINDING-5.5 | ADR-5-0-001 is the cache-prefix decision record | §5 |
| BINDING-5.6 | No rulings re-debated during stage execution | §5 |

---

## Appendix B: Precedent References

- Hot Lesson 2 (PRD citation discipline) — index.md
- Hot Lesson 3 (allowlist-over-deny CI guards) — index.md
- Hot Lesson 7 (producer-validator two-dispatch) — index.md
- topics/gate-patterns.md — ADR-002 provenance-comment exemption
- topics/project-types.md — FEATURE-execution-of-pre-planned-waves, binding-decisions-in-memory (validated:6)
- topics/claude-plugins-repo.md — keystone file order, zero SDK imports, model-ID as prose strings
- archive/run-2026-05-13-tk5.md — producer-validator two-dispatch, DEFERRED-gate honest-readiness-marker
- archive/run-2026-05-09-tk4.md — 5/5 binding rulings preserved across 5 waves; zero ruling-loss
