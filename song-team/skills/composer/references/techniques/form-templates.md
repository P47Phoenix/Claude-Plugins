---
loaded_by: structure-judge, groove
level: L3
last_reviewed: 2026-10-26
---

# Form Templates

Craft description of the six templates in `song-team/scripts/data/form-templates.json`. The JSON is what `structure_check.py` enforces; this file explains the same rules in words. When the two disagree the JSON wins and this file is wrong. Every template defaults to key `C`, `4/4`, and the tempo band shown.

Notation: `?` marks an optional section; `{n..m}` is an allowed repeat count; bars are `min-max`. A section label in `structure.md` is matched exactly (regex anchored both ends), so `Verse` fails where `Verse 1` is required.

## VCVCBC (verse-chorus with bridge)

The default `FULL_SONG` form. Tempo band 84-140.

| Order | Label | Bars | Repeat |
|-------|-------|------|--------|
| 1 | `Intro` | 2-16 | `?` |
| 2 | `Verse 1` | 4-16 | 1 |
| 3 | `Pre-Chorus 1` | 2-8 | `?` |
| 4 | `Chorus` | 4-16 | 1 |
| 5 | `Post-Chorus` | 2-8 | `?` |
| 6 | `Verse 2` | 4-16 | 1 |
| 7 | `Pre-Chorus 2` | 2-8 | `?` |
| 8 | `Chorus` | 4-16 | 1 |
| 9 | `Post-Chorus` | 2-8 | `?` |
| 10 | `Instrumental` | 2-16 | `?` |
| 11 | `Bridge` | 4-16 | 1 |
| 12 | `Chorus` | 4-16 | `{1..2}` |
| 13 | `Tag` or `Outro` | 1-16 | `{0..2}` |

Default meter: Verse four lines of `8/uSuSuSuS`; Pre-Chorus two lines of `6/uSuSuS`; Chorus `7/SuSuSuS` x3 then `8/SuSuSuSu`; Post-Chorus two lines of `4/SuSu`; Bridge two lines of `8/uSuSuSuS`; Tag `7/SuSuSuS`; Intro, Instrumental, Outro empty (unconstrained). Craft: the chorus is front-stressed and shorter-lined than the verse so it lifts; the bridge changes angle, not just chords; the final chorus repeat earns a lyric variation or a tag.

## AABA (thirty-two-bar form)

Standards, ballads, musical-theatre songs. Tempo band 60-120.

| Order | Label | Bars | Repeat |
|-------|-------|------|--------|
| 1 | `Intro` | 2-8 | `?` |
| 2 | `A1` | 4-16 | 1 |
| 3 | `A2` | 4-16 | 1 |
| 4 | `B` | 4-16 | 1 |
| 5 | `A3` | 4-16 | 1 |
| 6 | `Tag` or `Outro` | 1-8 | `{0..2}` |

Default meter: A and B sections four lines of `8/uSuSuSuS`; Tag `7/SuSuSuS`. Craft: the title lands at the end (or start) of every A; B (the middle eight) moves to a new harmonic area and a new lyric angle; A3 resolves what A1 set up. `arrangement_check.py` treats `B` as the bridge.

## verse-refrain

Folk, ballad, story songs: each verse closes on the same refrain line. Tempo band 70-130.

| Order | Label | Bars | Repeat |
|-------|-------|------|--------|
| 1 | `Intro` | 2-16 | `?` |
| 2 | `Verse <n>` | 8-24 | `{2..4}` |
| 3 | `Bridge` or `Instrumental` | 4-16 | `?` |
| 4 | `Verse <n>` | 8-24 | `{0..3}` |
| 5 | `Tag` or `Outro` | 1-16 | `{0..2}` |

`<n>` is a single digit (`Verse 1` ... `Verse 9`). Default meter: Verse four lines of `8/uSuSuSuS` then the refrain line `7/SuSuSuS`; Bridge two lines of `8/uSuSuSuS`; Tag `7/SuSuSuS`. Craft: the refrain line is fixed text and the fifth meter line; verse 1 sets the scene, each later verse advances time or widens the lens; the refrain means something new by the last verse. There is no chorus-role section, so `arrangement_check.py` falls back to `strict_rising`.

## jingle

15-60 seconds. Hook first, hook last; whole form at most 16 bars (`max_total_bars`). Tempo band 100-160.

| Order | Label | Bars | Repeat |
|-------|-------|------|--------|
| 1 | `Intro` | 1-2 | `?` |
| 2 | `Chorus` | 2-8 | 1 |
| 3 | `Verse 1` | 2-8 | `?` |
| 4 | `Chorus` | 2-8 | `?` |
| 5 | `Tag` | 1-4 | `?` |

Default meter: Chorus two lines of `6/SuSuSu`; Verse two lines of `7/SuSuSuS`; Tag `4/SuSu`. Craft: the product or message is the hook, stated within the first two bars; the verse, when present, gives one reason; the tag is the hook's last phrase alone.

## edm-build-drop

The drop plays the chorus role. Tempo band 120-150.

| Order | Label | Bars | Repeat |
|-------|-------|------|--------|
| 1 | `Intro` | 4-32 | `?` |
| 2 | `Build` | 4-32 | 1 |
| 3 | `Drop` | 8-32 | 1 |
| 4 | `Breakdown` | 4-32 | 1 |
| 5 | `Build` | 4-32 | 1 |
| 6 | `Drop` | 8-32 | 1 |
| 7 | `Outro` | 4-32 | `?` |

Default meter: Build two lines of `6/uSuSuS`; Drop four lines of `4/SuSu`; Breakdown two lines of `8/uSuSuSuS`; Intro and Outro empty. Craft: the lyric on the drop is a short, repeatable phrase of one to four words per line; the build's lyric rises in pitch and tightens in syllable count toward the drop; the breakdown carries the song's only verse-like content. `arrangement_check.py` treats `Drop` as a chorus.

## through-composed

No repeated material. Any allowed label, at least two sections, each 2-64 bars, no upper section count. Allowed labels: `Intro`, `Verse <n>`, `Pre-Chorus <n>`, `Chorus`, `Post-Chorus`, `Bridge`, `Instrumental`, `Breakdown`, `Build`, `Drop`, `Tag`, `Outro`, `A1`, `A2`, `B`, `A3`. Tempo band 60-140.

Default meter where a section needs one: Verse four lines of `8/uSuSuSuS`; Chorus two lines of `7/SuSuSuS`; Bridge two lines of `8/uSuSuSuS`. Craft: each section introduces a new melodic idea; use it only when the brief asks for a narrative that refuses to loop (art song, theatre monologue, score cue). Unused labels are fine; reusing a label with the same lyric defeats the form, though the checker does not detect that.

## Reading a `structure_check.py` violation

- `location: structure.md:sections`, `reason: section sequence does not match form template <name>`: `observed` is the actual label sequence, `limit` the pattern. Walk both left to right and report the first divergence.
- A bars violation names the section label; cite the range from the table above.
- `location: lyrics.md:<Label>`, `reason: lyric section tag absent from structure.md`: the structure table lacks a row the lyric uses.
- `ERROR` on `form_template`: the name is missing or not one of the six above (names are case-sensitive).

## Choosing a template from the brief

| `song_type` / genre signal | Template |
|----------------------------|----------|
| `FULL_SONG`, `LYRICS_ONLY` pop, rock, country, rnb, hip-hop, worship | VCVCBC |
| Standards, musical-theatre, jazz ballad | AABA |
| Folk, story song, childrens with a repeated line | verse-refrain |
| `JINGLE`, `target_length_sec` <= 60 | jingle |
| Electronic, dance | edm-build-drop |
| `INSTRUMENTAL` cue, art song, explicit "no repeats" | through-composed |
