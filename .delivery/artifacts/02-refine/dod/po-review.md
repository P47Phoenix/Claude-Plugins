<!-- run: run-2026-05-13-tk5 -->
# PO DoD Review — Stage 2 Refine (BACKLOG-106)

*Reviewer: Gandalf, Product Owner.*
*Pipeline: run-2026-05-13-tk5.*
*Scope: PRD + BACKLOG + constraints.yml against PO DoD gate criteria.*

> A product owner is never late, nor early. The probe is forged when the criteria are met.

## Verdict: **PASS** (8 / 8 gates green)

## Inputs reviewed

- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/02-refine/po/prd.md` (91 lines)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/backlog/BACKLOG-106-delivery-team-smoke-test.md` (202 lines)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/02-refine/po/constraints.yml` (51 lines)
- `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/artifacts/01-idea/_input/user-seed.md` (verbatim AC source)

## Verification commands run

- `wc -l` on PRD, BACKLOG, constraints.yml
- `grep -cE "^\s*-\s+\*\*US-[0-9]+\*\*: As a .+ I want .+ so that"` on PRD
- `grep -cE "^\s*-\s+\*\*AC-[0-9]+\*\*"` on PRD; `grep -cE "^[0-9]+\. "` on user-seed
- `python3 -c "import yaml; yaml.safe_load(open(...))"` on constraints.yml + BC-01 inspection
- `grep -nE "^### W6-[1-8] "` and `grep -nE "^\| W6-[1-8] \|"` on BACKLOG
- Python regex extraction of `## Out of Scope` blocks on PRD + BACKLOG
- `grep -niE "producer.?validator"` on PRD + BACKLOG

## Gate-by-gate

### Gate 1 — Business Value answers "why now?" — PASS

PRD `## Business Value` (line 8) names the live regression risk concretely:
- 5/5 token-economy waves shipped without an empirical end-to-end probe.
- Telemetry only populated when a pipeline is hand-run — no automatic answer to "is the team still building hello-world?" before the next plugin change.
- TARGET vs CURRENT framing (lines 14–16) makes the gap and the close-out explicit.

Not generic. The "why now" is "5 waves of token-economy / model-routing / prompt-template changes are about to compound — the next change is the moment to wire the probe."

### Gate 2 — ≥ 3 user stories `As a … I want … so that …` with real persona — PASS

Count via grep: **5** matching lines (PRD lines 20–24). Personas are specific, not generic:
- US-1, US-2, US-3: `plugin maintainer` / `maintainer`
- US-4: `contributor`
- US-5: `future plugin author`

All five preserve the canonical user-story grammar. None say bare "user".

### Gate 3 — Acceptance Criteria preserves all 8 user-seed ACs; AC-NN IDs present — PASS

- AC ID count in PRD (grep): **8** (AC-01 … AC-08, lines 39–46)
- Numbered ACs in user-seed `## Acceptance criteria (initiative-level)`: **8**
- Count equality: **8 == 8** (QA lesson applied — counted directly, not trusted from upstream)

Per-AC seed → PRD mapping:
- Seed-1 ↔ AC-01 — semantically identical.
- Seed-2 ↔ AC-02 — wording tightened ("Output:" → "Output written to"); content preserved.
- Seed-3 ↔ AC-03 — content preserved + path expansion (`telemetry.jsonl` → `.delivery/telemetry/skill-loads.jsonl`). All fields enumerated.
- Seed-4 ↔ AC-04 — preserved.
- Seed-5 ↔ AC-05 — preserved.
- Seed-6 ↔ AC-06 — preserved + amplified ("no Claude calls; complete in < 5 sec" added — both already implied in seed risk register and seed AC-1 wall-clock).
- Seed-7 ↔ AC-07 — preserved.
- Seed-8 ↔ AC-08 — preserved.

**Soft note (non-blocking)**: PRD ACs are semantic-verbatim, not byte-verbatim. Tightenings in AC-02, AC-03, AC-06 are editorial polish, not scope changes. No seed AC is dropped or weakened. PO accepts as in-scope Refine-stage editing.

### Gate 4 — constraints.yml parses; BC-01 local-only with memory-file `source` — PASS

- YAML parse via `python3 -c "import yaml; yaml.safe_load(…)"`: **OK**.
- BC-01 found in `binding_constraints[]`:
  - `id`: `BC-01`
  - `rule`: `NO .github/workflows/smoke-*.yml — claude CLI not available in CI runners`
  - `source`: `/home/meconnelly/.claude/projects/-var-home-meconnelly-Documents-GitHub-Claude-Plugins/memory/feedback_claude_code_local_only.md`
  - `bypass_allowed`: `false`

Source IS the binding memory file path. Local-only rule explicit and unbypassable.

### Gate 5 — BACKLOG-106 file present, line count 200–300 — PASS

- File exists at `/var/home/meconnelly/Documents/GitHub/Claude-Plugins/.delivery/backlog/BACKLOG-106-delivery-team-smoke-test.md`.
- `wc -l`: **202 lines**. In band [200, 300].

### Gate 6 — BACKLOG enumerates exactly 8 WIs W6-1 … W6-8 with file paths + effort — PASS

- H3 sections `### W6-[1-8] ` (grep): **8** (lines 29, 38, 44, 50, 56, 64, 72, 82).
- Table rows `| W6-N |` (lines 20–27): **8 rows**, each with surface column (explicit file paths) and effort column (M / S / M / S / M / S / M / S).
- File surfaces additionally enumerated in `## File Surface Inventory` table (lines 98–117) — 14 new files + 1 new-or-edit + 1 architect artifact.

### Gate 7 — Out-of-scope section present + CI workflows listed — PASS

Python regex extraction of `## Out of Scope` blocks:

**PRD (line 64)**:
```
- Hardware-team / mtg-commander / other-plugin smoke tests. (Factor `lib/` for reuse; build delivery-team's first.)
- CI workflows. (Banned by BC-01.)
- Cost-tracking dashboards beyond per-run report. (Future BACKLOG.)
- Tightening 2σ → tighter band before 20 accumulated production runs.
```

**BACKLOG (line 173)**:
```
- Hardware-team / mtg-commander / other-plugin smoke tests. Factor `lib/` for reuse; build delivery-team's first.
- CI workflows. Banned by BC-01.
- Cost-tracking dashboards beyond per-run report. Future BACKLOG.
- Tightening 2σ band before 20+ accumulated production runs.
```

Both list `CI workflows` as the second bullet, citing BC-01.

(Note: an initial `grep -i "CI|workflow"` scan returned no hits because `awk` over-truncated the section at the heading boundary itself; verified via Python regex on the full source.)

### Gate 8 — Producer-validator separation rule for meta-tests/baseline stated in PRD AND BACKLOG — PASS

**PRD (line 60, BC-03 in `## Constraints (binding)`)**:
> meta-test fault-injection fixtures CANNOT be authored by the same Stage-6 Dev dispatch that authors `lib/metrics.py` or `lib/baseline.py`. Binding from past waves; applies to validator-style artifacts. (Memory: producer-validator separation validated:5.)

**BACKLOG — 6 distinct hits** (lines 80, 147, 160, 161, 169, 191):
- Line 80 — W6-7 acceptance note tying rule to specific WIs (W6-2, W6-5).
- Line 147 — Risk register row with Scrum Bag owner.
- Lines 160–161 — Story decomposition labels Story 2 as Producer half, Story 3 as Validator half.
- Line 169 — BC-03 in `## Constraints` section.
- Line 191 — Stage 6 (Dev) handoff note: validator MUST NOT read producer's `lib/metrics.py` or `lib/baseline.py` source.

Rule is not buried — it is enforced structurally across WI acceptance, risks, decomposition, constraints, and handoff.

## Memory lessons applied

- **Developer-DoD lesson (10×)**: every claim verified by running the command (`wc -l`, `grep -cE`, `python3 -c "import yaml; …"`, Python regex extraction). No artifact text trusted on face.
- **QA coverage lesson (tk4 caught BACKLOG-104 had 10 ACs not 7)**: AC count enumerated by ID — 8 IDs counted in PRD, 8 numbered items counted in user-seed, equality verified manually. No upstream tally trusted.

## Open notes (non-blocking — for Stage 3+ awareness)

1. **AC tightening (Gate 3 soft note)**: PRD ACs are semantic-verbatim, not byte-verbatim. If downstream stages need strict byte-diff against user-seed (e.g., automated coverage matrix), the editorial deltas in AC-02, AC-03, AC-06 may warrant a one-line mapping artifact. PO accepts as-is for this Refine pass.
2. **Open Questions**: PRD line 76 declares "None blocking" — all 5 risks from user-seed `## Open risks` have mitigations cited. Confirmed seed↔PRD mapping is complete.

## Stop-rule status

Defects/story rolling rate = 0.111 (BACKLOG-106 line 8; user-seed line 70). Well under 0.4 threshold. Pipeline cleared to proceed to Stage 3 (Design).

— Gandalf, PO, run-2026-05-13-tk5. The probe is forged precisely when it means to be.
