# Contract: Topic Report

Emitted by `topic-verification` for every task type (`song`, `web`, `post`, `transcript`, `full`). The assembler sub-agent fills every `[BRACKETED]` placeholder.

## Template

```markdown
# Topic Report: [SHORT NAME OF THE ARTIFACT]

**Artifact:** [TYPE]; [TITLE]; [AUTHOR, SONGWRITER OR SPEAKER]; [DATE OR "undated"]; [URL OR "pasted text"]
**Checked:** [N] claims  |  Supported: [N]  Partially: [N]  Not supported: [N]  Unverifiable: [N]  Contested: [N]

## Source grade
- **Grade:** [primary / scholarly / popular / anonymous]
- **Cites anything:** [yes - N specific sources, M found | no]
- **Notes:** [WHY THE GRADE MOVED UP OR DOWN, ONE LINE EACH]

## Claim-by-claim verdicts

| # | Position | Claim (paraphrase) | Kind | Verdict | Contested vs unsupported |
|---|---|---|---|---|---|
| 1 | [verse 2, line 3 / para 4 / 12:40] | [PARAPHRASE, NO QUOTATION] | [scripture / history / language / doctrine / authority / statistic] | [supported / partially supported / not supported / unverifiable / contested] | [theologically contested | textually unsupported | n/a] |

## Corrections
For each claim marked partially supported, not supported or contested:

### [N]. [SHORT LABEL]
- **What the source material actually says:** [CORRECTION WITH A REAL SOURCE: SCRIPTURE REFERENCE, LEXICON AND HEADWORD, TRACTATE AND FOLIO, OR NAMED WORK WITH AUTHOR AND YEAR]
- **Where traditions differ (if contested):** [NAME THE TRADITIONS AND POSITIONS]
- **Source checked:** [WHAT WAS OPENED; "not opened" IF NOT]

## Overall assessment
[ONE SHORT PARAGRAPH, PLAIN LANGUAGE: HOW RELIABLE THE ARTIFACT IS AND WHY]

## What's fine to [sing | share | rely on], what to be careful with
- **Fine:** [PLAIN-LANGUAGE LIST]
- **Be careful with:** [PLAIN-LANGUAGE LIST, EACH WITH THE REASON]
- **Only a matter of tradition:** [CONTESTED POINTS THAT ARE NOT ERRORS]

## Not checked
[CLAIMS THAT COULD NOT BE CHECKED AND WHY: NO TRANSCRIPT, SOURCE NOT OPENED, NO LEXICON ACCESS]
```

## Rules

- Every verdict has one of the five labels exactly: supported, partially supported, not supported, unverifiable, contested
- The last column keeps **theologically contested** and **textually unsupported** apart (guardrail 10). A claim can be contested and also supported by the text of one tradition's reading
- Do not flag metaphor, poetry or devotion as error (guardrail 11); list devotional lines as "n/a" or omit them
- **Never reproduce lyrics, article paragraphs or post text** (guardrail 9). The claim column is a paraphrase; the position column locates it. For a song, give title, songwriter and line position only
- Each correction names a real source. If none could be found, the verdict is unverifiable and the correction says so (guardrail 5)
- Jewish sources are cited by tractate and folio or by named Midrash (guardrail 3)
- Original-language claims give transliteration, sense and the named lexicon (guardrail 2)
- Artifact details (title, songwriter or author, date) are filled only from what the user supplied or a source you opened; otherwise write "not given" (guardrail 1)
- The closing summary is plain language with short sentences (guardrail 6) and separates "fine", "careful" and "tradition"
- "Not checked" is never omitted. If everything was checked, write "Nothing outstanding."
