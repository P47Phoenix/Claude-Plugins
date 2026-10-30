# Source Grading

A rubric for weighting a website, article, video or transcript as evidence. The grade tells the user how far to trust the artifact's claims. It does not decide whether a single claim is true; the verification checks do that.

## The Four Grades

| Grade | What it is | Weight |
|---|---|---|
| **Primary** | The ancient or original text itself: the Bible in Greek or Hebrew, the Mishnah or Talmud, Josephus, a church father's own work, a manuscript | Highest; check it directly |
| **Scholarly** | Peer-reviewed article, academic press book, standard lexicon or critical commentary, a university or seminary scholar writing in their field | High; weigh by field and date |
| **Popular** | A pastor, ministry, magazine, blog or video by an informed writer, citing little or nothing | Medium to low; verify each claim |
| **Anonymous / unknown** | No author, no date, content farm, social post, forum, AI-generated page | Lowest; do not rely on it |

## Questions to Ask

1. **Who wrote or said it?** Name, role, field. A New Testament scholar on the New Testament weighs more than the same person on economics
2. **When?** Date of publication. For scholarship, check for later correction or a stronger contrary view. For a post, check the age
3. **What does it cite?** Count the specific, checkable sources (verse, tractate and folio, named book with author and year). "Scholars say" counts as zero
4. **Can the citations be found?** Spot-check two. A citation that cannot be found is a warning sign
5. **What is its purpose?** To teach, to sell, to provoke, to win an argument. Note any commercial or partisan aim
6. **Does it match the standard sources?** Check one or two key claims against a primary lexicon or a standard scholarly work
7. **Does it separate fact from opinion and devotion?** Mark where it does not

## Modifiers

Move the grade up or down one step for:

- **Up:** cites primary sources precisely; engages the strongest counterview; has an identifiable expert author; has a correction record
- **Down:** repeats a known folk claim (see `viral-claims.md`); cites nothing for strong claims; quotes an authority with no source; has a clear sales or partisan motive; was written by someone outside their field on a technical point

## For Transcripts and Video

- Treat the speaker as the author. Grade by their role and what they cite
- A sermon is a **popular** source unless the speaker is a recognized scholar speaking in their field
- Quote positions by timestamp, not by words (guardrail 9)
- If the transcript is auto-generated, note that errors in the text may be the transcription, not the speaker

## For Websites

- Check the About page and author line
- Check whether the page cites sources and whether they open
- A Wikipedia-style summary page is a **tertiary** guide: use it to find sources, not as one. Grade it popular
- Note whether the page is a lyrics site, a devotional site, an apologetics site or a news site, since each has its own pattern of weakness

## Output

For each source, one block:

```
Source: [TITLE, SITE OR SPEAKER]
Grade: [primary / scholarly / popular / anonymous]
Date: [DATE OR "undated"]
Cites anything: [yes - N specific sources, M found | no]
Notes: [UP/DOWN MODIFIERS, ONE LINE EACH]
```
