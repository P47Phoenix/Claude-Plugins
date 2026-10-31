# Source Tiers

Loaded for every `research` task type. How to weigh a source and what each tier is good for. Replaces the GRADE evidence grading used by the repository's `research-agent` skill, which does not fit textual and historical work. Complements `../../topic-verification/references/source-grading.md`, which grades an artifact being checked; this file grades sources used to build a result.

---

## The tiers

| Tier | What it is | Good for | Not enough for |
|---|---|---|---|
| **Primary text** | The biblical text in a named translation; the Hebrew, Aramaic or Greek text (for example via Blue Letter Bible, STEP Bible, Bible Gateway, the SBLGNT); manuscripts and ancient witnesses (LXX, DSS, Josephus, Philo, inscriptions, ancient Near Eastern records) | What the text says; sequence of events; what an ancient witness reports | Absolute dates (the text gives regnal years, not calendar years); the meaning of a rare word on its own |
| **Lexicon** | BDAG, HALOT, BDB, LSJ, Strong's (concordance numbers only), TDOT/TDNT, NIDOTTE/NIDNTTE | The sense and range of a term; where it occurs | Theology built on etymology; a claim about what a word "really means" against its context |
| **Scholarly** | A named published work with author, title and year: commentaries, chronologies, histories, journal articles, Bible dictionaries (Anchor Yale, IVP), reference grammars; Sefaria for rabbinic texts | Dates (as ranges), historical setting, state of the debate, who holds which position | Settling a contested point by one author's view; use two when the point is contested |
| **Popular** | Study-Bible notes, GotQuestions, Wikipedia, blogs, sermon sites, encyclopedia summaries, AI summaries | Finding leads, the common view, what people believe | The only support for any key claim, any date, any original-language claim, any rabbinic citation |

Jewish sources count as **primary** for what the tradition says (cite tractate and folio or the named Midrash) and as **traditional**, not historical, for what happened (guardrail 3; tag `[TRADITIONAL]`).

---

## Rules

1. A key claim needs a primary or scholarly source. Popular support alone makes it `[UNVERIFIED]`
2. A date needs a scholarly chronology or an ancient witness, and is a range or `[CONTESTED]` (guardrail 12). Popular sites often print one year as if settled; do not copy that
3. An original-language claim needs a lexicon, named (guardrail 2). A popular site quoting Strong's is not a lexicon check
4. A rabbinic claim needs the tractate and folio or the named Midrash, opened on Sefaria or in a printed edition (guardrail 3)
5. A claim about a scholar's position needs that scholar's work, or a scholarly source that cites it by page. "Many scholars say" without a name is `[UNVERIFIED]`
6. Where primary text and a scholarly source disagree about what the text says, the text wins; report the disagreement
7. Where two scholarly sources disagree about history or date, report both with names; do not average them into a single figure
8. Record for each source what was actually opened (the page, the entry, the chapter). A source found in a search snippet but not opened is a lead, not a citation

---

## Recording a source

Under "Sources" at the end of the result:

```
S1 (primary) -- 2 Kings 24-25, ESV, Bible Gateway. Opened: full chapters.
S2 (lexicon) -- BDAG s.v. tetelestai. Opened: entry via [site].
S3 (scholarly) -- Thiele, The Mysterious Numbers of the Hebrew Kings, 3rd ed., 1983, ch. 9. Opened: chapter summary on [site]; page numbers not confirmed.
S4 (popular) -- [site], "[page title]", accessed [date]. Used for leads only.
```

Tier names are fixed: primary, lexicon, scholarly, popular. Add `traditional` after the tier for a Jewish or patristic source used for tradition rather than history.
