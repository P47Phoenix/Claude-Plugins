---
loaded_by: hook-writer, verse-writer, lyric-editor
level: L3
last_reviewed: 2026-10-26
---

# Genre: Folk

## Lyric conventions

- The verse carries the song. Many verses, each a stanza of a story or a catalogue of images; the chorus (when present) is a refrain, short and repeated unchanged.
- Images come from land, weather as weather, hands, tools, seasons, kin: the creek, the fiddle, the salt tin, the fence post. Natural detail is literal, never a metaphor for a feeling.
- Third person and first person both common; the narrator is allowed to be a witness ("I was there when") rather than the subject.
- Past tense is natural for story verses; a present-tense refrain pulls the story into the room.
- Archaic or regional phrasing is allowed sparingly (one per song) and never in the refrain.
- The refrain is the line a room sings back: five to eight syllables, plain words, a full rhyme or an identical repeat.

## Rhyme density

Moderate. Verses are `xAxA` or `ABCB` (ballad stanza); only lines 2 and 4 rhyme, which frees lines 1 and 3 for detail. Full rhyme on the rhymed pair; slant accepted when the rhyme word is a concrete noun. Refrains rhyme internally or repeat verbatim. Avoid `AABB` in verses; it reads as a jingle in this genre.

## Taboo moves

- Cleverness: puns, wordplay in the refrain, or a knowing wink.
- Explaining the moral. The last verse shows the consequence; it never says what it meant.
- Stacked adjectives on natural images ("the cold grey lonely hills"); one noun, one fact.
- Pop-style pre-choruses that build with shorter words; folk builds by adding a verse, not by compressing.
- Naming real people, real places, or real ballads as models; the originality policy applies to traditional titles as well.
- Cliché weather (`against the wind`, `crying in the rain`); the scan catches these, and the listener catches the rest.

## Typical section lengths

| Section | Lines | Syllables per line |
|---------|-------|--------------------|
| Verse | 4 (ballad: 4 to 8 stanzas) | 8-10, lines 1 and 3 often longer |
| Chorus / refrain | 2-4 | 5-8 |
| Bridge | 4 (often absent) | 8-10 |

`hook_max_syllables`: write to a limit of **10**; a folk refrain over ten syllables stops being singable by a room. The gate enforces the config value (default 12, or `quality.genre_overrides.folk.hook_max_syllables` when set), so a refrain at 10 or under passes either way.

## Three original example lines

```text
Carry me down to the river mouth           (refrain: 9 syllables, an instruction a room can sing)
My grandmother kept salt in a tin          (verse: kin, object, one fact)
The fiddle learned the tune before we did  (verse: the instrument as a character)
```
