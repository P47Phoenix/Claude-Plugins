---
loaded_by: hook-judge
level: L3
last_reviewed: 2026-10-26
---

# Hook Rubric

Five criteria, each scored 1-5. Anchors are given for 1, 3, and 5; score 2 and 4 when the hook sits between anchors. The rubric informs the critique and sets revision priority. `cliche_scan.py` and `prosody_check.py --hook` decide the gate; a score of 5 everywhere does not pass a FAIL, and a score of 1 somewhere does not fail a PASS.

## 1. Memorability

- **1**: the line has no repeated sound, no rhythmic shape, and reads as a sentence from prose.
- **3**: a clear rhythmic shape or one internal echo; a listener recalls the gist but not the words after one hearing.
- **5**: a listener repeats the exact words after one hearing; the line has a built-in rhythm and at least one sonic echo (alliteration, internal rhyme, or a repeated stressed vowel).

## 2. Singability

- **1**: consonant clusters or closed vowels on the final stressed syllable; stress falls on articles or prepositions; more than `hook_max_syllables`.
- **3**: natural stress mostly aligns with where a chorus beat lands; the final syllable is singable but not open.
- **5**: every stressed syllable carries a content word; the last stressed syllable is an open or long vowel; within the syllable cap with room for a held note.

## 3. Title fit

- **1**: the title does not appear in the hook and the hook does not imply it.
- **3**: the title appears in the hook but is buried mid-line, or the hook is the title with filler words added.
- **5**: the title is the hook's landing point (final or first stressed phrase) and the `title_rationale` explains a payoff the chorus delivers.

## 4. Concreteness

- **1**: abstractions only (love, forever, heart, dreams); no noun a listener pictures.
- **3**: one concrete noun or verb, but the emotional claim still carries the line.
- **5**: the `central_image` is in or directly behind the hook; a specific, picturable noun or action does the emotional work.

## 5. Brief fidelity

- **1**: contradicts `pov`, `mood`, or a `must_avoid` entry; ignores `theme`.
- **3**: matches theme and mood; pov is correct; `must_include` items are absent or forced.
- **5**: theme, pov, mood, and audience all read correctly from the hook alone; every `must_include` item is present naturally; nothing from `must_avoid`.

## Scoring notes

- Score the hook as written, not as it would read after your suggested revision.
- Total 20 or above with a PASS gate: recommend the orchestrator proceed without a quality loop.
- Total 10 or below with a PASS gate: recommend one optional quality loop; the orchestrator decides.
