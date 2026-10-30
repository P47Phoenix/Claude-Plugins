# Doctrinal Alignment

## Purpose

Check the sermon against Protestant doctrinal consistency and internal theological coherence.

## Checks For

- Consistency with core Protestant distinctives (e.g. sola scriptura, sola fide) unless the user has specified a different tradition's lens
- Internal contradictions within the sermon's own theological claims
- Places where a claim is denominationally contested and should be flagged as such rather than presented as settled
- Whether Old Testament/Jewish material is integrated in a way that doesn't misrepresent Jewish theology or practice

## Output Format

A list of doctrinal concerns. The fields are defined in `contracts/doctrinal-concerns.md`.

## Standards

- Distinguish clearly between "this is doctrinally incorrect" and "this is contested across traditions and should be framed as such."
- No invention: don't assert a doctrinal position isn't held by any tradition without being sure of that.

## How to Check

1. Read for every theological claim: God, Christ, the Spirit, salvation, the church, last things, the sacraments, Scripture
2. Ask of each: is it consistent with mainstream Protestant teaching (name the confession or tradition if you rely on one, e.g. Westminster, Augsburg, Baptist Faith and Message)?
3. Look for contradictions between sections of the same sermon
4. Where traditions differ (Calvinist and Arminian views of election, baptism, spiritual gifts, end times, the role of women in ministry), mark the point **contested across traditions** and name the main positions
5. A point is **doctrinally incorrect** only when it contradicts the text or a core distinctive shared across the Protestant mainstream. If you are not sure, treat it as contested, not incorrect
6. Check Jewish material: does the sermon describe Jewish belief or practice fairly, and does it cite a source (Mishnah, Talmud tractate and folio, named Midrash)? Does it present Jewish texts as though they were proofs for Christian claims?
7. If the user has stated a tradition's lens (Lutheran, Reformed, Baptist, Anglican), apply that lens and say so

## Labels

- **Incorrect:** contradicts the text or a core shared distinctive
- **Contested across traditions:** held differently by named traditions; the draft must frame it as contested
- **Internal contradiction:** two claims in the same sermon conflict
- **Misrepresentation of Jewish material:** describes Jewish belief or practice inaccurately or without a source
