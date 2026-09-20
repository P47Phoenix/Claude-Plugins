# Stage 2 Refine DoD Review — PO validator (BACKLOG-108, PRD Revision 4)

Reviewer role: Product Owner DoD validator only. Framing: TARGET-vs-CURRENT (is the PRD well-formed and ready to build from; not whether ACs pass today).
Inputs read: prd.md (all 771 lines), constraints.yml, idea-brief.md, BACKLOG-108-latest-model-references.md, memory topic latest-model-references.md.

## Gate result

| # | Criterion | Result | Severity |
|---|-----------|--------|----------|
| 1 | Business value clear | PASS | - |
| 2 | Stories valuable and correctly scoped to backlog and idea brief | PASS (1 warning) | warning |
| 3 | Success gates and metrics tie to stated problem | PASS (1 warning) | warning |
| 4 | Open questions honestly non-blocking (OQ-9 open by design) | PASS | - |
| 5 | "Latest version of model X" reframing implemented coherently | PASS (1 warning) | warning |

No blocking failures.

## Findings

1. **Business value (PASS).** PRD section 1 states the problem structurally: every model release forces a repo-wide migration (third time: 4.7, 4.8 attempt, 5), and the fix is to stop encoding versions. Personas (section 2) each have a concrete pain. NFR-11 ("files to edit when the next model releases: 0") is the value statement in measurable form.

2. **Scope alignment with backlog (PASS).** The 7 stories in prd.md section 3 match the backlog Work Items table one to one (S1 to S7, same closing gates). Backlog constraints C-01..C-08 map to BC-01..BC-08 and PRD section 11. Out-of-scope lists agree (prd-quality-gate-flow aliases, smoke-*.yml, PR, stamps on the 9 unstamped files). The idea brief's 4.8 framing is superseded by a binding user decision recorded identically in the PRD header, backlog Summary and memory Section 0; this is the intended state.

3. **WARNING (non-blocking): idea-brief is stale and carries no supersession note.** `.delivery/artifacts/01-idea/po/idea-brief.md` still says "Opus 4.8 Migration", a positive allowlist guard, 9 new stamps, and the refuted "4.8 dispatches fewer sub-agents" claim. PRD Revision 3/4 changelogs and memory Section 0 document the supersession, and 01-idea artifacts are declared immutable (AC-7.5), so this is acceptable. Required fix: none for Stage 2 exit. Suggestion: downstream stages must be pointed at the PRD and memory topic, not the brief.

4. **Success gates tie to the problem (PASS).** G1 (guard forbids pins, runs at ship), G-LIT (canonical count 0), G2/G3 (version-free stamps, 34/34 reviewed) all attack "version strings in the tree". Each gate has exactly one closing story (section 5 ownership rule) and a runnable AC. G5 (observed model, parser proven on a real stream) is added scope but justified: the PRD shows executed evidence that the current parser reports `unknown` and cost 0.0 on a real stream, so baseline re-capture would be meaningless without it.

5. **WARNING (non-blocking): no direct test of the headline value claim.** NFR-11 (zero edits at next release) is "Verification: inspection ... by construction". The structural design supports it, and R7 (behaviour drift when "latest" moves) is honestly recorded with the quarterly fitness review as trigger. AC-1.2a already includes family-agnostic must-hit strings (`claude-mythos-5`, `claude-3-5-sonnet-20241022`), so coverage is largely present. Optional strengthening at Stage 5/6: a fixture with a hypothetical higher-numbered future ID. No PRD change required.

6. **Story sizing (PASS).** S3 is L (34 SKILL.md prose review); the PRD provides a de-risking path via OQ-9 (Michael may narrow) and AC-3.1 works under either answer. Strict order S1 to S7 is justified by BINDING-2.5.

7. **Open questions (PASS).** OQ-1, OQ-7, OQ-10 are resolved with evidence. OQ-2, OQ-6, OQ-8 concern claims that never ship (guarded by AC-2.3 and adversarial re-fetch). OQ-3, OQ-4, OQ-5, OQ-11 have Architect owners at Stage 4 with a runnable default. OQ-12 (`--bare`) and OQ-9 belong to the human with defaults that equal current behaviour or the fully-costed scope. Each row states why it is non-blocking and those reasons hold. OQ-9 deliberately open: accepted.

8. **Reframing coherence (PASS).** Checked end to end:
   - Convention (section 3): family-only prose; `model_awareness: latest` / `pattern_library_version: rev-1` / `last_audited` date; CLI aliases defined once (`MODEL_TIER_ALIAS`); API code reads one config value because the API has no evergreen alias (cited, section 8); synthetic fixture IDs.
   - constraints.yml `model_refs` and `invariants` restate the same scheme; no pin remains in it.
   - The Opus 5 fact lives only in citations and observed baselines (JSON out of guard scope by design), never in shipped prose or stamps.
   - Guard, canonical count command and ACs share one contract (PIN/STAMP/PROSE/BARE, no exemptions); accepted loopholes recorded (FR-1.2).
   - Honest limits stated: push-run guard detects but cannot block; local script is the blocking gate (FR-1.5, FR-7.3).

9. **WARNING (non-blocking): historical version words in memory and backlog.** The memory topic keeps superseded rulings (Sections 1 to 6) with 4.7/4.8/5 IDs. They sit under `.delivery/`, which the guard excludes, so there is no conflict. Noted so Stage 6 does not treat them as leftovers.

10. **Minor readability note.** prd.md is 771 lines with four revision changelogs; a builder must read sections 1, 3, 5 and 8 first. Not blocking; the section 5 gate table and section 3 convention are an adequate entry point.

11. **Citation honesty (PASS).** Section 8 marks each claim VERIFIED/UNVERIFIED, discloses that the serving-infrastructure and headless-doc quotes come from the Challenger's fetch and were not re-fetched by the PO, and carries UNVERIFIED items (`haiku` latest, Claude Code default effort, literalism) as non-shipping OQs.

## Verdict

PASS. Business value is clear, stories map cleanly to the backlog and the (superseded) idea brief, gates and metrics tie to the stated problem, open questions are honestly non-blocking, and the latest-version reframing is coherent across PRD, constraints and backlog. Four non-blocking warnings (findings 3, 5, 9, 10) need no action before Stage 3.
