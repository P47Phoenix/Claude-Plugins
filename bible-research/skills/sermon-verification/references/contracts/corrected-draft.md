# Contract: Corrected Draft

Emitted by `sermon-verification` task type `gate`. The only thing the user sees from the gate: the corrected content, ending in a mandatory "Verification notes" section. Never the pre-correction draft, never the four reports.

## Template

```markdown
[THE CORRECTED DRAFT, IN THE SAME CONTRACT AS THE INPUT (SHORTLIST, BREAKDOWN, MANUSCRIPT OR REVISION), FINAL FORM, READY TO READ. NO "INTERNAL DRAFT" MARKER. NO FLAGS LEFT IN THE TEXT.]

**Verification notes:**
- **Checked:** [WHAT WAS CHECKED, IN PLAIN WORDS]
- **Corrected:** [WHAT WAS FIXED AND HOW, ONE LINE EACH]
- **Reworded:** [PHRASING SOFTENED TO TRACK THE SOURCE]
- **Contested (kept, framed as contested):** [POINTS]
- **Removed:** [CLAIM] - no citable source could be found to support it.
- **Not settled / not confirmed:** [WHAT COULD NOT BE CONFIRMED AND WHY]
```

## Rules

- **The Verification notes section is mandatory**, with no exceptions, on a shortlist as much as on a full breakdown
- **Minimum one line.** If nothing needed correction: **Verification notes:** All claims checked and verified against source - no corrections needed.
- Omit a bullet that has nothing to report, except in the all-clear case
- Apply corrections in place: "not supported" or "needs correction" -> fix the claim, reference or wording; "partially supported" or overstated -> reword to track the source; contested -> keep, framed as contested
- **Remove** any claim that no real source supports in any version; do not leave it flagged and uncorrected, and do not invent a fix (guardrails 5 and 12)
- Notes are a short plain-language summary of changes, not a re-run of the full report (guardrail 6)
- Never name the internal draft, an agent, a verdict table or a flag count
- Never claim a check that was not performed; say what was not confirmed
- Keep the input's contract: a shortlist stays a shortlist of 3-5 candidates ending in the question; a breakdown keeps sections 1-7 (and 8 for a manuscript)
