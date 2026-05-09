# PPTX

Generated via `scripts/generate_pptx.py` from a JSON intermediate file. Requires `python-pptx` (`pip install python-pptx`).

- The Composer produces `composed-draft.json` alongside `composed-draft.md` during Step 4 when format=pptx
- After user approval in Step 6, the script converts the JSON to a `.pptx` file
- Layout mapping: `title` -> "Title Slide", all other layouts -> "Title and Content" (name-first, index-fallback)
- Tables, speaker notes, and Mermaid diagram placeholders are supported
- Branding via `--template`, `--font`, `--accent-color` (see `references/flow/user-review.md` PPTX Generation step)
- If `python-pptx` is not installed, falls back to structured-markdown with a warning

**When to use**: native PowerPoint editability needed; corporate branding via `.pptx` template.
