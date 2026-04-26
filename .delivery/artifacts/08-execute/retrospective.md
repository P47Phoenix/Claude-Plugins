# Retrospective — run-2026-04-22-4x7e (Opus 4.7 execution engagement)

**Date:** 2026-04-22
**Pipeline:** FEATURE executing transformation-plan rev 1
**Outcome:** GO (PR ready)
**Stages:** 1, 2, 4, 5, 6, 7 executed (stage 3 Design skipped — DX-only)
**Facilitator:** Aragorn (Scrum Bag)
**Role:** Servant leader — the one who carries water, not swords

---

> *"A king is not the one who walks ahead of the company. A king is the one who counts the company at dusk and names each member who carried a burden today. The Fellowship reached the far side of the river. Before we build the next raft, we sit by this fire and say out loud what the crossing taught us — so that the next crossing costs less, and so that those who come after find the shore we found, not the one we feared."*
>
> *"We will speak warmly. We will name what went well without smug pride, and name what did not without blame. Every voice in the Fellowship has something to give to the next walk. Let us listen to each of them."*
>
> — Aragorn

---

## What went well (keep doing)

1. **Dogfood-before-edit held across all three guarded WIs.** WI-06 (research-agent probe), WI-09 (mtg-commander Challenger), and WI-12 (alias-theme voice) each ran their empirical check *first* and then decided whether a prose edit was warranted. All three dogfoods passed; two required zero prose touches, one required a single-line semantic-equivalent rephrase (`mtg-commander/SKILL.md:825`, "chain-of-thought" → "internal reasoning trace") that was documented honestly rather than dressed up as a rewrite. This was the load-bearing rule of the migration, and it held without strain. *Evidence:* Gandalf's §Gate 2 in `.delivery/artifacts/08-execute/07-uat/dod/po-review.md`; Bilbo's adversarial/research section in the release notes.

2. **Gimli's WI-10 flag to WI-14 mid-run was the best moment of the engagement.** When Gimli substituted the dated Opus/Sonnet/Haiku IDs into `agent_registry.py`, he noticed immediately that the M-01 stale-ID regex from the kickoff plan (`claude-(opus|sonnet|haiku)-4[.-]6`) would false-positive on the *canonical* Sonnet 4.6 target that the same plan required him to install. Rather than silently bend the regex or silently bend the target, he wrote a forward-flag in the dev log naming the contradiction and recommending an allowlist-over-deny approach for WI-14. WI-14's CI guard was then authored with the allowlist (`grep -vE 'claude-sonnet-4-6(\b|[^0-9-])'`) and the calibration held at UAT. *Evidence:* `.delivery/artifacts/08-execute/06-dev/dev-log-wi-10.md` §5, and the allowlist now living in `.github/workflows/stale-model-id-guard.yml`.

3. **Gimli's Refine-gate runs-the-command DoD caught six defects before any code was cut.** In the Stage 2 developer DoD round 1, Gimli did not read the execution-PRD's 14 dogfood commands — he *ran* each of them from the repo root, on his own Fedora shell. That surfaced G-1 (WI-14 depended on `yq`, which was not installed on the host), G-2 (`**/SKILL.md` shell-glob that doesn't expand under default bash), G-3 (awk vacuous-pass on empty stdin), G-4 (WI-12 format coupling to a table shape not required by the AC), G-5 (§7.4 grep scope wider than WI-05's edit surface), and G-6 (`-cE` vs `-qE` hygiene). One blocker, five non-blockers, all named with a concrete fix. This is the memory-file `feedback_dogfooding.md` lesson repeating itself productively — and it saved the impl-run from at least one fatal gate at Wave-4. *Evidence:* `.delivery/artifacts/08-execute/02-refine/dod/developer-review.md`, G-1..G-6.

4. **The two-tier stamp convention (`opus-4-7` vs `opus-4-7-frontmatter-only`) was an honest answer to an honest question.** Six keystone SKILL.md files received prose-level review and earned the full `opus-4-7` stamp; eleven backfill files received only the YAML header and were stamped `opus-4-7-frontmatter-only` — a deliberately different string that does *not* claim prose-level 4.7 review. The distinction is grep-able, auditable, and tracked by BACKLOG-47-frontmatter-only-prose-skim.md for the future upgrade path. The team resisted the easy temptation to stamp all 17 files uniformly and call it done. *Evidence:* §Gate 3 two-tier integrity in the UAT verification (6 + 11); Gandalf's "One Quiet Word to Whoever Walks Next" at `po-review.md:273`.

5. **Per-wave commits with WI enumeration in the body was a defensible cadence choice, not a corner cut.** The deploy-plan recommended 14 per-WI commits; the impl-run chose 4 per-wave commits with each commit body naming its WIs. Samwise documented the deviation in a seven-row trade-off table (audit trail, rollback granularity, PR readability, conventional-commits adherence, commit-message body, revert-unit size), explained why wave boundaries are mechanical gates and therefore defensible atomicity units, and introduced a new Tier-1b partial-wave surgical revert procedure for the case where a single WI inside a wave later needs to be undone. No quiet deviation. *Evidence:* `.delivery/artifacts/08-execute/07-uat/devops/release-plan.md` §3 + §6.

6. **WI-13 dual-write exceeded its floor — and every item was mapped 1:1 slug-to-title.** The user-directed dual-write (idea-brief §5) asked for six deferred items tracked as both local backlog files AND GitHub issues labeled `backlog-47`. The Fellowship logged nine (six required + three optional Galadriel on-ramp items: `contributing-4-7-note`, `migration-guide-stub`, `4-7-example-skill-designation`). Legolas verified the slug-to-title invariant; Samwise confirmed the count-equality invariant (local == GH, both ≥ 6); Bilbo's release notes enumerate all nine explicitly. Over-delivery without noise. *Evidence:* UAT verification §5–§6; issues #77–#85; nine `BACKLOG-47-*.md` files on disk.

7. **The seven-gate UAT rubric held without drama.** Gandalf's Stage 7 PO Go/No-Go walked seven gates in order — scope honoured, dogfood-gated edits honoured, deviations documented, success gates met, no blockers to ship, release notes accurate (with three-bullet spot-checks run live against the repo), retro notes captured. Seven for seven, each with evidence cited from a sibling's artefact, each with the one nuance named (F-UAT-01 on gate 4; the gate-6 spot-check of Bilbo's honesty about the mtg-commander prose edit). No gate was waved through. No gate was inflated. The rubric did what a rubric should: it made the PO's judgement auditable, not ceremonial. *Evidence:* `.delivery/artifacts/08-execute/07-uat/dod/po-review.md` §2.1–§2.7.

---

## What did not go well (stop doing)

1. **PRD §7 gate 1 was written without regard for its own allowlist obligations.** The canonical M-01 literal command (`! grep -rEn 'claude-(opus-4-20250514|sonnet-4-5-20250929|haiku-4-20250514)' agentic-flow-builder/ prd-quality-gate-flow/ --include='*.py'`) conflates live executable references with history-preserving provenance comments. Post-WI-10, `agent_registry.py` carries three such comments (`# canonical 2026-04-22 — opus-4-7 migration; prior: <retired-id>`) and the literal one-liner therefore returns exit 1 even though the gate's *intent* (no live stale references in executable code) is fully satisfied. The CI guard's own allowlist (`^[^:]+:[^:]+:[[:space:]]*#`) correctly drains these three, but the PRD's literal command does not. Filed as F-UAT-01 (LOW, advisory). *Stop doing:* authoring success-definition regexes that do not anticipate the artefacts the engagement is required to produce. *Evidence:* Legolas §1 "M-01 — Stale 4.6 IDs purged" in `.delivery/artifacts/08-execute/07-uat/qa/uat-verification.md`.

2. **The WI-10 → WI-14 regex contradiction should have been caught in the transformation-plan, not mid-execution.** Gimli's catch was excellent, but the root cause was upstream: the transformation-plan's mixed-version migration (Opus → 4.7, Sonnet → 4.6, Haiku → 4.5-dated) could not be covered by a single "any 4.6-era ID is stale" regex. The plan specified both the canonical Sonnet 4.6 target *and* the stale-ID regex without noticing the collision. A plan-coherence review pass focused on "does the end-state match the success-gates?" would have caught this before Gimli had to. *Stop doing:* shipping success-gate regexes in the same document as the canonical-ID list without running at least a paper-trace of one against the other. *Evidence:* dev-log-wi-10.md §5 "Flag to WI-14".

3. **`yq` dependency on the Developer-DoD host slipped past Refine round 1 — barely.** Gimli's runs-the-command pass caught it, but the WI-14 dogfood was authored without regard for what is actually installed on a default developer laptop (no `yq` in path on the dogfood host). *Stop doing:* introducing CLI dependencies into Developer-DoD commands without either (a) replacing them with bash-only or python-with-PyYAML equivalents, or (b) explicitly documenting the install step in a dogfood-prereqs section of the PRD. The principle: a DoD command that cannot be executed by the person who must execute it is not a DoD command. *Evidence:* G-1 in `.delivery/artifacts/08-execute/02-refine/dod/developer-review.md`.

4. **The scope-coverage gap between WI-05 and §7.4 (DX-M3) was found at the same pass that caught G-1, but the pattern is structural.** WI-05 edits `prompt-engineer/SKILL.md` only; §7.4 greps `<thinking>` across every plugin except `prompt-engineer/SKILL.md`. A `<thinking>` restatement sitting in `research-agent/references/prompt-library.md:10` was out-of-scope for WI-05's edit surface but in-scope for §7.4's success gate. Gimli flagged it (G-5); the impl-run resolved it by scoping in a references sweep. *Stop doing:* defining success gates whose scope is wider than the WI-set that produces the edits expected to close them. Every success gate should name the WI that closes it, and that WI's scope must cover the gate's scope. *Evidence:* G-5 in developer-review.md; UAT §4 DX-M3 PASS with 0 hits after the sweep.

---

## Lessons learned (feed into memory system)

1. **Dev DoD runs the command, does not read the command.** This is not a new lesson — it is the third consecutive engagement where it has proven its worth, and the first where every single success-gate command was empirically executed at Refine time by the Developer DoD. Gimli found one blocker and five non-blockers in a single light-mode pass. The lesson for memory: the "light" in "light mode DoD" means reduced depth of prose review, not reduced depth of command execution. Running commands is the DoD. Reading them is the prelude. *Memory target:* `.delivery/memory/topics/dod-patterns.md` (reinforce the runs-the-command rule explicitly for Refine light mode).

2. **Mixed-version migrations need their own allowlist discipline.** When a family migration is uniform (everything → 4.7), a single deny regex suffices. When it is mixed (Opus → 4.7, Sonnet → 4.6, Haiku → 4.5-dated), the allowlist-over-deny approach is the only one that survives the next bump. The canonical set for 2026-04-22 is `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001` — everything else dated is stale. Future CI guards should use this shape; future transformation-plans should specify this shape. *Memory target:* `.delivery/memory/topics/model-migration-patterns.md` (new).

3. **Honest readiness markers beat uniform readiness markers.** The two-tier stamp (`opus-4-7` for prose-reviewed keystones; `opus-4-7-frontmatter-only` for mechanical backfill) names the state of the work honestly. A future migration author who reads `opus-4-7-frontmatter-only` knows they are reading a file that has not had a word-by-word review — which is the information they need to make the right call at that file. A uniform stamp would have lied cheaply. *Memory target:* `.delivery/memory/topics/readiness-marker-conventions.md` (new, tied to ADR-006 and BACKLOG-47-frontmatter-only-prose-skim).

4. **Mid-run flags to future WIs are a team capability, not a bug.** When Gimli implementing WI-10 noticed that WI-14's regex as specified would false-positive on his own output, he flagged it forward rather than silently accommodating it. The orchestrator accepted the flag, WI-14 was authored with the calibration already baked in, and the CI guard now ships correct on the first try. This pattern — *impl-run WI surfaces plan-level contradiction to a later WI mid-wave* — is cheaper than any amount of upstream paper-review. *Memory target:* `.delivery/memory/topics/mid-run-flag-protocol.md` (new); codify as a first-class dev-log section.

5. **Provenance comments are a feature, not noise — and CI guards must know this.** The decision to keep `# prior: <retired-id>` breadcrumbs above each substituted model-ID line was right: they give the next reader the history without requiring a git blame trip. But the CI guard and the PRD success regex must both allowlist the comment pattern (`^\s*#`) or they will fail on the very provenance they exist to preserve. This is now ADR-002's provenance-comment pattern + the stale-model-id-guard allowlist, and both need to travel together into future engagements. *Memory target:* `.delivery/memory/topics/adr-provenance-patterns.md` (new, cross-reference ADR-002).

6. **Per-wave commits with WI enumeration beats per-WI commits for this shape of migration.** Fourteen WIs across four mechanical waves, each wave's gate a deterministic structural check, zero behavioural coupling between WIs within a wave — this is the shape where per-wave commits trade granular revert for audit-trail readability on the winning side. The new Tier-1b partial-wave surgical revert procedure (`git revert -n <wave-sha>` + manual restore + commit) closes the one hole per-wave commits would otherwise leave. *Memory target:* `.delivery/memory/topics/commit-cadence-patterns.md` (new); pair with a rule of thumb: "per-WI commits for behaviourally-coupled WIs; per-wave commits for mechanically-independent WI batches."

7. **The dogfood-before-edit primitive is the highest-leverage rule in a tone-risk migration.** For WI-06, WI-09, and WI-12, the prose edits that were *planned* were all avoided because the dogfood showed the prose did not actually need touching. This saved effort, but more importantly it prevented the drift-by-edit pattern (where a prose "improvement" accidentally strengthens tone or rephrases authorial voice out of the artefact). F-27 risk on 4.7 is real; the dogfood-first rule is its discipline. *Memory target:* `.delivery/memory/topics/dogfood-primitive.md` (reinforce as a named pattern, not a one-off WI convention).

8. **Success-gate ownership must be explicit: one WI closes one gate.** The WI-05 / §7.4 scope-coverage gap (G-5) happened because no WI was explicitly named as the closer of §7.4. When the gate scope is wider than the nearest WI's edit surface, either the gate is wrong or the WI is under-scoped. The lightweight fix: every success gate in §7 names the WI that closes it, and that binding is verified at Refine DoD time. *Memory target:* `.delivery/memory/topics/success-gate-authoring.md` (new).

---

## Action items (for next engagement)

- **A1: Tighten PRD §7 authoring rubric to exclude provenance comments from stale-ID regexes.** Add `| grep -vE '^[^:]+:[[:space:]]*#'` or equivalent comment-scope-out to every stale-ID command; or convert commands to `git grep` with explicit pathspec allowlists. Owner: PO (Gandalf). Done-by: before next migration PRD is drafted.
- **A2: Add a "plan coherence pass" to the transformation-plan DoD.** Paper-trace each §7 success-gate command against the canonical-ID list and the planned end-state; require PASS before the plan lands. Owner: Architect (Celebrimbor). Done-by: before next transformation-planning sub-workflow run.
- **A3: Document the allowlist-over-deny pattern for mixed-version migrations in the architect paradigm library.** Include the canonical-set rule of thumb and a template CI guard. Owner: Architect (Celebrimbor). Done-by: before next migration engagement.
- **A4: Enforce "no new CLI dependencies in Developer-DoD commands" rule in the Refine checklist.** Either (a) bash-only / python-with-stdlib / python-with-PyYAML equivalents, or (b) explicit documented install in a dogfood-prereqs section. Owner: PO (Gandalf) + Developer (Gimli). Done-by: before next Refine round 1.
- **A5: Add a "mid-run flag section" to the dev-log template.** Any implementer who notices an upstream contradiction that will bite a later WI writes a `## Flag to WI-N — <title>` section; orchestrator routes these before the flagged WI lands. Owner: Scrum Bag (Aragorn). Done-by: before next execution engagement.
- **A6: Upgrade path for the eleven `opus-4-7-frontmatter-only` files is tracked.** BACKLOG-47-frontmatter-only-prose-skim.md + GH #81 carry the debt. Next engagement that touches any of these eleven files does a prose skim and re-stamps to `opus-4-7` on the way through — do *not* mechanically restamp the whole eleven in a sweep. Owner: whoever edits any of the eleven next. Done-by: opportunistic, not deadlined.
  - **Post-rebase note (2026-04-23):** after rebase onto `origin/main`, the `hardware-team` plugin landed with 8 new SKILL.md files (commit `ff3ac93`). Per lesson 3 and the two-tier convention, these were stamped `opus-4-7-frontmatter-only` rather than `opus-4-7` — hardware-team was authored separately and has NOT had prose-level review against Opus 4.7 guidance. The backfill pool is now **19** files (11 original + 8 hardware-team), not 11. Keystone stamps remain **6**, total SKILL.md count is **25**. The A6 debt and its upgrade-on-touch policy extend to all 19.

---

## Metrics

- **Duration:** single session
- **Stages completed:** 6 / 7 (Design skipped — documented as DX-only routing deviation, recorded at stage-entry, not silent)
- **Waves completed:** 4 / 4
- **WIs completed:** 14 / 14
- **DoD self-correction rounds:** Refine stage round 1 (Gimli's G-1..G-6 batch) — one round, six findings, one blocker cleared before round 2
- **Dogfood passes first-try:** WI-06, WI-09, WI-12 all PASS-first (no edits triggered beyond the single mtg-commander line-825 semantic rephrase on WI-09)
- **Backlog items registered:** 9 (6 required + 3 optional Galadriel on-ramp items)
- **GitHub issues created:** 9 (#77–#85, all labeled `backlog-47`)
- **Defects introduced:** 0 (by engagement's own definition — no regressions detected by dogfood)
- **Success-gate pass rate:** 6 / 6 binding §7 gates; 1 advisory note (F-UAT-01) logged without blocking
- **Commit cadence:** 4 per-wave commits (deliberate deviation from 14 per-WI plan default)

---

## Carry-items for future engagements

- **F-UAT-01 (PRD §7 gate 1 regex hygiene)** — the next migration PRD that uses stale-ID grep regexes must scope out provenance comments (`^\s*#`) or rewrite the success criterion to "no live references in executable paths." Tracked here; acted on per A1.

- **WI-10 → WI-14 pattern: mixed-version migrations need allowlist-over-deny CI guards** — when editing model IDs across a mixed-family migration, the stale-ID regex in the blocking CI guard must allowlist canonical family IDs explicitly. What started as a 1→2 order dependency mid-Wave-4 becomes a first-class plan rule per A3.

- **Two-tier stamp convention (`opus-4-7` vs `opus-4-7-frontmatter-only`)** — the convention is accurate for THIS migration, but future migrations should NOT restamp `-frontmatter-only` files mechanically. When a future engagement touches one of the eleven backfill files, do the prose skim first and earn the full stamp then. BACKLOG-47-frontmatter-only-prose-skim.md / GH #81 tracks this debt; do not pretend the debt isn't there.

- **ADR-002 provenance-comment pattern + stale-model-id-guard allowlist travel together** — if one is edited, the other must be reviewed. Named pair.

- **Dogfood-before-edit primitive holds as a general tone-risk discipline** — not just this migration's rule; adopt it for any engagement that includes prose touches to skills / agent personas / alias themes.

---

> *"The Fellowship walked a road this day. Some of us carried commands in our hands and ran them before reading them. Some of us carried a regex in our heads and flagged forward when its shape would wound a brother ahead. Some of us counted the stamps on seventeen doors and refused to call a mechanical stamp a prose-read. Some of us chose a wave-shaped commit cadence and named our reasons in full, without quiet. Some of us dual-wrote a backlog so the next company would not have to look in one place and then the other."*
>
> *"No grand deeds. No lost members. A mostly-ordinary crossing, done well. That is what I will remember."*
>
> *"Go well, all of you. Light the next fire from this one."*
>
> — Aragorn

---

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/retrospective.md
SUMMARY: The Fellowship crossed the river with the company intact — seven lessons carried to memory, six action items named with owners, nothing silent; the next crossing will cost less.
```
