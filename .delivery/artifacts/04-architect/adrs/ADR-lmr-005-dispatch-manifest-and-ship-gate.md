# ADR-lmr-005: Dispatch-manifest shape (OQ-4) and the ship gate

- **Status**: Proposed (flips to Accepted when Stage 4 DoD passes)
- **Date**: 2026-09-20
- **Run**: run-2026-05-28-o48m, BACKLOG-108
- **Owner**: Solution Architect (PRD FR-7.3, FR-7.4, AC-DISP, OQ-4; BINDING-5.1, BINDING-5.4; Architect DoD round-2 F5, F8; QA W5)

## Context

AC-DISP (PRD FR-7.4) enforces "One Role = One Sub-Agent" with one file per stage, `<stage>/dispatch-manifest.txt`: line 1 `expected_validators: N`, then `<role><TAB><agent-id>` per dispatch; N must equal the line count, roles distinct, agent ids distinct. Its `REQUIRED` stage list is the PRD's guess (`02-refine`, `04-architect`, `05-plan`, `06-development`) and the PRD invites the Architect to correct it (OQ-4). The PRD also asks where the `dod_validators` counts live.

Evidence gathered in this stage (commands and files read):
- `.delivery/config.yml` lines 56 to 63 hold the source of truth: `idea: [po, architect]`, `refine: [po, architect, developer, qa]`, `design: [ux, po, qa, developer, architect]`, `architect: [architect, qa, developer, devops, security]`, `plan: [sm, po, qa, developer, devops]`, `development: [developer, qa, architect, tech-writer]`, `uat: [qa, devops, po, tech-writer]`.
- `.delivery/state.md`: `stages_completed: [1, 2]`, `stages_skipped: [3]`, routing `idea: light, refine: light, design: skip, architect: light, plan: light, development: full, uat: full`.
- `delivery-flow/SKILL.md` (Depth Definitions, read): Light = "Primary agent only, blocking criteria only, reduced DoD (primary + 1 reviewer)". Yet Stage 2 in this run, routed light, ran four validators (`.delivery/artifacts/02-refine/dod/` holds po, architect, developer, qa reviews). So N for a light stage is "validators actually dispatched", bounded by the config list, not equal to it.
- Stage directory names: `delivery-flow/references/pipeline-stages.md` line 550 writes to `artifacts/06-dev`; this run's PRD ACs and `.delivery/artifacts/` use `06-development`; both directories exist, and `06-development/dod/` already holds files from earlier waves (`S1-S2-architect-review.md`, `S3-architect-review.md`, and others). Stage 7 uses `07-uat`.
- DoD rounds and per-story units: `02-refine/dod/` and `04-architect/dod/` hold `-r2` files (a role re-validates in a second round); `06-development/dod/` holds per-story groups (`S1-S2-*`, `S3-*`). The PRD format (roles distinct within one manifest) cannot describe a second round by the same role, nor seven stories.

## Decision

1. **REQUIRED stage directories** for AC-DISP in this run: `02-refine`, `04-architect`, `05-plan`, `06-development`, `07-uat`. Excluded with reason: `01-idea` (predates the manifest rule, PRD), `03-design` (skipped, `stages_skipped: [3]`). `07-uat` is added because UAT is routed `full`, has its own `dod_validators.uat`, and (per architecture.md section 6) ship happens after UAT passes. If the Plan stage instead ships before UAT, drop `07-uat` from the list and say so in the plan; the checker takes the list as data.
2. **Stage-to-config-key map**: `02-refine` to `refine`, `04-architect` to `architect`, `05-plan` to `plan`, `06-development` to `development`, `07-uat` to `uat`. The checker reads the list with a stdlib regex on `.delivery/config.yml` lines of the form `  <key>: [a, b, c]` (no YAML dependency, per BC-03).
3. **The development directory is `06-development` for this run.** The PRD ACs (AC-3.1 ledger, AC-4.4 `s5-separation.txt`, `smoke-streams/`) already hard-code it. The orchestrator's default of `06-dev` (pipeline-stages.md) is a reference-doc mismatch to log for a later wave; the Stage 6 dispatch prompts must state `06-development` explicitly. Stale earlier-wave files in `06-development/dod/` are not read by the checker (it reads only `dispatch-manifest*.txt`).
4. **Manifest = one DoD round of one unit.** File naming: the stage-level round is `dispatch-manifest.txt`; extra rounds and per-story units are `dispatch-manifest-<label>.txt` (`-r2`, `-S1`, `-S2`, and so on). The format inside stays exactly as the PRD wrote it.
5. **Checker rules** (extends the PRD script, same negative self-test approach): for each required stage the checker requires at least one `dispatch-manifest*.txt` (a stage with none is a violation, so absence cannot pass, as in the PRD); for `06-development` it requires one manifest per story S1 to S7 (`dispatch-manifest-S<k>.txt`; a story's producer dispatches are not validators and are not listed); each manifest passes the PRD's four checks (line 1 shape, `N == lines`, roles distinct, agent ids distinct) plus two more: every role is in the config list for that stage and `N <=` the list length (BINDING-5.4: never more dispatches than the list); and every agent id is unique across ALL manifests of the run (a reused agent across rounds is a fusion or a copy).
6. **Cross-check for authorship claims (QA W5)**: the AC-4.4 `Dispatch-Id` trailers in the S5 commits must each appear in the `06-development` manifest set (producer ids under a developer role in the S5 producer manifest, the validator id under the qa role), and `run_smoke.py` joins `lib/` in the producer path list so one commit cannot touch it together with the validator files. These are additions for the Plan stage to write as AC text.
7. **Base ref for pre-ship ACs** (Architect F8): the S1 developer records `base_sha=$(git merge-base main HEAD)` once, in `.delivery/artifacts/06-development/base-sha.txt`. AC-2.1, AC-2.5, AC-4.4 and AC-5.9b, which use the moving `main` ref, are evaluated against that SHA. If `main` has not advanced the result is identical; if it has, the line numbers named in AC-2.1 and the diff in AC-2.5 stay meaningful. The named source lines in AC-2.1 are properties of the base commit, not of whatever `main` is at ship time.
8. **Ship sequence** (S7, in this order, each output and exit status pasted into the S7 report): (0) pre-ship-only ACs (AC-2.1, AC-2.5, AC-4.4, AC-5.9b); (1) staging complete (guard scope includes untracked files, so order is irrelevant); (2) `python3 scripts/check_model_pins.py` strict: `guard-scope hits 0 files 0`, `exit=0`; (3) the canonical count equals the script's `--list` line count; (4) `python3 scripts/check_skill_budgets.py` exit 0; (5) AC-6.1 `MATCH` (ADR-lmr-001); (6) `AC-DISP`; then squash-rebase, ff-merge, `git push origin main`; afterwards `git rev-list --count origin/main..HEAD` prints 0 and the guard's push run on `main` is expected green. The step-2 output is the sole mechanical stop unless the optional `pre-push` hook (ADR-lmr-002 D8) is installed; the reviewer of the ship reads that line.
9. **SKILL.md edits after the baseline capture** invalidate what the baseline measured (Architect F8). By design the live capture is the LAST step before ship (architecture.md section 6), so no such edit is expected; if DoD rework touches a SKILL.md after the capture, either re-capture or record an explicit waiver in the S7 report.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Keep one manifest per stage (PRD as written) | Cannot describe a second DoD round or seven per-story units: roles repeat, so a correct run would fail AC-DISP (evidence: `-r2` files and `S1-S2-*` files above). |
| Allow repeated roles inside one manifest | Removes the very check (roles distinct) that detects a fused or duplicated dispatch. |
| Derive expected N from the config list only | Light stages legitimately dispatch fewer than the list (SKILL.md Light definition), and Stage 2 dispatched exactly the list; an equality rule would fail one of them. The bound is `N <= len(list)` and roles subset of the list. |
| Read `06-dev` per pipeline-stages.md | The PRD ACs and existing artifacts already use `06-development`; switching means rewriting AC paths. Logged as a reference-doc defect instead. |
| Parse config with PyYAML or `yq` | New dependency; BC-03 forbids it. |
| Branch protection or a server-side hook for the push | Out of scope (PRD section 10). |

## Consequences

- AC-DISP has more moving parts than the PRD's script: about 60 lines instead of 30. It still needs no dependency and carries a negative self-test.
- The S7 executor needs a manifest per story and per extra round; the orchestrator must write them as it dispatches, or the ship gate fails loudly. That is the intent.
- If the PO prefers the PRD's one-file-per-stage form, the minimum change is to make the manifest describe only the final passing round of the stage and to drop the per-story requirement for `06-development`; the ADR then drops rules 4 and 5's per-story clause. Rule 5's role and length bounds remain valid either way.

## Status rationale

Proposed until Stage 4 DoD passes; then Accepted.
