# ADR-006 — 4.7-Readiness Marker Convention: YAML Frontmatter Header Strip

**Status:** Accepted
**Date:** 2026-04-20
**Architect:** Celebrimbor
**Engagement:** Opus 4.6 → 4.7 Transformation Plan
**Related:** Galadriel DX pillars P-1 / P-7; Pattern 4.6; DX metric DX-M4; Open Questions Galadriel §7 Q2; Q5 (REQ-10 baseline integration)
**Supersedes:** none
**Superseded-by:** none

**Rollback trigger:** this decision is committed (Accepted), but if the Wave-1 WI-03 spike discovers that the SKILL.md frontmatter schema validator strict-rejects unknown fields, the Decision section below is revoked and the ADR is superseded-in-place by the Option-B (HTML comment) implementation (Alternatives Considered §B; Implementation Notes §Pre-requisite). The Wave-1 WI-03 spike MUST complete before any frontmatter-touching WI (WI-04, WI-05, WI-06, WI-11) dispatches. No ambiguity: if WI-03 says "strict," Option A does not ship; if WI-03 says "unknown fields accepted," Option A ships as-written.

---

## Context

Galadriel's DX-M4 shows all 17 in-scope SKILL.md files currently lack a forward-compatibility marker — a 4.7-aware file and a 4.7-naive file are textually indistinguishable. Galadriel P-1 proposes a scannable header strip inside the existing YAML frontmatter (all 17 files already carry 5–11-line frontmatter per scope-baseline §4).

Options for where the marker lives:

- **Option A — YAML frontmatter field** (`model_awareness: opus-4-7`, `last_audited: YYYY-MM-DD`, `pattern_library_version: 4-7-N`).
- **Option B — Comment block below frontmatter** (HTML comment or markdown admonition).
- **Option C — Filename convention** (`SKILL-4-7.md` or similar).
- **Option D — Separate sidecar file** (`SKILL.md.meta`).

CLAUDE.md conventions and the marketplace.json skill discovery contract pivot on YAML frontmatter being pure and minimal. Changing filenames breaks the manifest (PRD Constraint 2 — plugin architecture frozen). Sidecar files introduce a new surface with no existing precedent.

## Decision

Adopt **Option A — three new YAML frontmatter fields** as the 4.7-readiness marker, with a light-touch CI convention (warning, not blocking) for coverage.

Field definitions:

```yaml
---
name: <existing>
description: <existing>
model_awareness: opus-4-7
last_audited: YYYY-MM-DD
pattern_library_version: 4-7-N
---
```

- **`model_awareness`** — a free-text tag naming the latest model family the file has been deliberately reviewed against. Two tier values for this engagement:
  - `opus-4-7` — file's **prose** was reviewed against 4.7 (keystones edited in Waves 2–3).
  - `opus-4-7-frontmatter-only` — file received the ADR-006 marker mechanically (Wave 4 WI-11) with no prose review. Prevents a future `grep 'model_awareness: opus-4-7$'` from over-counting reviewed files (fresh-challenger F-C-08 priority #3). Upgrade from `-frontmatter-only` to `opus-4-7` requires a future prose-skim backlog item (logged in plan §6.5).

  Future 4.8 migration will bump to `opus-4-8` and (if re-running) `opus-4-8-frontmatter-only`.
- **`last_audited: YYYY-MM-DD`** — ISO date. Set by whoever performs the Wave 3 keystone edit. CI warns (not blocks) if the date is more than 180 days old on a 4.7-tagged file.
- **`pattern_library_version: 4-7-N`** — tracks the Galadriel Pattern 4.6 / ADR-005 central library. Starts at `4-7-1`; increments when `prompt-engineer/SKILL.md` adds or materially edits a pattern. Skills citing patterns by name implicitly pin themselves to a library version.

Scope:

- **All 17 SKILL.md files** gain the three fields during Wave 3. The two paradigm sub-skills (66 and 80 LOC) inherit via parent if the parent convention allows; otherwise duplicate.
- **CI check (new, low-priority):** a warning-only grep (`grep -L "model_awareness:" **/SKILL.md`) runs on PRs. Does not block merge. Logs a reminder. Lives alongside the existing `workflow-injection-lint.yml` regression guard pattern.
- **Retroactive backfill** for non-keystone SKILL.md files happens in a single Wave 4 mechanical edit (WI-11). No prose edits; frontmatter-only addition.

## Consequences

- **Positive:** A reader can triage 4.7-awareness in under 10 seconds without scrolling (Galadriel DX-M1 target). Satisfies DX-M4 (header coverage target: 0 missing).
- **Positive:** `last_audited` dates create a visible decay signal — files that silently age past 4.7 become observable at review time.
- **Positive:** YAML frontmatter is the existing skill metadata surface; no new convention, no new file, no schema churn. Preserves PRD Constraint 2.
- **Positive:** CI as a *warning* (not a block) matches the past memory lesson `feedback_team_autonomy.md` — team makes autonomous decisions; we don't hard-gate on marker drift.
- **Negative:** Three new fields per SKILL.md is non-zero churn. Mitigation: Wave 4 WI-11 is a single mechanical PR (frontmatter-only, ~17 files × 3 lines each). Low review cost.
- **Negative:** `last_audited` must be maintained; a forgotten bump silently ages a file. Mitigation: the CI warning provides the nudge; `plugin-dev:skill-reviewer` can be extended to refresh the date as part of its review protocol (a future small backlog).
- **Negative:** If the Skill tool's frontmatter schema validator is strict, unknown fields could error. **Risk mitigation**: NDOC-02 (PRD Section 2.11) flagged that no authoritative doc confirms the frontmatter contract on 4.7. WI-03 (Wave-1 blocker) fetches the current Skill tool frontmatter reference and records a binary verdict. If the verdict is "unknown fields accepted" (the expected historical behaviour), Option A ships as-written. If the verdict is "strict," this ADR's Decision is revoked and replaced by Option B (HTML comment block below frontmatter) via the rollback trigger in the metadata block above — no further ADR re-authoring needed; same semantics, different placement. The rollback criterion is mechanical: WI-03's verdict string drives the branch.

## Alternatives Considered

- **Option B (comment block below frontmatter).** Rejected as primary; held as contingency if frontmatter validation turns out to be strict (see NDOC-02 spike). Comments are less scannable and not machine-queryable via `yq`.
- **Option C (filename convention).** Rejected outright — breaks the manifest, violates PRD Constraint 2.
- **Option D (sidecar metadata file).** Rejected — introduces a new surface per SKILL.md with no existing precedent. Doubles the file count without proportional clarity gain.
- **No marker at all.** Rejected: DX-M1 and DX-M4 baselines are infinite / 17 respectively — Galadriel's evidence that the current state is undiagnosable.

## Implementation Notes

- **Pre-requisite spike (Wave 1 addendum):** WebFetch the current SKILL.md frontmatter contract page (NDOC-02, challenger loop2 Finding #8). If unknown fields are permitted (expected), proceed with Option A. If not, fall back to Option B (HTML comment block `<!-- model_awareness: opus-4-7 -->` etc.) — same semantics, different placement.
- **Wave 3 per-keystone edit:** include the three fields as part of the prose-edit commit. Do not split into a separate commit — locality of change makes the header meaningful alongside the prose it advertises.
- **Wave 4 backfill (WI-11):** non-keystone SKILL.md files (rule-derived set per plan §6.1 WI-11 — currently 11 files, `{scope-baseline §4 inventory} \ {six keystones}`) each gain the three fields via a single PR. Ordered after all prose edits so `last_audited` dates reflect the actual review state. Backfill files stamp `model_awareness: opus-4-7-frontmatter-only` (not `opus-4-7`) — the honest two-tier tag distinguishes mechanical backfill from prose-reviewed keystones (fresh-challenger F-C-08 priority #3).
- **Date hygiene:** `last_audited` on a file edited in Wave 3 is set to the Wave 3 edit date, not the original authoring date. On a Wave 4 backfill file (no prose edit), `last_audited` is set to the backfill date with a note "frontmatter-only; no prose review performed."

---

*"A thing that does not announce its era is a thing that will be dated wrongly by the first passer-by. Inscribe the year on the ring's inside; the wearer need not see it, but the inscriber always shall."*

— Celebrimbor
