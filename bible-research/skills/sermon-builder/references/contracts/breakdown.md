# Contract: Breakdown

Emitted by `sermon-builder` task types `breakdown`, `draft` and `revise`. The five required parts come from the project's sermon-building workflow (context, original language, theology, homiletical structure, references). Sections 1-7 follow the layout of the project's finished breakdowns, using `source/sample-breakdown-loving-your-wife.md` as the structural sample; sections 4 and 6-7 add the Jewish-sources, index and bibliography parts that the better chats included. The gate adds the closing "Verification notes".

## Template

```markdown
# [PASSAGE REFERENCE]: "[TITLE]"

**Translation used:** [NAME, STATED ONCE]. Switches are marked in the text.

## 1. Original Context
- **Historical setting:** [WHO WROTE IT, WHEN (STATE ANY SCHOLARLY DISAGREEMENT), WHAT WAS HAPPENING]
- **Literary setting:** [GENRE, PLACE IN THE BOOK, WHAT COMES BEFORE AND AFTER]
- **Audience:** [WHO FIRST HEARD IT, WHAT THEY ALREADY KNEW]
- **Structure of the passage:** [SHORT MAP BY VERSE RANGE]

## 2. Original-Language Notes
For each key term (3-6):
- **"[ENGLISH WORD]" (*[TRANSLITERATION]*, [SCRIPT OPTIONAL]) - [VERSE].** [SENSE IN PLAIN WORDS]. Lexicon: [BDAG / HALOT / Strong's, s.v. HEADWORD]. [WHY IT MATTERS FOR THE SERMON]

## 3. Theological Significance
- [POINT, WITH SCRIPTURE REFERENCE]
- **Contested across traditions:** [POINT, WITH THE MAIN READINGS NAMED]  (use only where true)
- **Echoes and parallels (labeled as echoes):** [PASSAGE] echoes [PASSAGE] in [SHARED WORD OR THEME]. The later text does not quote the earlier one.

## 4. Jewish and Other Extra-Biblical Sources
- [SOURCE, e.g. b. Sanhedrin 108b / Mishnah Sukkah 4:9 / Bereishit Rabbah 33:6]: [WHAT IT SAYS, PARAPHRASED]. [DATE OF THE TEXT AND WHETHER IT WAS WRITTEN AFTER THE NT]. [Sefaria link only if fetched and confirmed]
- If none can be cited: "No Jewish or extra-biblical source I can name supports a claim here." (never "Jewish tradition says")

## 5. Suggested Homiletical Structure
**Big idea:** [ONE SENTENCE]
**I. [MOVEMENT TITLE] ([VERSES])** [ONE TO TWO SENTENCES]
**II. ...**
**[Closing / forward pointer]** [WHERE THE PASSAGE LEADS]

## 6. Scripture Index
- **Primary text:** [REFERENCE]
- **Cross-references:** [REFERENCE] ([WHY, AND WHETHER QUOTATION, ALLUSION OR ECHO])

## 7. Sources and Bibliography
- [AUTHOR, TITLE, PUBLISHER/JOURNAL, YEAR] ([WHAT IT SUPPORTS])
- [LEXICON, s.v. HEADWORD]
- **Gaps:** [CLAIMS THE DRAFT COULD NOT SUPPORT, LEFT OUT]

## 8. Manuscript (draft task only)
[FULL SERMON TEXT PER homiletical-structure.md]

**Verification notes:** [ADDED BY THE GATE]
```

## Rules

- Sections 1, 2, 3, 5 and 6 are always present. Section 4 is present even when empty (state why). Section 7 lists real works only. Section 8 appears only for `draft`
- `revise` returns only the sections that changed, each with a one-line reason for the change
- Every scripture reference is book, chapter, verse
- Every original-language term has transliteration, sense and a named lexicon (guardrail 2)
- Section 4 cites by tractate and folio or named Midrash (guardrail 3)
- Contested points are labeled contested; echoes are labeled as echoes (guardrails 4, 8)
- Section 7 never lists a source that was not opened or confirmed
- Plain language throughout (guardrail 6)
