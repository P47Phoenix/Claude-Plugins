# PO DoD Review — BACKLOG-108 PRD (Revision 5), Stage 2 Refine, round 2

Validator: Product Owner (business value, story scope, gates and metrics, open questions, reframing coherence, navigability). Target-vs-current framing: judged for well-formedness and build-readiness, not for ACs passing today.

## Gate-result table

| # | Criterion | Result | Severity |
|---|-----------|--------|----------|
| 1 | Business value clear | PASS | blocking |
| 2 | Stories valuable and correctly scoped to backlog (idea brief superseded per binding decision) | PASS | blocking |
| 3 | Success gates and metrics tie to the stated problem | PASS | blocking |
| 4 | Open questions honestly non-blocking (OQ-9, OQ-12 deliberately open) | PASS | blocking |
| 5 | Reframing implemented coherently | PASS | blocking |
| 6 | PRD navigable | PASS with warning | warning |
| 7 | Personas specific with goals, pain, context | PASS | warning |
| 8 | Out-of-scope present and non-empty | PASS | blocking |
| 9 | Dependencies with status; risks with L/I/mitigation; assumptions listed | PASS | warning/suggestion |

## Findings

1. Business value is stated as behaviour, not as a measured cost (section 1, section 2; warning). The problem is "every model release forces a repo-wide migration; third time in a quarter". No baseline effort (hours, files touched) for a past migration is given, so the payoff is asserted, not sized. Success is still well tied: NFR-11 (0 files edited on next release, executable through >= 3 synthetic-future fixtures in AC-1.2a) and NFR-10 (`guard-scope hits 0 files 0`). Required fix (optional): add one line in section 1 giving the file/line count touched by the 4.7 migration, as the baseline the "0 edits" target is compared against.

2. Stories are engineering work items, not "As a <persona>, I want, so that" stories (section 3; warning). Each story has an FR, runnable ACs and a closing gate, and section 2 personas carry goals and pain, so value traceability exists, but no story names its persona. Required fix (optional): add a one-line "Serves: <persona>" tag under each S1 to S7 heading.

3. Navigability (warning). PRD is 978 lines; sections 13 to 17 are revision history. The reader's guide (line 8) mitigates this by naming sections 1, 3, 5, 8 as the builder path. Residual risk: the idea brief still says "Opus 4.8 Migration" and carries no supersession note of its own (guide says so explicitly). Required fix (optional): move the reader's-guide sentence about the superseded brief into a short "Read first" box, and consider a one-line pointer at the top of the idea brief only if the immutability rule (AC-7.5) permits.

4. Gate to story mapping is coherent (section 5; no action). One closing story per gate, precondition stories listed, and the backlog work-item table matches the PRD (S3 closes G2/G3/G6; S4 closes G4/G-LIT; S5 G5; S6 G9; S7 G8/G10). G8 and G10 are inspection-only, acknowledged as process gates. Acceptable.

5. Open questions (section 9; no action). OQ-1, 7, 10 are resolved with evidence; OQ-2, 3, 4, 5, 6, 8, 11 carry a "why non-blocking" that holds (defaults exist, claim never ships, or either answer keeps ACs satisfiable). OQ-9 and OQ-12 are open for the human with a stated PO default and cost of either answer. Honest.

6. Reframing coherence (no action). The latest-version decision is recorded once (line 15), the convention is stated once (section 3 preamble), and pins, stamps, prose, tier aliases, API-has-no-alias, and baselines-record-observed-model are consistent across S1 to S7, NFRs, risks (R7 to R9, R13) and citations. The known gap that the API has no evergreen alias is handled honestly (FR-2.2 config-read, convention 4, R10) rather than papered over.

7. Scope discipline (no action). S5 smoke-harness parser fix and re-baselining is larger than a pure de-pinning, but is in the backlog work items and justified by evidence (real stream-json shape differs from the fixture; model reported `unknown`). Out-of-scope list is substantive (prd-quality-gate-flow, smoke workflows, PRs, 9 unstamped files, `--bare`, `.json` scanning).

## Verdict

DONE. All blocking criteria pass. The three warnings (baseline size of the past migration, persona tags on stories, residual navigation cost of the long PRD) are non-blocking and may be addressed at the author's discretion or carried forward. PRD is well-formed and ready to build from.
