# UAT Stage Lessons

**Entries**: 6 | **Last updated**: 2026-04-03

- Dogfooding is a P0 UAT gate, not a follow-up task. PO will reject UAT without it. Execute dogfooding BEFORE submitting for DoD, not after. (validated: 2, last: run-2026-03-29-h3k7)
- Review scope must include ALL files in the changeset, including shared utility modules (e.g., hook_utils.py in lib/). QA validator checks file counts against actual files on disk. (validated: 1, last: run-2026-03-27-c8f2)
- FEATURE-type pipeline runs serve as dogfooding evidence for structural pipeline changes (exercises more stages than BUG_FIX). Sufficient when the pipeline itself is the product under test. (validated: 2, last: run-2026-03-30-r4x2)
- Structural-only empirical validation (when bash unavailable) should cap review board confidence below 5/5 and carry a P1 follow-up. Do not claim full validation with structural evidence alone. (validated: 1, last: run-2026-03-30-r4x2)
- Tech Writer validator in plugin repos must search INSTALLED plugin files (e.g., ~/.claude/plugins/...), not repo source files. False negatives occur when the validator greps the wrong file scope. Provide explicit file paths in the prompt. (validated: 1, last: run-2026-04-01-m7v3)
- Agent validation of format-critical rules (color identity, legality) must be deterministic API-driven, not LLM-inferred. When correctness is binary, mandate programmatic validation in the agent guide. LLM card knowledge is unreliable for exhaustive checks across 100+ items. (validated: 1, last: run-2026-04-02-k3r9)
