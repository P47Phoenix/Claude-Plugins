# UAT Stage Lessons

**Entries**: 7 | **Last updated**: 2026-04-04

- Dogfooding is a P0 UAT gate, not a follow-up task. PO will reject UAT without it. Execute dogfooding BEFORE submitting for DoD, not after. (validated: 2, last: run-2026-03-29-h3k7)
- Review scope must include ALL files in the changeset, including shared utility modules (e.g., hook_utils.py in lib/). QA validator checks file counts against actual files on disk. (validated: 1, last: run-2026-03-27-c8f2)
- FEATURE-type pipeline runs serve as dogfooding evidence for structural pipeline changes (exercises more stages than BUG_FIX). Sufficient when the pipeline itself is the product under test. (validated: 2, last: run-2026-03-30-r4x2)
- Structural-only empirical validation (when bash unavailable) should cap review board confidence below 5/5 and carry a P1 follow-up. Do not claim full validation with structural evidence alone. (validated: 1, last: run-2026-03-30-r4x2)
- Tech Writer validator in plugin repos must search INSTALLED plugin files (e.g., ~/.claude/plugins/...), not repo source files. False negatives occur when the validator greps the wrong file scope. Provide explicit file paths in the prompt. (validated: 2, last: run-2026-04-04-j8f2)
- When Dev edits plugin files in the installed location, changes MUST be synced back to the source repo before UAT closes. PO will reject if source and installed diverge. This is the inverse of the Tech Writer lesson — both directions of the installed↔source gap cause problems. (validated: 1, last: run-2026-04-04-j8f2)
- Agent validation of format-critical rules (color identity, legality) must be deterministic API-driven, not LLM-inferred. When correctness is binary, mandate programmatic validation in the agent guide. LLM card knowledge is unreliable for exhaustive checks across 100+ items. (validated: 1, last: run-2026-04-02-k3r9)

- **Cross-doc consistency check by Tech Writer is a load-bearing UAT gate, not a courtesy review.** Tier values, file counts, dates, IDs MUST be spot-checked across all UAT artifacts (test-plan, release-plan, release-notes, user-guide). At run-2026-05-03-tk0e, Bilbo caught: Tier B value mismatch (user-guide said 400, schema says 300), file count off by 3 (release-plan said 17, actually 20), ADR path references unresolved, and a vague checklist item. Add to default UAT TW gate criteria template. (validated: 1, last: run-2026-05-03-tk0e)

- **Producer-validator separation (skill anti-pattern #8) applies to validator-style artifacts too.** Cross-doc-consistency-report is itself produced by the Tech-Writer; a fresh Tech-Writer DoD validator caught a self-drift (5 mislabeled rows). Action: validator-style artifacts (cross-doc reports, traceability matrices) MUST be DoD-checked by a fresh dispatch, not approved-with-caveats by the producer. (validated: 1, last: run-2026-05-05-tk3)

- **Stage 7 entry should sweep for stale Wave-N-1 carry-overs in the new run's namespace.** DEFECT-006 root cause: prior-run UAT review files in `.delivery/artifacts/07-uat/dod/` weren't superseded automatically; the cross-doc Tech-Writer flagged 6 stale files (1 genuinely stale, 5 mislabeled — see producer-validator lesson). Action: add a Stage-7 entry-step that overwrites or moves prior-run UAT carry-overs before primary agents dispatch. Wave 3 surface. (validated: 1, last: run-2026-05-05-tk3)
