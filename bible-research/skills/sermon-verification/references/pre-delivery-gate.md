# Pre-Delivery Verification & Auto-Correction

## Purpose

Run all verification agents (Scripture-Citation, Historical & Translation Accuracy, Doctrinal Alignment, Red Team) against any sermon breakdown or draft before it is shown to the user. Apply corrections directly into the content rather than surfacing them as a separate report the user has to act on. The user should only ever see a final, corrected version — with a short transparency note summarizing what was checked and changed.

## When This Runs

Automatically, on any sermon breakdown, passage analysis, or draft produced by the core workflow — before that content is sent to the user as a response. This includes the shortlist stage. Not user-invoked; it's a gate, not a request. (A user may also invoke it directly on their own draft with `gate`.)

## Process

1. **Draft internally.** The draft is produced by `sermon-builder` (or supplied by the user).
2. **Run all four verification agents against the internal draft**, exactly as their individual specs define:
   - Scripture-Citation Verification
   - Historical & Translation Accuracy
   - Doctrinal Alignment
   - Red Team
3. **Apply corrections directly into the draft**, not as a side list:
   - Any "not supported" or "needs correction" verdict → fix the underlying claim, reference, or wording in place.
   - Any "partially supported" or overstated phrasing (e.g. Red Team flags on word choice) → reword in place to track the source more precisely.
   - Any denominationally contested point → keep in the draft, but ensure it's explicitly framed as contested (per Doctrinal Alignment agent's standard), rather than removed.
4. **Handle unverifiable claims per the non-negotiable standard**: if a claim can't be corrected because no real source supports any version of it, remove it from the draft entirely rather than leaving a flagged-but-uncorrected claim in front of the user.
5. **Never show the user the pre-correction draft.** Only the corrected version is delivered.

## Output to the User

Deliver:

- The corrected sermon breakdown/draft (final form, ready to read), in the `corrected-draft` contract.
- A brief **"Verification notes"** section at the end — not a full agent-by-agent report, just a short plain-language summary of what was caught and fixed, e.g.:
  - "Corrected: South Galatia audience noted as majority view rather than settled fact."
  - "Reworded: softened 'leveling' language in 4:8–11 to track Paul's actual wording."
  - "Removed: [claim] — no citable source could be found to support it."

If nothing needed correction, say so briefly ("All claims checked and verified against source — no corrections needed") rather than omitting the notes section. The notes section is mandatory, minimum one line.

## Standards

- This agent does not loosen the non-negotiable standards (no invention, real citable sources only, original-language fidelity) — it exists to enforce them silently rather than deferring them to the user.
- Corrections must still be traceable to a real source; this agent doesn't invent a fix if no real fix exists — it removes the claim instead.
- Keep the transparency note short — it's a summary of changes, not a re-run of the full verification report.

## Order of Operations

1. Run the four checks against the draft; record each finding with its claim location
2. Resolve overlaps (a claim flagged by two checks is fixed once)
3. Apply fixes from most severe to least: remove unsourced claims; correct wrong references; reword overstated claims; add contested framing
4. After fixing, re-read the corrected draft once: confirm every remaining claim has a source, every term is glossed, and the notes section is present
5. Do not run `oral-delivery.md`; pacing is on demand only
6. Do not change content that no check flagged, except to repair a sentence broken by a fix
