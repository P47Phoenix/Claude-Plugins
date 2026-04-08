# DevOps DoD Review — Stage 07 UAT

**Reviewer**: Samwise Gamgee (DevOps)
**Artifact under review**: `.delivery/artifacts/07-uat/devops/release-plan.md`
**Bundle**: Orchestration Discipline (v2.7), marketplace 2.17.1 -> 2.18.0
**Verdict**: **DONE**

> *"Right then, Mr. Frodo — let's walk the path one more time before we lock the door. Boots tied, kettle off, lembas counted twice."*

---

## DoD Criteria

### 1. Release plan complete

| Requirement | Status | Evidence |
|---|---|---|
| Pre-release checklist covers working tree, artifacts, schema, hooks, docs, dogfood, PR readiness | DONE | §1.1–§1.7, seven sub-sections, every box actionable |
| Release steps are linear and unambiguous | DONE | §2.1–§2.9, nine numbered steps from sanity sweep through announce |
| Commit-per-story discipline preserved | DONE | §2.2 enforces edit-map scope, conventional-commits, `refs #NN` vs `Closes`, co-author trailer |
| Branch + push flow matches deploy plan | DONE | §2.3 single rebase, §2.4 push gated on §1 + §2.1–§2.3 green |
| PR creation uses draft -> CI -> ready transition | DONE | §2.5 draft PR, §2.6 CI watch, §2.7 `gh pr ready` only after CI green |
| Human checkpoint defined with merge-method guard | DONE | §2.8 explicitly requires **Merge commit** (not squash, not rebase), preserving the 12–13-commit history |
| Post-release verification covers GitHub state, CI, schema parity, hooks, dogfood, follow-ups, memory write-back | DONE | §4.1–§4.7, seven sub-sections, all "none of these are optional" |
| Sign-off ritual specified | DONE | §5 names the file (`.delivery/state.md`) and the exact line format |

**Release plan: complete.** Every gate the deploy plan promised gets a typed-out command or a checkbox here. No hand-waving, no "TBD".

### 2. Rollback documented

| Requirement | Status | Evidence |
|---|---|---|
| Rollback ladder has clear severity levels | DONE | §3.1 decision table maps symptom -> level (L1/L2/L3/L4) |
| Each level has copy-pasteable commands | DONE | §3.2 (L1 single-commit), §3.3 (L2 issue-scoped), §3.4 (L3 full-bundle merge revert with `-m 1`), §3.5 (L4 emergency pin notice) |
| L3 covers the merge-revert subtleties | DONE | §3.4 explicitly notes `git revert -m 1`, manual issue reopen via `gh issue reopen`, marketplace version walk-back to 2.17.1 |
| L4 acknowledges direct-to-main as last resort with justification | DONE | §3.5 single-doc-file scope, README admonition wording provided, tracking issue requirement |
| Schema v2.6 tolerant-parse fallback documented for users | DONE | §3.5 admonition tells users exactly which keys to pin: "v2.6 tolerantly parses any v2.7 keys" |

**Rollback: documented.** Four levels, every level with a runbook, every command shell-ready.

### 3. Rollback achievable

This is the criterion that usually fails on paper plans. It does not fail here.

| Achievability check | Status | Evidence |
|---|---|---|
| L1/L2/L3 are exercised BEFORE the release PR merges | DONE | §3.6 "Rollback rehearsal" performs a `--no-ff --no-commit` simulated merge, then a dry-run `git revert -m 1`, then `git reset --hard origin/main` to discard the rehearsal. Rehearsed reverts are achievable reverts |
| Rehearsal failure mode is defined | DONE | §3.6 "If the dry-run revert had conflicts, fix them in the source branch BEFORE merging the release PR" |
| L3 known gap (issue auto-reopen) is anticipated | DONE | §3.4 calls out that merge-commit revert does NOT auto-reopen — manual `gh issue reopen` listed as a step, not a footnote |
| Marketplace version walkback included | DONE | §3.4 deliberate `2.18.0` -> `2.17.1` follow-up commit, framed as a user-facing signal |
| L4 escape hatch underwritten by real backward-compat | DONE | Tolerant-parse design from the bundle itself (validated in §1.4) makes the L4 admonition truthful, not aspirational |
| Time-to-revert is bounded | DONE | L1 ~5 min (single revert + push + CI), L2 ~10 min, L3 ~15 min + manual reopens, L4 ~2 min direct-to-main doc edit. All achievable inside an incident window |

**Rollback: achievable.** The §3.6 rehearsal is the load-bearing item — it converts "documented rollback" into "proven rollback". Proper Gaffer-grade discipline.

---

## Cross-cutting checks

- **Consistency with deploy plan**: §2 release steps match the deploy plan §3 commit table; §3 ladder matches deploy plan §5's four-level structure; §2.8 merge-commit guard matches the deploy plan's history-preservation rationale. No drift.
- **CI surface honest**: §2.6 names the only automated gate (`docs.yml` MkDocs build) — no fictional test suites, no pretend coverage gates. Honest about what exists.
- **Git safety per CLAUDE.md**: §2.2 explicitly forbids amending and routes corrections through new commits or pre-push `reset --soft`. §3.5 names direct-to-main as exceptional and bounds it to a single doc file. Aligned with project safety protocol.
- **Self-learning loop closed**: §4.7 writes back a tier-3 memory chunk so the next release inherits the lesson. The pipeline learns from itself.
- **Dogfood evidence**: §1.6 and §4.5 require the orchestrator to prove discipline (zero compound prompts, zero out-of-allowlist self-writes) on this run AND the next run after merge. The release plan trusts but verifies.

## Minor observations (not blocking)

- §2.9 offers a choice between channel post and `.delivery/release-notes/` file. Either is fine; recommend committing the file form so the release note becomes part of the audit trail. Not a defect.
- §4.4 hook smoke test re-runs the §1.4 fixtures from a clean clone. Consider tucking those fixture files into `delivery-team/hooks/fixtures/` in a future sprint so the smoke test stops being tribal knowledge. Logged as a follow-up, not a blocker.

Neither observation prevents this stage from passing DoD.

---

## Verdict

**STATUS: DONE**

The release plan is complete, the rollback is documented across four levels with copy-pasteable commands, and rollback achievability is proven by the §3.6 pre-merge rehearsal. DevOps signs off on Stage 07 UAT for the Orchestration Discipline Bundle.

> *"There and back again, Mr. Frodo. And if 'back again' is needed, we've already practiced the road."*

— Samwise Gamgee, DevOps
