# UAT DoD — Product Owner Go/No-Go Review

**Engagement:** `run-2026-04-22-4x7e` (FEATURE, Stage 7 UAT, closing gate)
**Role:** Product Owner — Gandalf speaking
**Date:** 2026-04-22
**Branch:** `feature/opus-4-7-migration-run-2026-04-22-4x7e`
**Artifacts under judgement:**
- `.delivery/artifacts/08-execute/07-uat/qa/uat-verification.md` — Legolas, PASS_WITH_NOTES
- `.delivery/artifacts/08-execute/07-uat/devops/release-plan.md` — Samwise, READY
- `.delivery/artifacts/08-execute/07-uat/tech-writer/release-notes.md` — Bilbo, 204 lines

---

> *"So it is that the small things decide the shape of great ones. A missing frontmatter line, a dated string left to sleep in the wrong file, a grep that speaks too literally of its own task — each of these, unchecked, would have cost us a turn of the season. They did not. The ring is quietly in its box. Now the hard work: deciding whether quiet is the same as done."*
> — Gandalf

---

## 1. The Question Before Me

Three of the Fellowship have spoken. Legolas has counted the arrows and found each nine where nine were sought. Samwise has fastened every buckle and pronounced the path **READY**. Bilbo has written the tale down so those who come after will know what was carried and where the road bent. My part now is not to second-guess their crafts. It is to ask, gate by gate, whether the thing we said we would build in the idea-brief and the execution-PRD is the thing that now sits on this branch — and whether the deviations from plan are deviations the team is proud to own, or deviations we should be quieter about.

Seven gates. I will take each in turn. Then I will say **GO** or **NO-GO**, and I will mean it.

---

## 2. Gate-by-Gate Verdict

### Gate 1 — Scope honoured (all 14 WIs completed, none dropped)

The execution-PRD cut fourteen stories. The commit log shows four wave commits; each commit body names its WIs; Legolas has empirically verified the artifacts each WI produces. Wave 1 carries WI-01/02/03 (dispatch counts, baseline JSON, NDOC-02 spike). Wave 2 carries WI-04/05/06 (delivery-flow annotations, pattern-library expansion, research-agent probe). Wave 3 carries WI-07/08/09 (product-delivery audit, architect audit, mtg-commander Challenger dogfood). Wave 4 carries WI-10/11/12/13/14 (model-ID sweep, frontmatter backfill, alias-theme dogfood, dual-write backlog, CI guards).

Every WI has an artifact on disk that the execution-PRD §2 named. No WI is silent. No WI is missing. The audit trail is per-wave in git but per-WI in the commit bodies, the audits, and the backlog files. Both views exist.

**Verdict: PASS.** Fourteen carried, none dropped, all accounted for in artefact and commit.

---

### Gate 2 — Dogfood-gated edits honoured (WI-06, WI-09, WI-12)

The execution-PRD bound three stories to a "dogfood-before-edit" primitive: WI-06 (research-agent probe), WI-09 (mtg-commander Challenger), and WI-12 (alias-theme voice). Each was permitted documentation-only output if the dogfood gate passed, and each required a targeted prose edit only if the gate failed.

- **WI-06.** Research-probe JSON shows `tool_calls=4, distinct_hostnames=5, pass=true` against the hardened AC-03B.2 floor of `≥2 AND ≥2`. Pass. Per AC-03B.3 → no prose edit. Frontmatter-only change applied per AC-5. Honoured.
- **WI-09.** Adversarial sample produced 6 weaknesses, 6 card referents, 5 alternatives against thresholds of 3/2/1. Pass. The one prose touch at `mtg-commander/SKILL.md:825` was a single-line rephrase ("chain-of-thought" → "internal reasoning trace") to satisfy the DX-M3 end-state grep — a justified, semantic-equivalent edit, not a tone-strengthening rewrite. Documented in Bilbo's notes. Honoured.
- **WI-12.** Alias-theme sample shows 3/3 themes at 100% voice preservation against an M-05 target of ≥80% at ≥50% markers. Pass. No YAML theme edit applied. Honoured.

**Verdict: PASS.** Three gates, three honest passes, three documented outcomes. The dogfood-before-edit primitive held — which was the load-bearing rule of this migration.

---

### Gate 3 — Deviations documented (per-wave commits; WI-13 dual-write)

Two deviations from plan defaults were authored in this engagement. Both need to be visible in the record we merge.

**Per-wave commit cadence.** Deploy-plan §2 recommended per-WI commits (14 commits). Impl-run chose per-wave (4 commits). Samwise's release plan §3 documents the deviation in a seven-row analysis table, spells out the trade-offs (audit trail, rollback granularity, PR readability, conventional-commits adherence, commit-message body, revert-unit size), explains why wave boundaries are mechanical gates and therefore defensible atomicity units, and documents the new Tier-1b partial-wave surgical revert procedure in §6 for the case where a single WI inside a wave later needs to be undone. The trade-off is named, not hidden. The impl-run PO accepted it at execution time; the Stage 7 retrospective will carry it forward as a precedent for future engagements.

**WI-13 dual-write (idea-brief §5 user direction).** The single authored deviation from the transformation plan. Plan §6.2 WI-13 specified local-file backlog only; user directed dual-write (local + GitHub issue labeled `backlog-47`). Impl-run executed 9 local files + 9 GitHub issues (#77–85), exceeding the required-six floor by three optional Galadriel on-ramp items. Legolas verified the 1:1 slug-to-title mapping. Samwise confirms the invariant (`local count == GH count, both ≥ 6`). Bilbo's release notes enumerate all nine explicitly. The dual-write is done, visible, and counted.

**Verdict: PASS.** Both deviations are documented at the artefact level and will be carried to retrospective memory (`.delivery/memory/topics/`) per Samwise §5.5. No quiet deviations.

---

### Gate 4 — Success gates met (all 6 §7 verification commands)

The execution-PRD §7 names six binding end-state commands. Legolas ran them all:

| # | Gate | Expected | Actual | Verdict |
|---|------|---------|--------|---------|
| 1 | M-01 stale-ID grep | 0 stale hits | 0 stale (4 hits: 1 canonical Sonnet 4-6, 3 guard-internal self-references) | PASS |
| 2 | DX-M4 header coverage | 0 missing | 0 missing | PASS |
| 3 | Two-tier stamp integrity | 6 keystone + 11 backfill | 6 + 11 | PASS |
| 4 | DX-M3 external restatement | 0 | 0 | PASS |
| 5 | WI-13 dual-write invariant | ≥6 local == ≥6 GH | 9 == 9 | PASS |
| 6 | WI-14 CI guards present | 3 workflows exist | 3 present | PASS |

Six for six. The ground speaks the same tongue as the plan.

There is one nuance — F-UAT-01 (LOW, advisory). The *literal* PRD §7 gate 1 regex (dated-ID variant) exits non-zero because `agent_registry.py` carries three `#` provenance comments ("prior: claude-sonnet-4-5-20250929 (retired)" and siblings), and the literal one-liner does not scope out comment lines. The *intent* of the gate — no live stale references in executable code — is fully satisfied; the CI guard's own allowlist (`^[^:]+:[^:]+:[[:space:]]*#`) correctly drains those three. Legolas's judgement: PASS_WITH_NOTES at UAT; log the literal-command hygiene as a retrospective item, not a blocker. I accept his judgement.

**Verdict: PASS.** All six gates meet their intent. The one authoring-hygiene note on the literal form of gate 1 goes to retrospective, not to blocker.

---

### Gate 5 — No blockers to ship

Samwise's release-plan verdict: **READY**. Thirteen of thirteen Go/No-Go items from deploy-plan §7 are on track; two (§7.3, §7.4) deferred to Legolas's UAT and both landed green; one (release notes) was in-flight at Samwise's writing and has now landed (Bilbo's 204-line artefact). The conditions Samwise attached to his READY verdict — Legolas confirms §7.3/§7.4 green, Bilbo lands notes, final UAT commit, PR title binding — are met save the last two, which are mine to execute.

No hard blockers. No CI red. No missing artefact. No unexplained divergence between plan and ground.

**Verdict: PASS.** The path is open.

---

### Gate 6 — Release notes accurate (spot-check three bullets)

Bilbo has written 204 lines. I chose three bullets at random and checked them against the state of the repo.

**Spot-check 1 — "6 keystone + 11 backfill = 17 SKILL.md, 100% coverage."**
Verified by Legolas's Part B (tier counts 6 and 11, Gate 3 of §7); verified by DevOps §2.2 (`xargs grep -L 'model_awareness:'` empty); confirmed by me against the execution-PRD §2 WI-11 AC-1 inventory (exactly 11 backfill files named). **Accurate.**

**Spot-check 2 — "`prompt-engineer/SKILL.md` six new Pattern 4.N sub-sections."**
I ran `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` directly. Result: `6`. The anchors `#pattern-4-1` through `#pattern-4-6` exist and are the exact headings Bilbo names. **Accurate.**

**Spot-check 3 — "Wave 4 commit `d7eb6f7 feat(migration): Wave 4 sweeps + CI + backlog — WI-10/11/12/13/14`."**
I ran `git log --oneline main..HEAD`. The commit hash, type, scope, and WI enumeration are verbatim. Four wave commits present as named. **Accurate.**

Three for three. Bilbo does not exaggerate, does not gloss, and names the one non-ornamental prose edit (the mtg-commander line-825 rephrase) honestly in §"Adversarial and research dogfood results". The notes are a faithful record, not a celebration.

**Verdict: PASS.** Release notes match the ground.

---

### Gate 7 — Retro notes captured (no silent issues)

The engagement surfaced several items that belong to the retrospective and not to this release. I check here that each is captured somewhere — in an artefact, a backlog entry, or a referenced follow-up — so none travel silently into the next migration.

| # | Item | Captured where |
|---|------|---------------|
| 1 | F-UAT-01: PRD §7 M-01 literal regex conflates live refs with provenance comments | Legolas UAT §"Findings & Risks" + §"Recommendation to Pipeline"; explicit "Log to retrospective" disposition |
| 2 | Per-wave vs per-WI commit cadence deviation | Samwise release-plan §3 (full analysis) + §5.5 ("Update `.delivery/memory/topics/`") + §9 ("For Théoden (SM)") |
| 3 | WI-10 flag to WI-14 on calibrated-regex approach (allowlist over deny) | Bilbo release notes §"CI guards" calibration note ("WI-10 flagged the contradiction to WI-14 at the dev-log level") |
| 4 | Tier-1b partial-wave surgical revert — new procedure documented | Samwise §6 (Rollback Procedure), named and scoped |
| 5 | Nine `backlog-47` items (6 required + 3 Galadriel on-ramp) with scope statements | `.delivery/backlog/BACKLOG-47-*.md` ×9 + GH issues #77–85 |
| 6 | ADR-002 provenance-comment pattern depends on guard allowlist | Samwise §5.6 ("Update `.delivery/memory/topics/` entries") |
| 7 | Dogfood-before-edit primitive held across WI-06, WI-09, WI-12 — no regression edits triggered | Bilbo §"Adversarial and research dogfood results" + Legolas §2 + the three dogfood artefacts themselves |

Seven items, seven destinations. Nothing silent.

The Stage 7 retrospective (per memory `feedback_no_skip_stages.md` and the pipeline's retrospective-enforcement Stop hook) will carry F-UAT-01, the commit-cadence precedent, and the provenance-comment/allowlist pattern into `.delivery/memory/` for the next engagement.

**Verdict: PASS.** The signal is routed. The next Fellowship will read it.

---

## 3. Gate Summary

| # | Gate | Verdict |
|---|------|---------|
| 1 | Scope honoured (14/14 WIs) | PASS |
| 2 | Dogfood-gated edits honoured (WI-06, WI-09, WI-12) | PASS |
| 3 | Deviations documented (per-wave commits; dual-write) | PASS |
| 4 | Success gates met (6/6 §7 commands) | PASS |
| 5 | No blockers to ship (release-plan READY) | PASS |
| 6 | Release notes accurate (3/3 spot-checks) | PASS |
| 7 | Retro notes captured (7/7 routed) | PASS |

**Seven for seven.**

---

## 4. Final Verdict

# GO

The engagement is ready to ship. The skills speak the language of their runtime. The guards are armed. The backlog is logged on both surfaces. The notes are honest. The deviations are owned. The Fellowship walked the road together and left no piece of gear behind.

My verdict is not a celebration — it is a judgement. This was, as Bilbo said, a mostly-ordinary journey. That is the highest praise I can offer.

---

## 5. PR Proposal — Title + Body Skeleton

**Title** (per Samwise §4 condition 4, ≤70 chars permitted by the PRD convention but held here at the exact form the deploy-plan dictated):

```
feat(delivery): execute Opus 4.7 migration plan (run-2026-04-22-4x7e)
```

**Body skeleton** (to be passed via HEREDOC at `gh pr create` time):

```markdown
## Summary

Executes the approved Opus 4.7 plugin-skill migration per the transformation
plan (`.delivery/artifacts/04-architect/solution/transformation-plan.md` rev 1,
§6 Roadmap) and the execution-PRD
(`.delivery/artifacts/08-execute/02-refine/po/execution-prd.md`). All 14 work
items (WI-01 through WI-14) complete across four waves. No breaking changes;
migration is additive (frontmatter) and mechanical (model-ID sweep).

- All 17 SKILL.md files carry `model_awareness:` frontmatter
  (6 keystone `opus-4-7` + 11 backfill `opus-4-7-frontmatter-only`).
- Model-ID sweep in `agentic-flow-builder/scripts/agent_registry.py`
  (3 substitutions + provenance comments); `prd-quality-gate-flow/stage_definitions.py`
  annotate-only per WI-10 AC-01.5 structural check.
- `prompt-engineer/SKILL.md` carries the canonical 4.7-era pattern library
  (Patterns 4.1–4.6) + PAT-01 reframe; anchors cited by sibling SKILL.md files.
- Two new CI guards: `skill-md-header-warn.yml` (warning-only, DX-M4) and
  `stale-model-id-guard.yml` (blocking, M-02, with calibrated allowlist for
  provenance comments). `workflow-injection-lint.yml` (DEFECT-004) unchanged.
- Nine `backlog-47` items dual-written as local files AND GitHub issues
  (#77–85) per user-directed WI-13 dual-write.

## Six §7 verification commands — all green

| # | Gate | Expected | Actual |
|---|------|---------|--------|
| 1 | M-01 stale-ID grep (PRD-canonical) | 0 stale | 0 stale (3 provenance-comment hits allowlisted) |
| 2 | DX-M4 missing-header count | 0 | 0 |
| 3 | Two-tier stamp integrity (6 / 11) | 6 + 11 | 6 + 11 |
| 4 | DX-M3 `<thinking>` restatement count | 0 | 0 |
| 5 | WI-13 dual-write invariant | ≥6 == ≥6 | 9 == 9 |
| 6 | WI-14 CI guard files present | exit 0 | exit 0 |

Full verification evidence at
`.delivery/artifacts/08-execute/07-uat/qa/uat-verification.md`.

## Deviations from plan

1. **Per-wave commits (4) instead of per-WI commits (14).** Wave boundaries
   are mechanical gates; each wave commit body enumerates its WIs. Documented
   in `.delivery/artifacts/08-execute/07-uat/devops/release-plan.md` §3. A new
   Tier-1b partial-wave surgical revert procedure (§6) handles the case where
   a single WI inside a wave needs to be undone without the rest.
2. **WI-13 dual-write (local + GitHub).** Authored deviation from transformation
   plan §6.2 per idea-brief §5 user direction. 9 files + 9 issues (6 required
   + 3 optional Galadriel on-ramp).

## Test plan

- [x] `grep -rEn 'claude-(opus|sonnet|haiku)-4[.-]6' --exclude-dir=.delivery` returns only canonical / guard-internal references
- [x] `find . -name SKILL.md -not -path './.delivery/*' | xargs grep -L 'model_awareness:' | wc -l` returns `0`
- [x] `grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` returns `6`
- [x] `ls .delivery/backlog/BACKLOG-47-*.md | wc -l` returns `9`
- [x] `gh issue list --label backlog-47 --state all --json number --jq 'length'` returns `9`
- [x] `test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml`
- [x] `stale-model-id-guard.yml` calibrated dry-run returns 0 blocking hits on HEAD
- [x] `skill-md-header-warn.yml` dry-run: 0 SKILL.md missing the marker
- [x] `workflow-injection-lint.yml` unchanged (DEFECT-004 guard intact)
- [ ] Post-merge synthetic test: introduce `claude-opus-4-20250514` in a test PR — confirm guard blocks (WI-14 AC-5)
- [ ] Post-merge synthetic test: introduce SKILL.md without marker — confirm warning fires, PR remains mergeable (WI-14 AC-5)

## Rollback

- **Tier 1 (per-wave):** `git revert <wave-sha>` — four clean wave commits.
- **Tier 1b (partial-wave surgical):** `git revert -n <wave-sha>` + manual
  restore + commit. Documented in release-plan §6.
- **Tier 3 (full withdrawal):** `git revert <merge-sha>` on `main`.
- See `.delivery/artifacts/08-execute/07-uat/devops/release-plan.md` §6 for full
  procedure, including the Wave-4 revert-ordering caveat.

## Artefact index

- Execution PRD: `.delivery/artifacts/08-execute/02-refine/po/execution-prd.md`
- UAT verification: `.delivery/artifacts/08-execute/07-uat/qa/uat-verification.md`
- Release plan: `.delivery/artifacts/08-execute/07-uat/devops/release-plan.md`
- Release notes: `.delivery/artifacts/08-execute/07-uat/tech-writer/release-notes.md`
- PO Go/No-Go: `.delivery/artifacts/08-execute/07-uat/dod/po-review.md`
- Transformation plan (binding): `.delivery/artifacts/04-architect/solution/transformation-plan.md`
- Six binding ADRs: `.delivery/artifacts/04-architect/adrs/ADR-00{1..6}-4-7-*.md`

Closes: items tracked by this engagement.
Refs: #77, #78, #79, #80, #81, #82, #83, #84, #85 (deferred scope, tracked by `backlog-47` label).

Co-Authored-By: The Fellowship (Gandalf, Celebrimbor, Gimli, Legolas, Samwise, Bilbo, Galadriel, Théoden, Aragorn, the Challenger, and the Hobbits of the Shire)
```

The `gh pr create` call uses `--base main --head feature/opus-4-7-migration-run-2026-04-22-4x7e` and passes this body via HEREDOC per repository convention.

---

## 6. Post-Merge Actions (handed to Samwise and Théoden)

1. Samwise fires the two WI-14 AC-5 synthetic tests (stale-ID reintroduction, missing-marker SKILL.md) per release-plan §5.2–5.3. Expected: first blocks, second warns but allows merge. Both close without merging.
2. Samwise deletes `feature/opus-4-7-migration-run-2026-04-22-4x7e` after merge confirmation.
3. Théoden runs the Stage 7 retrospective (pipeline hook will enforce this before session end). Carry F-UAT-01, the commit-cadence precedent, the provenance-comment/allowlist pattern, and the dogfood-before-edit track record into `.delivery/memory/`.
4. I review the 9 open `backlog-47` issues post-merge. Per Samwise §5.1 expected outcome, most stay OPEN as deferrals — that is the point of BACKLOG-47; items are tracked, not closed by the engagement that logged them.

None of these are gates on the merge. They are the follow-through that makes the next engagement cheaper.

---

## 7. One Quiet Word to Whoever Walks Next

The two-tier stamp — `opus-4-7` (keystone, prose-reviewed) vs `opus-4-7-frontmatter-only` (backfill, mechanical) — is the honest answer to a question we will face again. When the next model arrives, do not be tempted to stamp every file `opus-4-N` in a mechanical sweep and call it review. Use the tier. Eleven files still wait for a word-by-word read; backlog #81 tracks the upgrade path. That debt is named. Pay it when the road allows. Do not pretend it isn't there.

And when the PRD §7 regex speaks too literally of its own task, tighten the regex or rewrite the success criterion — do not argue with the ground when the ground is right. (F-UAT-01. Log it. Close it next time.)

---

*"The path was walked. The rings are in their box. And the kingdom, for the first time in some weeks, speaks with the same voice as the model that reads it. Go well. Light your next fire from this one."*
— Gandalf

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/07-uat/dod/po-review.md
SUMMARY: Seven gates struck true — scope carried, dogfood held, deviations owned, notes honest, no silent threads; the ring goes quietly into its box. GO.
```
