# Research Method

Loaded for every `research` task type. Adapted from the repository's `research-agent` skill (type detection, source IDs, integrity tags, bias audit, provisional disclosure), trimmed to what Bible research needs. The academic frameworks (PICO, SPICE, PECO, GRADE) are **not** used here; `source-tiers.md` replaces GRADE.

---

## 1. Classify the question

State the shape of the question before searching. It decides the source plan.

| Shape | Signal | Plan |
|---|---|---|
| **Descriptive** | "what is", "list", "timeline", "who was", "passages on" | Map what the primary text says first, then what scholarship adds |
| **Explanatory** | "why", "what led to", "how did X come about" | Primary text, then the historical and scholarly context; label causal links `[INFERENCE]` unless a source states them |
| **Comparative** | "difference between", "X or Y", "early or late date" | Lay out each position with who holds it; do not pick a winner unless the sources do |
| **Exploratory** | "how might", "what themes", "ideas" | Primary text and a verified timeline first; everything derived from them is `[INFERENCE]` |

Song-idea requests are exploratory and rest on a descriptive timeline. Do the timeline first.

---

## 2. Source plan

Before fetching, write a short plan: which passages to open, which lexicon entries, which scholarly works, which Jewish sources. Then work the plan in tier order (see `source-tiers.md`):

1. **Primary text** -- open the passage in the stated translation; check the original-language term where it matters
2. **Lexicon** -- BDAG, HALOT, Strong's (named), for any term claim
3. **Scholarly** -- a named published work (author, title, year, page or section if possible); for dates, a chronology (for example Finegan, *Handbook of Biblical Chronology*; Thiele, *The Mysterious Numbers of the Hebrew Kings*; Kitchen, *On the Reliability of the Old Testament*; Hoehner, *Chronological Aspects of the Life of Christ*). Opening the work, or a page that quotes it with a citation, is required before citing it
4. **Jewish sources** -- Sefaria page for the tractate and folio or the named Midrash
5. **Popular** -- study-Bible notes, reputable reference sites, encyclopedias; use to find leads, never as the only support for a key claim

Search is for finding sources; the source itself is what gets cited.

---

## 3. Source IDs and tags

- Give every source an ID in order of first use: `S1`, `S2`, ... List them at the end under "Sources" with tier, author or site, title, year, and what was opened
- Cite inline by ID: "the siege began in the ninth year of Zedekiah (2 Kings 25:1, S1; Thiele, S4)"
- Tags, used inline and never removed silently:
  - `[UNVERIFIED]` -- the claim is common but no source was located. In a timeline the entry is **dropped**; in findings it stays, tagged
  - `[INFERENCE]` -- reasoning that goes beyond what the sources state (a causal link, a thematic reading, a song idea)
  - `[CONTESTED]` -- scholarship splits; both positions and who holds them are given
  - `[Single-source]` -- a key claim rests on one source; seek corroboration or say none was found
  - `[TRADITIONAL]` -- held by a named tradition (rabbinic, patristic, church) but not asserted by the text itself; name the tradition and its source

---

## 4. Quote and paraphrase

Verbatim quotes use quotation marks and give the reference. Everything else is paraphrase. Never present paraphrase as a quotation. Keep quotations short (a verse or a sentence); never reproduce long passages from a source (guardrail 9).

---

## 5. Bias audit (before assembling)

Ask, and record the answer in a line under "Method notes":

- **Tradition bias** -- did the plan lean on one confessional tradition's sources? Name a source from another tradition on any contested point
- **Recency or popularity bias** -- did a single popular site shape the result? Replace it with a primary or scholarly source, or tag `[Single-source]`
- **Confirmation bias** -- did the search look only for support? Record the strongest counter-position found, or say none was found
- **Harmonizing bias** -- did the result smooth over a tension in the text or between sources? Report the tension as it stands

If a bias is found after findings were written, tag the affected findings `[BIAS RISK: type]` rather than quietly rewriting them.

---

## 6. Provisional disclosure

When source access limited the work (a work could not be opened, a page was behind a paywall, only a summary was read), say so in the Method notes and again in the Verification notes: "These findings are provisional because [limitation]; verify before relying on them."

---

## 7. Multi-slice assembly (timeline and song-ideas)

When several era slices come back:

1. Merge in canonical order (the era order in `timeline-eras.md`), then by passage order within an era
2. Renumber `S[N]` IDs so each source has one ID across the merged result; merge duplicate sources
3. Keep every `[CONTESTED]` and `[UNVERIFIED]` tag; never resolve a split by choosing one date
4. Where two slices date the same event differently, report the range that covers both with both sources, tagged `[CONTESTED]`
5. Apply the contract last; the merged result keeps the "INTERNAL DRAFT" line until the gate removes it
