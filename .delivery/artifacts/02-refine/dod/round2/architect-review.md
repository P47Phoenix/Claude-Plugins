# Architect DoD Review (Round 2) — Stage 2 Refine (PRD: Update Claude-Plugins Skills for Claude Opus 4.7)

**Reviewer**: Celebrimbor, Master Smith of Eregion
**Artifact**: `.delivery/artifacts/02-refine/po/prd.md` (rev 2)
**Companion inventory**: `.delivery/artifacts/02-refine/data/scope-baseline.md` (Elrond)
**Round 1 verdict (self)**: DONE — `.delivery/artifacts/02-refine/dod/architect-review.md`
**Round 2 reviewer inputs to verify did not regress architectural inputs**: DEV-01 (regex fix in AC-01.4 / M-01), DEV-02 (alias path correction in AC-05.1 / AC-05.2 / M-05 / R-03), DEV-03 (`parallel_validators` boolean-vs-count correction in AC-03.3 / AC-09.1 / M-03 / R-02 / §3.8)
**Stage**: 2 / Refine — DoD gate round 2 before Stage 4 transformation-planning
**Date**: 2026-04-20

> *"A second inspection is no insult to the first. The smith who refuses to reweigh his ore after a new measure is not a smith but a stubborn man with a hammer. Let us weigh again — and where the measure is truer, record it so."*

---

## Summary

Revision 2 applies three targeted developer corrections (DEV-01 / DEV-02 / DEV-03) without disturbing the architectural inputs I signed off in round 1. All three fixes are **tightenings**, not scope shifts: the regex now actually matches MID-01, the alias-theme path now points to real files with real marker fields, and the validator-count source is now anchored to a key that exists in the frozen v2.7 schema (`dod_validators`) rather than a boolean flag misread as a count. I verified each claim against the live repo.

No gate criterion that passed in round 1 weakens in round 2. No new architectural inputs need to be added for this stage. I find zero blocking issues and three small observations, all resolvable inside the Architect stage.

**Round 2 verdict: DONE.**

---

## Per-Criterion Table

| # | Criterion | R1 Verdict | R2 Verdict | Rev-2 impact (did rev-2 weaken this criterion?) |
|---|---|---|---|---|
| 1 | AS-IS feasibility | PASS | **PASS** | Strengthened. DEV-02's path correction makes R-03's affected-file column point to files that actually exist (`delivery-team/skills/delivery-flow/references/aliases/*.yml`). AS-IS can now target the right artefacts without me re-discovering them. |
| 2 | TO-BE guidance | PASS | **PASS** | Unchanged. No rev-2 edit touches the 4.6→4.7 delta statements (F-01..F-29) or REQ intents. |
| 3 | Roadmap inputs present | PASS | **PASS** | Strengthened. DEV-03's correction gives me a concrete per-stage expected-count table (`idea`=2, `refine`=4, `design`=5, `architect`=5, `plan`=5, `development`=4, `uat`=4) I can use directly in Phase 3 sequencing. Sizing hints and dependencies unchanged. |
| 4 | Technical correctness of research findings | PASS (one note) | **PASS** | Unchanged. The F-09 attribution note from R1 remains resolvable in AS-IS; nothing in rev-2 touched Section 2. |
| 5 | Cross-cutting signals | PASS | **PASS** | Unchanged. Cross-cutting scope (REQ-02 six-file keystone audit, REQ-08 plugin-dev routing) intact. |
| 6 | Risk surface usable | PASS | **PASS** | Strengthened. R-02's affected-file column now correctly names `.delivery/config.yml` `dod_validators.<stage>` as the measurement source; R-03's column now points at real theme YAML paths. I can plan mitigations against the right artefacts. |
| 7 | Constraint completeness | PASS | **PASS** | Strengthened. DEV-03's correction **preserves** Constraint 5 (schema v2.7 frozen): the fix re-points to an existing key rather than proposing a new one. Nine-constraint enumeration intact. |
| 8 | Open Questions answerable in Architect stage | PASS | **PASS** | Unchanged. All eight OQs still resolvable within Architect stage. |
| 9 | **No round-2 regressions** (new criterion) | — | **PASS** | Verified below: each DEV-fix narrows scope or corrects a wrong referent — none broaden scope, loosen criteria, or remove an architectural input. |

**Overall: 8/8 prior criteria hold at PASS. Criterion 9 (no regression) PASS.**

---

## Findings

### 1. DEV-01 regex fix (AC-01.4 / M-01) — verified correct

**Claim (PRD rev 2):** The old regex `claude-(opus|sonnet|haiku)-[0-9](\.[0-9])?-[0-9]{8}` required a literal `.` between major and minor digits, so it silently failed to match MID-01's ID `claude-sonnet-4-5-20250929` (which uses `-` as the major/minor separator). The new regex `claude-(opus|sonnet|haiku)-[0-9]([.-][0-9])?-[0-9]{8}` accepts either `.` or `-` and matches all three MID lines. "Verified 2026-04-20: returns 3 hits."

**My verification (run just now):**

```
$ grep -rnE 'claude-(opus|sonnet|haiku)-[0-9]([.-][0-9])?-[0-9]{8}' \
    --include='*.py' --include='*.json' --include='*.md' --include='*.yml' --include='*.yaml' \
    --exclude='*.db' --exclude-dir=.delivery --exclude-dir=.git --exclude-dir=__pycache__ \
    agentic-flow-builder/ prd-quality-gate-flow/ \
  | grep -v 'claude-haiku-4-5-20251001' | wc -l
3
```

Three matches, at exactly the line numbers the PRD claims:
- `agentic-flow-builder/scripts/agent_registry.py:148` → MID-01 (`claude-sonnet-4-5-20250929`)
- `agentic-flow-builder/scripts/agent_registry.py:172` → MID-02 (`claude-haiku-4-20250514`)
- `agentic-flow-builder/scripts/agent_registry.py:187` → MID-03 (`claude-opus-4-20250514`)

The rev-2 regex matches the baseline stated in M-01 and the hits named in AC-01.4. The allowlist exclusion (`grep -v 'claude-haiku-4-5-20251001'`) correctly preserves the single currently-canonical dated ID as the only non-stale dated reference. The `*.db` and `.delivery/` exclusions are intact per Section 3.9 and Constraint 4.

**Architectural impact of DEV-01 fix:** Neutral-to-positive. The regression guard in M-01 now actually guards. My round-1 finding that the complement-of-allowlist construction is sound still stands; it is the *regex body* that was too tight, and that is now correct.

### 2. DEV-02 alias path correction (AC-05.1 / AC-05.2 / M-05 / R-03) — verified correct

**Claim (PRD rev 2):** The previous alias-creator references pointed at `alias-creator/references/*theme*.md`, which holds only `theme-format.md` — a schema document, not per-theme content. Per-theme voice lives in `delivery-team/skills/delivery-flow/references/aliases/<theme>.yml` (13 YAML files), each carrying `roles[].catchphrase` and `roles[].examples[]` fields which are the extractable marker source.

**My verification:**

```
$ ls delivery-team/skills/delivery-flow/references/aliases/
breaking-bad.yml  bulls-jordan.yml  business.yml  dilbert.yml  funny.yml
lotr.yml  mandalorian.yml  marvel.yml  mtg.yml  nfl.yml
snl.yml  star-wars.yml  the-office.yml
```

13 YAML files, matching the enumeration in AC-05.1. Spot-read `lotr.yml` confirms the `roles[].catchphrase` + `roles[].examples[]` structure is real and populated (e.g., Gandalf / product-owner has a catchphrase plus two example lines). The marker-extraction command (`yq '.roles[].catchphrase' ...`) is executable against this structure.

**Architectural impact of DEV-02 fix:** Strengthens R-03's usability. Before the fix, the mitigation would have targeted a schema file that carries no voice markers — the dogfood run would have been uninterpretable. After the fix, R-03 points at the actual content surface, and M-05's ≥80% × ≥50% threshold can be measured by a tiny marker-match script as advertised. `alias-creator/SKILL.md` is correctly kept out of scope (it defines the format; it does not host per-theme content) — this preserves scope discipline. No architectural input weakens.

### 3. DEV-03 validator-set source correction (AC-03.3 / AC-09.1 / M-03 / R-02 / §3.8) — verified correct and preserves Constraint 5

**Claim (PRD rev 2):** `parallel_validators` in `.delivery/config.yml` was incorrectly treated as an integer count in rev 1. It is in fact a boolean flag that toggles parallel-vs-serial execution. The expected-count source is the per-stage list under `dod_validators.<stage>`, and its length equals the number of expected validator dispatches.

**My verification against live config:**

```yaml
pipeline:
  ...
  parallel_validators: true          # boolean flag — confirmed
  ...
dod_validators:
  idea: [po, architect]              # length 2
  refine: [po, architect, developer, qa]            # length 4
  design: [ux, po, qa, developer, architect]        # length 5
  architect: [architect, qa, developer, devops, security]  # length 5
  plan: [sm, po, qa, developer, devops]             # length 5
  development: [developer, qa, architect, tech-writer]     # length 4
  uat: [qa, devops, po, tech-writer]                # length 4
```

All seven per-stage counts match the numbers stated in AC-09.1. The fix is sound.

**Architectural impact of DEV-03 fix:** Strengthens three risk/metric rows and — critically — **preserves Constraint 5** (config schema v2.7 frozen). Rev 2 introduces no new config key; it re-points to an existing key that has been in the schema since v2.7. A less careful fix could have proposed a new `expected_validator_count` key, which would have violated Constraint 5 and required a schema version bump. That Gandalf avoided this trap is the kind of detail I look for.

M-03 and AC-03.3 pairing of *dispatch count* with *first-attempt hit rate* still closes the silent-fusion gap (F-08): neither signal alone would catch silent role-fusion, but dispatch-count-less-than-expected plus hit-rate-holding-at-100%-of-dispatched would make the fusion unambiguous. That pairing logic was already in rev 1 and survives rev 2 intact.

### 4. R-08 Contingency section — unchanged, still structurally sound

Rev 2 did not touch R-08. I note here only that the "Contingency — Dogfood Findings" section with placeholder ID remains the correct structural answer to the late-stage regression risk (stages not yet fired on 4.7). My round-1 observation #2 about sequencing REQ-09 first in Phase 1A carries forward.

### 5. MID-04 resolver question — unchanged, still Phase-1B scope

Rev 2 did not touch the MID-04 resolver question. It remains a Phase 1B Structural AS-IS task per OQ-3 and UV-01, and my round-1 observation #3 carries forward.

### 6. No-regression check across all rev-1 strengths — confirmed

I re-read every section rev 2 touched with an eye for silent weakening:
- **AC-01.2 re-scoping of MID-03 as drift-hygiene** (rev 1 per Challenger C-01) — intact in rev 2.
- **Keystone set of six files** (rev 1 per Challenger C-02 / C-03) — intact in rev 2.
- **REQ-10 baseline capture** (rev 1 per QA DEF-08) — intact in rev 2; AC-10.2 still references the metrics that the DEV-fixes touch.
- **Concrete checklist for adversarial output** (rev 1 per QA DEF-03, M-04) — intact in rev 2.
- **R-05 re-scored Low/Low** (rev 1 per Challenger C-01 / C-07) — intact in rev 2.
- **Section 3.1.1 SDK-import verification** — intact in rev 2.
- **Constraints 1–9** — intact in rev 2; Constraint 5 *preserved* by DEV-03 as noted above.
- **Open Questions 1–8** — intact in rev 2.
- **Revision-history table** — rev 2 adds a "Revision Log" subsection enumerating DEV-01/02/03 fixes; this is additive documentation, not a change to prior entries.

Zero rev-1 strengths are weakened by rev-2 changes.

---

## Overall Verdict

**DONE.**

The PRD (rev 2) remains architecturally ready. The three developer corrections are all tightenings: a regex that now matches what it claimed to match, a path that now points at the files that actually carry the content in question, and a config-key reference that now names a key that actually exists in the frozen schema. None of them touched the TO-BE intent, the keystone classification, the risk set, or the constraint set.

I can produce Phase 1A Behavioral AS-IS, Phase 1B Structural AS-IS, Phase 2 TO-BE, and Phase 3 Roadmap against this intake without further revision.

The transformation-planning sub-workflow may proceed.

— **Celebrimbor**, Solution Architect (Round 2)
