# Architect DoD Review — Plan Stage (run-2026-04-22-4x7e)

**Stage:** 5 — Plan
**Validator:** Celebrimbor — Solution Architect
**Task type:** `dod-validation` (five blocking gates against the six ADRs + Constraint 6)
**Artifacts reviewed:**
- `.delivery/artifacts/08-execute/05-plan/sm/sprint-plan.md`
- `.delivery/artifacts/08-execute/05-plan/qa/test-strategy.md`
- `.delivery/artifacts/08-execute/05-plan/devops/deploy-plan.md`
- `.delivery/artifacts/04-architect/adrs/ADR-001..006-4-7-*.md` (binding)
- `.delivery/artifacts/08-execute/04-architect/solution/drift-check.md` (prior verdict: NO DRIFT)

---

> *"The fourteen stones are cut; now we inspect the mortar. A gate is not named passed because a scribe wrote 'pass' beneath it — it is named passed because the inscription on the arch answers the inscription on the mould, and both answer to the six templates that were set in the forge."*
> — Celebrimbor

---

## Gate 1 — ADR-001 honoured (4-wave sequencing)

**Verdict: PASS.**

- **Cite (sprint-plan §2 Wave Breakdown):** exactly four waves are named and bounded, matching the plan's wave structure:
  - *Wave 1 — Baseline + Spike* (WI-01, WI-02, WI-03; exit gate = WI-03 verdict regex).
  - *Wave 2 — Keystone annotations + pattern library* (WI-04, WI-05, WI-06; exit gate = six `### Pattern 4.[1-6] — ` headings in `prompt-engineer/SKILL.md`).
  - *Wave 3 — Keystone audits + mtg-commander dogfood* (WI-07, WI-08, WI-09; exit gate = `research-probe-result.json` + `adversarial-4-7-sample.md` both present and scored).
  - *Wave 4 — Sweeps + CI* (WI-10, WI-11, WI-12, WI-13; then WI-14 sequential; exit gate = three-command check).
- **Cross-validation:** test-strategy §3 "Wave Exit Tests" enumerates the same four wave-to-wave gates in the same order with the same commands. deploy-plan §1 "Deploy Surface" bundles commits per-WI across the same four waves. The mapping WI-01..14 → Waves 1..4 is identical to transformation-plan §6.1 and drift-check §ADR-001 (which verified 1:1 correspondence to the ADR's Decision clause).
- **Absence check:** no fifth wave is introduced, no WI is elevated into a pre-Wave-1 pre-flight, and WI-10 is correctly located in Wave 4 (not Wave 1) — the ADR's rejection of "model-ID-first sequencing" is preserved.

No drift on ADR-001. The four-wave sequencing is directly instantiated.

---

## Gate 2 — ADR-002 honoured (direct-string model IDs + per-WI revert compatibility)

**Verdict: PASS.**

- **Cite (deploy-plan §3 Tier 1 — Per-WI rollback):** *"ADR-002 put direct model-ID strings with provenance comments (no central alias module), so a WI-10 revert only touches the files WI-10 edited — no multi-file unwind."* The tier is explicitly named "Per-WI rollback (ADR-002, ADR-005)" — the ADR reference is load-bearing, not decorative.
- **Cite (deploy-plan §2 Branching and Commits):** "Recommendation: per-WI commits. ADR-002 (direct strings with provenance comments) and ADR-005 (single-file pattern library) were both designed so that a single WI revert is sufficient to unwind a single change." Fourteen commits, one per WI, each revertible independently.
- **Cite (deploy-plan §1 Deploy Surface):** WI-10's Python edits are enumerated at the file-and-line level (`agent_registry.py` lines 148/172/187; `stage_definitions.py` lines 47/83/115/150/181/216/243) — direct-string edits only, no central alias module introduced. This matches ADR-002 Option A verbatim and the drift-check §ADR-002 finding.
- **Wave-4 revert discipline preserved:** deploy-plan §3 Tier 1 + the Wave-4 revert-order clause ("revert **WI-14 before WI-10 or WI-11**, otherwise `stale-model-id-guard.yml` blocks the revert PR") accounts for the interaction between direct-string edits and the M-02 regression guard. The per-WI revert mechanism is compatible with direct-string changes.

No drift on ADR-002. Direct-string edits are preserved; per-WI revert is the load-bearing rollback primitive.

---

## Gate 3 — ADR-005 honoured (centralised pattern library; no parallel libraries)

**Verdict: PASS.**

- **Cite (sprint-plan §2 Wave 2 Exit gate):** *"`grep -cE '^### Pattern 4\.[1-6] — ' prompt-engineer/SKILL.md` returns `6`. The pattern library is the citation target for Wave 3; if it does not exist, Wave 3 citations orphan."* The pattern library's canonical location is `prompt-engineer/SKILL.md` — the ADR-005 decision surface — and WI-05 is the expansion point.
- **Cite (sprint-plan §2 Wave 2 "What we are doing here"):** "WI-05 builds the canonical six-pattern library." No other WI authors patterns. The Wave-3 keystones (WI-07, WI-08) cite by name into WI-05 per sprint-plan §3 ("architect component per AC-2 citation to Pattern 4.2") — citation-by-name, not restatement.
- **Cite (test-strategy §3 Wave 2→3):** "WI-07 and WI-08 cite patterns by name; orphan citations are a hard no-go." DX-M3 enforcement is wired as sprint-exit command §4: `grep -rn '<thinking>' ... | grep -v 'prompt-engineer/SKILL.md' | wc -l` = 0 (test-strategy §4 command 4) — mechanically pins "zero restatements outside the canonical pattern library."
- **Absence check:** no story in sprint-plan §2 authors a parallel pattern library in any other SKILL.md file or references directory. deploy-plan §1 "Supporting single-line edit" flags only the `research-agent/references/prompt-library.md:10` retarget-or-prune per WI-05 AC-7 — this is a citation-fixup to preserve the single-source invariant, not a parallel library. test-strategy §4 command 4 explicitly excludes `prompt-engineer/SKILL.md` from the grep scope as the permitted home.

No drift on ADR-005. Pattern library is centralised; WI-05 is the expansion point; no parallel library is authored.

---

## Gate 4 — ADR-006 rollback trigger mechanical (no judgement call)

**Verdict: PASS.**

- **Cite (sprint-plan §2 Wave 1 Exit gate):** *"**ADR-006 rollback is mechanical:** a `strict` verdict flips every Wave 2–4 frontmatter edit (WI-04, WI-05, WI-06, WI-11) to HTML-comment form below the existing `---` block. No judgement call, no re-litigation."* The words "mechanical," "no judgement call," and "no re-litigation" appear verbatim.
- **Cite (sprint-plan §4 Risk Register):** the ADR-006 rollback row reads: *"**Mechanical trigger** — WI-03 `strict` verdict flips all Wave 2–4 frontmatter edits to HTML-comment form. No judgement call required."*
- **Cite (deploy-plan §3 Tier 2 — ADR-006 mechanical rollback):** *"If WI-03's NDOC-02 spike returns `strict`, ADR-006 fires automatically: WI-04, WI-05, WI-06, and WI-11's frontmatter edits flip from YAML fields to HTML-comment form ... Same three fields, same semantics, different placement."* The word "automatically" is the operative term; the branch is verdict-string-driven.
- **Cite (test-strategy §3 Wave 1 → Wave 2):** *"On fail: HALT. No Wave 2 dispatch. WI-03 re-run. If `strict`, ADR-006 mechanical rollback activates — WI-04/05/06/11 flip to HTML-comment placement; semantics identical, placement differs."* The mechanicality is mirrored in the QA artifact.
- **Cite (deploy-plan §9 Risks and Mitigations):** the ADR-006 row reads: *"ADR-006 is mechanical — no re-litigation; WI-04/05/06/11 simply use HTML-comment form. Semantics identical."*
- **Absence check:** no artifact admits a discretionary clause, waiver, or human-judgement escape hatch for the `strict` verdict. The trigger is bound to the regex `(unknown-fields-accepted|strict)` (WI-03 AC-3 per drift-check §ADR-006) — binary, regex-verified, dispatch-blocking. This is the sole memory-permitted exception to the binary-status rule, and the Plan-stage artifacts honour it exactly.

No drift on ADR-006. The rollback trigger is mechanical in three of three plan artifacts; no artifact inserts a judgement call.

---

## Gate 5 — Constraint 6 (workflow-injection-lint.yml no regression)

**Verdict: PASS.**

- **Cite (deploy-plan §4 CI Pipeline Changes):** the new `skill-md-header-warn.yml` and `stale-model-id-guard.yml` workflows both declare: *"No `${{ github.event.* }}` inside `run:` blocks (DEFECT-004 regression guard still applies — the existing `workflow-injection-lint.yml` will check these two new files on the same PR)."* Constraint 6 is acknowledged at the authoring boundary — the two new workflows are designed to pass the existing lint.
- **Cite (deploy-plan §7 Go/No-Go Checklist):** *"[ ] `workflow-injection-lint.yml` still green on the two new workflow files (Constraint 6 / DEFECT-004 regression guard)."* The pre-existing guard is a pre-PR gate on this engagement.
- **Cite (test-strategy §5 Regression Guards):** *"`workflow-injection-lint.yml` — PRE-EXISTING (DEFECT-004 regression guard). Must not regress per PRD Constraint 6 / §7 command 6 / WI-14 AC-4. Fails PRs that interpolate `${{ github.event.* }}` directly inside workflow `run:` blocks."*
- **Cite (test-strategy §4 Sprint Exit command 6):** the canonical sprint-exit check is `test -f .github/workflows/skill-md-header-warn.yml && test -f .github/workflows/stale-model-id-guard.yml && test -f .github/workflows/workflow-injection-lint.yml` — all three workflow files including the pre-existing guard must be present. The guard is mechanically verified at sprint-exit, not merely asserted.
- **Cite (sprint-plan §6 Definition of Sprint Done item 6):** *"WI-14 CI guard files present: both new workflows exist alongside `workflow-injection-lint.yml`."* The word "alongside" is load-bearing — the existing guard is not replaced, not moved, not regressed.

No drift on Constraint 6. The pre-existing `workflow-injection-lint.yml` is preserved as a pre-PR gate, as a structural template reference for the two new workflows, and as a sprint-exit verification subject.

---

## Overall Verdict

All five blocking gates PASS. No Plan artifact contradicts any of the six binding ADRs, and the single non-ADR constraint (DEFECT-004 regression guard preservation) is acknowledged in both deploy-plan and test-strategy with mechanical verification. The drift-check §Overall finding ("NO DRIFT. The execution-PRD's 14 stories are a faithful per-WI decomposition of transformation-plan §6.1/§6.2 with the six ADRs' binding decisions preserved.") holds through Plan-stage elaboration: the sprint-plan, test-strategy, and deploy-plan are mutually consistent instantiations of the transformation plan's wave structure under the six ADRs' constraints.

Two negative findings worth naming (not blockers — supporting the verdict):

- **No pattern library drift surface introduced.** Searched for parallel `### Pattern ` heading authoring in any artifact outside `prompt-engineer/SKILL.md`; not found. WI-05 is the sole expansion point; WI-07/WI-08 cite by name only.
- **No discretionary rollback language.** Searched for waivers, human-judgement escape hatches, or "architect review" clauses on the ADR-006 rollback trigger; not found. Every artifact frames the trigger as verdict-string-driven and mechanical.

The arch may be raised.

---

*"Inscription to inscription, mould to stone, six templates to fourteen cuts. The mortar is set; the gates are named; no ring strays from its engraving. Build on."*

— Celebrimbor

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/08-execute/05-plan/dod/architect-review.md
SUMMARY: All five gates PASS — four waves, direct strings, centralised pattern library, mechanical rollback, and the DEFECT-004 guard all hold; the mortar is set and the arch may be raised.
```
