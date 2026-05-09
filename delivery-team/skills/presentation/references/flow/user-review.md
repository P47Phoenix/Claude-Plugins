# Step 6: User Review

**Begin**: `[6/6] Ready for your review.`

If threshold was exceeded (100%), append to the presentation output:

> `[NOTICE] Generation exceeded threshold ({elapsed}s / {threshold}s). Consider using '--light' or adjusting 'presentation.thresholds' config.`

Present to the user:
1. The complete presentation between `--- PRESENTATION START ---` and `--- PRESENTATION END ---`
2. A **Collaboration Summary** table: role | slides contributed | artifacts consumed
3. **Narrative Cuts** (if any): list of slides merged/removed by the cutting pass, with rationale from `cuts_log`. Enables user to `restore {slide title}` if needed.
4. **Emphasis Order** (if reordered): list of slide reorder actions from `emphasis_log`, showing impact-ranked ordering decisions.
5. Warnings (staleness, [TBD] count)
6. Suggestions from Review Gate
7. Options:
   - **approve** — save to `.delivery/artifacts/presentations/{type}-{date}.md` (or `.pptx` when format=pptx)
   - **changes** — describe what to adjust
   - **abort** — discard draft

## PPTX Generation (when format=pptx)

On **approve**, if format is `pptx`, execute the PPTX generation step:

1. **Dependency check**: Verify `python-pptx` is installed. If not, fall back to structured-markdown with warning:
   > "PPTX output requires python-pptx. Install with: pip install python-pptx. Falling back to structured-markdown."
   Save the `.md` artifact instead and stop.

2. **Invoke script**:
   ```bash
   python delivery-team/skills/presentation/scripts/generate_pptx.py \
     --input .delivery/artifacts/presentations/.drafts/composed-draft.json \
     --output .delivery/artifacts/presentations/{type}-{date}.pptx \
     [--template {presentation.pptx_template or --template flag}] \
     [--font {presentation.pptx_font or --font flag}] \
     [--accent-color {presentation.pptx_accent_color or --accent-color flag}]
   ```

3. **Branding precedence** (evaluated once at generation):
   - CLI `--template` flag > config `presentation.pptx_template` > no template (blank presentation)
   - CLI `--font` flag > config `presentation.pptx_font` > default: Calibri
   - CLI `--accent-color` flag > config `presentation.pptx_accent_color` > default: #2d5aa0
   - Template provides the base; font/color flags override within it.

4. **Output**: Display to user:
   > "Presentation saved to .delivery/artifacts/presentations/{type}-{date}.pptx
   > {N} slides generated. Note: PPTX output is designed for editing -- minor formatting adjustments may be needed."

5. Clean up `.drafts/` directory (including `.json` intermediate).

## Change routing (when user says "changes")

| Feedback Type | Routes To | Example |
|---------------|----------|---------|
| Structural (add/remove/reorder slides) | Step 1 | "Add a demo slide after features" |
| Content (wrong data, different emphasis) | Step 3 | "Velocity should be in story points" |
| Formatting/tone (layout, wording) | Step 4 | "Make slide 3 more concise" |

Re-execute from the routed step forward, not from the beginning.

**On approve**: Save final presentation. Clean up `.drafts/` directory.
**On abort**: Clean up `.drafts/` directory. No artifacts saved.
