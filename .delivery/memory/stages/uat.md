# UAT Stage Lessons

**Entries**: 3 | **Last updated**: 2026-03-29

- Dogfooding is a P0 UAT gate, not a follow-up task. PO will reject UAT without it. Execute dogfooding BEFORE submitting for DoD, not after. (validated: 2, last: run-2026-03-29-h3k7)
- Review scope must include ALL files in the changeset, including shared utility modules (e.g., hook_utils.py in lib/). QA validator checks file counts against actual files on disk. (validated: 1, last: run-2026-03-27-c8f2)
- FEATURE-type pipeline runs serve as dogfooding evidence for structural pipeline changes (exercises more stages than BUG_FIX). Sufficient when the pipeline itself is the product under test. (validated: 1, last: run-2026-03-29-h3k7)
