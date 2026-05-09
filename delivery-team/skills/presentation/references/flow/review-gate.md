# Step 5: Review Gate (TW + UX)

**Begin**: `[5/6] Reviewing draft... ({reviewer names}, {scope: full | MUST-FIX only})`

**Degradation behavior**:
- **Full mode, under threshold**: 2 reviewers (TW + UX), full scope.
- **Full mode, 75% threshold hit**: 1 reviewer (TW only), MUST-FIX only scope.
- **Light mode, under threshold**: 1 reviewer (TW only), full scope.
- **Light mode, 75% threshold hit**: 1 reviewer (TW only), MUST-FIX only scope.

Dispatch two reviewer sub-agents **in parallel**:

| Reviewer | Skill | Focus |
|----------|-------|-------|
| Technical Writer | `delivery-team:operations` | Clarity, jargon for audience, scannable titles, single message per slide, narrative necessity |
| UX Designer | `delivery-team:ui` | Density, hierarchy, visual story, readability when projected, narrative arc |

**Narrative quality criteria** (added to each reviewer's evaluation scope):
- **TW criterion**: "Does each slide earn its place? Could any slide be cut without losing the argument?" — validates information cutting was effective
- **UX criterion**: "Does the presentation build toward a clear climax? Is the strongest content positioned for maximum impact?" — validates narrative tension arc

Each reviewer reads `composed-draft.md` and returns findings as:
- **MUST-FIX**: Blocks user review. Composer fixes these automatically before Step 6 (including narrative quality MUST-FIX issues — same auto-fix behavior as formatting issues).
- **SUGGESTION**: Included as notes for user awareness.

Show review summary to user (issues found, what was fixed, suggestions preserved).

**Complete**: `Review complete: {N} MUST-FIX resolved, {M} suggestions preserved`
