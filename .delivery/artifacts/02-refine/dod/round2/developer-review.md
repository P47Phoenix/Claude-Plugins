# Developer DoD Review — PRD (Refine stage), Round 2

**Artifact under review**: `.delivery/artifacts/02-refine/po/prd.md` (rev 1 + Rev 2 DoD patches)
**Reviewer**: Developer (alias **Gimli**, DoD round 2)
**Date**: 2026-04-20
**Round-1 artifact**: `.delivery/artifacts/02-refine/dod/developer-review.md` (3 concrete defects)

---

> *"Hmmf. The fellowship came back with their tools sharpened. Axe is axe; I'll swing it on the rock and see if the rock yields. Talk is cheap — grep is cheaper."*

The three fixes were testable claims, and I tested them. All three hold. The PRD is shippable from a developer's standpoint.

---

## Summary

Round 1 flagged three concrete, verifiable bugs:

- **DEV-01**: AC-01.4 regex missed MID-01 (`claude-sonnet-4-5-20250929`) because the middle separator was `\.` only.
- **DEV-02**: AC-05.1 / M-05 / R-03 pointed at `alias-creator/references/*theme*.md`, a path that holds only the schema doc. Per-theme personality content lives under `delivery-team/skills/delivery-flow/references/aliases/<theme>.yml`.
- **DEV-03**: AC-03.3 / AC-09.1 / M-03 / R-02 treated `pipeline.parallel_validators` as an integer count. It is a boolean toggle. The real expected-count source is `.delivery/config.yml` `dod_validators.<stage>` list length.

Rev 2 of the PRD ships patches for all three. I reproduced the commands from the revised PRD against the live repo. **All three patches hold.**

Two secondary observations that don't block shipping but Architect should note:

- The `yq` invocation in AC-05.1 (`yq '.roles[].catchphrase' ...`) works on go-yq because `.[]` iterates object values as well as array elements — but `roles` is a map keyed by role name, not a list. Go-yq handles it. If anyone tries with jq-flavoured `.roles[]` syntax, they'd need `.roles[]` to be aware they're iterating a map. Not a defect in the PRD (the command is correct), noting for downstream.
- One note in §3.9 says 21 row-level copies in `prd_flows.db`. I did not re-verify that number (not a round-1 finding). Architect's Phase 1B structural AS-IS will naturally touch it.

**Verdict: DONE.** Round-2 gate passes.

---

## Per-criterion table

| # | Criterion | Verdict | Rev-2 notes |
|---|-----------|---------|-------------|
| 1 | Implementability | PASS | Every REQ still resolves to a concrete file path + line or command. No abstractions snuck in during rev 2. |
| 2 | AC commands valid (run them) | PASS | REQ-01 AC-01.4 regex → 3 hits (expected). REQ-03 AC-03.3 / REQ-09 AC-09.1 counts match `dod_validators.<stage>` list lengths exactly. REQ-05 AC-05.1 path + field shape confirmed against `lotr.yml`. All three previously-broken commands now execute and return the documented counts. |
| 3 | Scope grounding | PASS | Every REQ still traces to a Section 2 Finding (F-01..F-29) or a Section 3 inventory line (MID-01..04, PAT-01..07, DISP-01..03, SZ-01..17, HK-01..07). Rev 2 didn't introduce new scope; it corrected existing pointers. |
| 4 | No silent refactors | PASS | REQ-03 still additive (AC-03.1). REQ-05 still spot-sample (AC-05.1 names "3 themes", not all 13). REQ-02 still a read + list, not a rewrite. No REQ upgraded to "rewrite" in rev 2. |
| 5 | Keystone realism | PASS | Six-file keystone set (rev 1) preserved. Rev 2 did not add or remove keystones; it corrected the commands that probe them. |
| 6 | CLAUDE.md compliance | PASS | REQ-08 still stipulates `plugin-dev:*` routing. Constraint 5 still freezes schema v2.7. Rev 2 DEV-03 fix explicitly preserves Constraint 5 (uses existing key `dod_validators` rather than adding a new key). Open Question 8 still routes future SDK work through `claude-api` skill. |
| 7 | No forbidden patterns | PASS | No `CRITICAL:` / `You MUST` over-pressure introduced in rev 2 patches. Tone stayed within F-28 guidance. Non-goals intact. |
| 8 | Effort signal adequacy | PASS | Sizing hints (S/M/L) still live in the "PO sizing hypothesis" footers, still non-binding on Architect (per QA DEF-02 resolution carried into rev 2). No AC hides a sizing assertion. |
| 9 | Round-1 findings closed | PASS | All 3 verified by re-running the new commands — see evidence block below. |

---

## Verification evidence — round-1 findings re-run against live repo

### DEV-01 — AC-01.4 regex catches MID-01

**Revised command (from PRD §4 REQ-01 AC-01.4):**

```bash
grep -rnE 'claude-(opus|sonnet|haiku)-[0-9]([.-][0-9])?-[0-9]{8}' \
  --include='*.py' --include='*.json' --include='*.md' --include='*.yml' --include='*.yaml' \
  --exclude='*.db' --exclude-dir=.delivery --exclude-dir=.git --exclude-dir=__pycache__ \
  agentic-flow-builder/ prd-quality-gate-flow/ \
  | grep -v 'claude-haiku-4-5-20251001' \
  | wc -l
```

**Actual output (executed 2026-04-20 against working tree):**

```
3
```

**Detail (without `wc -l`):**

```
agentic-flow-builder/scripts/agent_registry.py:148:                "config": {"model": "claude-sonnet-4-5-20250929"},
agentic-flow-builder/scripts/agent_registry.py:172:                "config": {"model": "claude-haiku-4-20250514"},
agentic-flow-builder/scripts/agent_registry.py:187:                "config": {"model": "claude-opus-4-20250514"},
```

**Verdict:** Regex now matches all three target lines (MID-01 line 148, MID-02 line 172, MID-03 line 187). The middle character class `[.-]` correctly accepts the `-` separator in `claude-sonnet-4-5-20250929`. Pre-implementation baseline of **3** matches what M-01 states. The allowlist filter (`| grep -v 'claude-haiku-4-5-20251001'`) correctly preserves the canonical Haiku 4.5 ID (I confirmed no such line exists in this repo today, so the filter is defensive, not suppressing). **FIX HOLDS.**

### DEV-02 — AC-05.1 alias path

**Revised claim (from PRD §4 REQ-05 AC-05.1):** per-theme personality content lives in `delivery-team/skills/delivery-flow/references/aliases/<theme>.yml` and each theme file ships `roles[].catchphrase` + `roles[].examples[]`.

**Actual directory listing (executed 2026-04-20):**

```
breaking-bad.yml  dilbert.yml  lotr.yml       marvel.yml  nfl.yml    star-wars.yml
bulls-jordan.yml  funny.yml    mandalorian.yml mtg.yml     snl.yml    the-office.yml
business.yml
```

**Verdict on count:** 13 files, exactly as the revised PRD claims.

**Shape verification against `lotr.yml`:**

```
product-owner: catchphrase="A product owner is never late, nor early. They prioritize precisely wh..." examples=2
scrum-master: catchphrase="I do not know what strength is in my backlog, but I swear to you I wil..." examples=2
data-analyst: catchphrase="I was there three thousand sprints ago, when the metrics last failed...." examples=2
developer: catchphrase="And my code!..." examples=2
architect: catchphrase="Let us forge something that will endure beyond the ages...." examples=2
qa-engineer: catchphrase="That bug still only counts as one...." examples=2
devops: catchphrase="I can't deploy the feature for you, Mr. Frodo, but I can carry the pip..." examples=2
release-manager: catchphrase="I will ship the release, though I do not know the way...." examples=2
tech-writer: catchphrase="I think I'm quite ready for another documentation adventure...." examples=2
ux-designer: catchphrase="Instead of a dark UI, you would have a design beautiful and terrible a..." examples=2
ui-designer: catchphrase="I choose a mortal design -- and I will make it timeless...." examples=2
game-ui-designer: catchphrase="I see all. The player shall see only what they need...." examples=2
user-feedback: catchphrase="We don't know about architecture, but we know what we like...." examples=2
```

**Verdict:** Every role in `lotr.yml` carries both a `catchphrase` and a non-empty `examples` list (≥2). AC-05.1's marker-extraction contract ("at least 2 signature markers per role") is satisfiable from the file structure. M-05's ≥50%-markers definition is mechanically measurable. **FIX HOLDS.**

**Structural note (non-blocking):** `roles` is a YAML mapping (dict-keyed-by-role-name), not a sequence. The `yq '.roles[].catchphrase'` example in AC-05.1 works on go-yq (`.[]` on an object iterates values) but would need to be `.roles[].catchphrase` with map-aware semantics for jq-via-yj users. Not a PRD defect — the command as written is correct for standard go-yq. Flagging only so Architect picks the right tool in the implementation run.

### DEV-03 — AC-03.3 `parallel_validators` boolean vs count

**Revised claim (from PRD §4 REQ-03 AC-03.3 + §4 REQ-09 AC-09.1):** `pipeline.parallel_validators` is a boolean; the per-stage expected validator count comes from `.delivery/config.yml` `dod_validators.<stage>` list length; the specific expected counts are idea:2, refine:4, design:5, architect:5, plan:5, development:4, uat:4.

**Actual config shape (executed 2026-04-20 against `.delivery/config.yml`):**

```
pipeline.parallel_validators: True
type: bool

dod_validators keys: ['idea', 'refine', 'design', 'architect', 'plan', 'development', 'uat']
  idea: ['po', 'architect'] (len=2)
  refine: ['po', 'architect', 'developer', 'qa'] (len=4)
  design: ['ux', 'po', 'qa', 'developer', 'architect'] (len=5)
  architect: ['architect', 'qa', 'developer', 'devops', 'security'] (len=5)
  plan: ['sm', 'po', 'qa', 'developer', 'devops'] (len=5)
  development: ['developer', 'qa', 'architect', 'tech-writer'] (len=4)
  uat: ['qa', 'devops', 'po', 'tech-writer'] (len=4)
```

**Verdict:** `parallel_validators` is a Python `bool` (`True`), not an int. The seven stage counts enumerated in AC-09.1 (`idea:2, refine:4, design:5, architect:5, plan:5, development:4, uat:4`) match the live config byte-for-byte. M-03 now measures dispatch count against a real list, not a mis-named boolean. Constraint 5 (schema v2.7 frozen) is respected — no new key added; existing `dod_validators` key is used. **FIX HOLDS.**

---

## Findings

### Blocking findings

None.

### Non-blocking observations

- **OBS-01 (advisory, not a defect):** AC-05.1's `yq '.roles[].catchphrase' ...` command is correct for go-yq semantics on map values. If the implementation run happens to use jq-via-yj instead, the translator may emit `.roles | to_entries[] | .value.catchphrase`; Architect should note which tool the run uses. Not a PRD change.
- **OBS-02 (advisory, not a defect):** PRD §3.9 claims 21 row-level copies of family-alias strings in `prd_flows.db`. I did not re-verify this (not a round-1 finding and not load-bearing on any AC). Architect's Phase 1B structural AS-IS touches this naturally.
- **OBS-03 (advisory, positive):** Rev 2's Revision Log (lines 561–563) lists DEV-01/DEV-02/DEV-03 individually with before/after diffs — this level of traceability made verification mechanical, not interpretive. Carry this pattern forward.

---

## Verdict

**DONE.**

All three round-1 defects are closed by rev 2, verified against the live repo by re-running the revised commands. Scope and shape of the PRD otherwise unchanged. No new defects surfaced during round-2 re-read. The rock yielded; the axe is clean.

---

## Closing (Gimli, in character)

*"Rev 2 holds. The regex catches what it said it'd catch — three lines, named and numbered. The alias path points where the voices actually live — thirteen YAML files, each with catchphrases and examples by role. And `parallel_validators` is the boolean toggle my round-1 axe said it was, with the real counts sitting under `dod_validators` right where it belongs."*

*"Gandalf wrote the fixes and I swung the axe at each one. None dented. That is as much endorsement as a dwarf gives before first ale."*

**— Gimli, Developer DoD reviewer, round 2**
