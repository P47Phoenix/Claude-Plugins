# Claim Extraction

How to find the claims in an artifact, including the ones it never states outright, and how to tell poetic license from doctrinal error.

## Goal

Turn the artifact into a numbered list of checkable claims. A claim is something that could be true or false: it says what Scripture says, what happened, what a word means, what God is like, or what an authority said.

## Hard Rule: Paraphrase, Never Reproduce

- Paraphrase every claim in your own words
- Quote at most a **short identifying phrase** (a few words) to help the user find it
- **Songs:** give title, songwriter, and line **position** ("verse 2, line 3", "chorus, line 1"). Do not give the words
- Articles, posts, transcripts: give a section, paragraph number or timestamp, not the paragraph
- Never reproduce a block of the artifact, even to "show" the claim
- **Attribution:** if the songwriter, author, speaker or date is not given in what the user supplied, write "not given". Do not guess or fill it in from memory (guardrail 1)

## Claim Kinds

Tag each claim with one kind:

| Kind | Example shape |
|---|---|
| **Scripture citation** | The artifact cites or alludes to a verse and says what it means |
| **Historical assertion** | A date, person, event or custom |
| **Language or etymology** | "The Greek/Hebrew word really means..." |
| **Doctrinal assertion** | A statement about God, Christ, the Spirit, salvation, the church |
| **Quoted authority** | "Spurgeon said...", "the early church taught..." |
| **Statistic or count** | "appears 365 times", "7 of 10 pastors" |

## Finding Implicit Claims

Many claims are never stated; they are assumed. Look for:

- **A chorus that implies a doctrine.** A repeated line about God "pouring out wrath on the Son" assumes a view of the atonement. List the assumed doctrine as a claim, tagged doctrinal
- **A post that assumes a disputed date.** A meme about "Jesus was born on December 25" assumes a date. List the date
- **A word study left unstated.** A phrase like "the original word for love" assumes a lexical claim. List it
- **A scripture allusion** without a reference. Identify the likely verse and say it is an allusion; if you cannot identify it, say so
- **An appeal to "the early church" or "Jewish tradition"** with no source. List the appeal and mark the source as missing
- **Cause-and-effect leaps.** "Because X, God will Y." List the implied promise and the verse it relies on
- **Presupposed context.** A claim that only works if the verse is read a certain way

For each implicit claim write a short line: "The song assumes that..." or "The post assumes that..."

## Poetic License vs Doctrinal Error

Do not treat poetry as a lecture. Before listing a line as a doctrinal claim, ask:

1. Is it **figurative**? ("The mountains bow", "my chains fell off") Figures are not claims about how the world works. Do not list them as errors (guardrail 11)
2. Is it a **biblical image** the text itself uses? (Light, rock, shepherd, bride) List it only if the artifact stretches it past what the text says
3. Does it **assert something specific** that could contradict the text? ("God turned his back on the Son") That is a claim; list it
4. Is it a **traditional phrase** that different traditions read differently? Mark it **contested**, not wrong (guardrail 10)

Prefer the charitable reading first. Flag a line only when no reasonable reading is faithful to the text, or when the artifact itself leans on the doubtful reading.

## Separating Fact-Claims from Devotion

| Lean toward devotional | Lean toward fact-claim |
|---|---|
| "Lord, I want to be near you" | "God cannot look at sin, so he left Jesus" |
| "Your love is deeper than the sea" | "The Greek word for love in John 21 shows..." |
| "I surrender all" | "Jewish grooms always did X when engaged" |

If a line could be both, list it as a claim and note it may be devotional; the verifier will not flag metaphor.

## Output

A numbered list. For each claim:

```
[N]. [KIND] - [PARAPHRASE OF THE CLAIM, ONE SENTENCE]
     Position: [verse 2, line 3 | paragraph 4 | 12:40]
     Explicit or implicit: [explicit | implicit - assumes ...]
     Note: [DEVOTIONAL? CONTESTED? NONE]
```

At the end, list anything you could not parse (garbled lyrics, an unclear sentence) rather than guessing.
