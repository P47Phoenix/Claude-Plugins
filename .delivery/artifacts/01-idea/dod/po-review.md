# PO DoD Review -- Stage 1 Idea (Paired Constraints Primitive)

**Validator**: Gandalf (Product Owner) | **Date**: 2026-04-08
**Artifact**: `.delivery/artifacts/01-idea/po/idea-brief.md`
**Scope**: BACKLOG-001 paired with BACKLOG-004

> *"I have looked into the brief, and I have not found it wanting."*

## Gate Criteria Assessment

1. **Concrete problem with cited evidence** -- PASS. Four burdens, each anchored to a file and line: `plan.md` 57% first-try pass baseline, `architect-examine-decomposition-gaps.md` Gaps 1-3, `pipeline-stages.md:428-449`. Stones, not rumor.
2. **Distilled vision, not a PRD** -- PASS. Section 2 names the primitive (`constraints.yml`, <=8 fields) and the two domains without prescribing schema fields, validator code, or acceptance tests. Those await Refine, as they should.
3. **Explicit IN/OUT scope** -- PASS. Seven IN items, six OUT items, each named by backlog id or artifact. BACKLOG-005, BACKLOG-003, BACKLOG-006, MAR pilot, broad rewrites, and v2.8 bump are all explicitly excluded.
4. **Measurable success with baselines** -- PASS. Five of six stakes carry numeric thresholds or binary checks; Plan pass-rate stake cites baseline 57% -> target >=80% over 5 runs. Stakes 2-6 are deterministically verifiable.
5. **Anti-scope prevents drift** -- PASS. Section 5 forestalls the six most probable scope expansions (paradigm restructure, new collab patterns, broad rewrites, permanent opt-in flag, schema bump, pipeline bypass). Discipline over ambition, named.
6. **Real backlog + gap evidence, no fabrication** -- PASS. BACKLOG-001 and BACKLOG-004 named as paired sources; Architect examination and PO synthesis/revision memos cited as inputs. Cross-checked: the cited files are consistent with prior work in this repo's memory trail.
7. **No implementation leakage** -- PASS. The brief names *what* (shared schema, Golden Rule invariant, banned-token lint, Architect-in-Plan wiring) without prescribing *how* (no field list, no matcher algorithm, no hook wiring code). The banned-token set quoted in Section 2 is quoting the Architect examination's evidence, not designing the lint -- acceptable at Idea depth.

## Counsel for Downstream Stages

- **Refine**: pin the <=8 field budget as a hard contract; schema creep is the predictable failure mode. Turn the six stakes into explicit AC. Make the 5-run dogfood window a P0 UAT gate, not a soft aspiration.
- **Design**: lay the two domain templates side-by-side so divergence is visible at a glance.
- **Architect (light)**: do not re-open "which gaps" -- the three Architect-confirmed gaps are locked. Focus on Stage 5 invocation wiring and the installed<->source sync boundary.
- **Plan**: Architect must be a named participant producing `sequencing.md`; verify on the dogfood run.

## Verdict

The seed is well-formed: named burden, bounded reach, measured stakes, counselled against its own drift. Stage 2 may plant it.

```
STATUS: DONE
ARTIFACT: .delivery/artifacts/01-idea/dod/po-review.md
SUMMARY: The brief is measured, bounded, and evidence-bound -- pass through the gate, the road to Refine is open.
```
