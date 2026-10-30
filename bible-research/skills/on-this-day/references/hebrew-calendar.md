# Hebrew Calendar

How to give the Hebrew-calendar correspondence for a Gregorian date. Run this only when the user asks for it or asks about Jewish observances.

## The Rule

State the **specific year** being referenced. The Gregorian date is not fixed relative to the Hebrew calendar year over year, so a Hebrew date or festival is correct only for a stated year. Cite the specific calendar or converter used.

## Basics (gloss on first use)

- The Hebrew calendar is **lunisolar**: months follow the moon, and a leap month is added in some years so festivals stay in their seasons
- A year has 12 months, or 13 in a **leap year**. In a leap year an extra month (Adar I) is added before Adar (Adar II). Leap years fall 7 times in each 19-year cycle
- Months in order from Tishrei: Tishrei, Cheshvan, Kislev, Tevet, Shevat, Adar (Adar I and II in a leap year), Nisan, Iyar, Sivan, Tammuz, Av, Elul
- The **civil new year** (Rosh Hashanah, 1 Tishrei) is when the year number changes. The year number is the Gregorian year plus 3760 before Rosh Hashanah and plus 3761 after it, for the usual dates in autumn to winter. Always confirm with a converter; do not rely on this arithmetic alone
- A Hebrew day runs from **sunset to sunset**. A Gregorian date after dark may already be the next Hebrew date. State whether the date given is for the daytime or the evening, and the location if it matters

## Converting a Date

1. Fix the Gregorian date and the year (state the year)
2. Convert with a published converter. Hebcal (hebcal.com) provides a date converter; its JSON endpoint takes the Gregorian year, month and day. Fetch the result; do not compute it by hand
3. Record the Hebrew day, month and year, and note if the date falls after sunset
4. Identify any observance on the Hebrew date from the converter or a published calendar. Cite which

## Observances

- Name the observance and the **Hebrew date** it falls on (for example 15 Tishrei for the first day of Sukkot)
- Note differences: festivals have an extra day in the Diaspora for some observances; Israel and the Diaspora can differ. State which is meant
- Fast days, minor observances and modern observances (Yom HaShoah, Yom Ha'atzmaut) are not biblical festivals. Say so where relevant
- Biblical festivals are listed in Leviticus 23 (the appointed times). Give the verse when you mention one
- A link to the New Testament (for example John 7 and the Feast of Tabernacles) is a connection the text itself makes; label other links as **echoes** (guardrail 8)

## Citing Jewish Sources

When a Jewish source describes an observance (the Mishnah on Sukkot, for example), cite by tractate and folio or by named Midrash. Examples: Mishnah Sukkah 4:9 (the water ceremony), Mishnah Sukkah 5:1-3 (the Temple celebration). Do not write "Jewish tradition says." These texts were written after the New Testament; say so when using them to describe first-century practice (see `jewish-sources.md`).

## Entry Format

```
Gregorian date: [DAY MONTH YEAR]
Hebrew date: [DAY MONTH YEAR(5xxx)] ([daytime | begins at sunset the evening before])
Observance: [NAME, OR "none"]
Biblical basis: [REFERENCE, IF A BIBLICAL FESTIVAL]
Source: [CONVERTER OR CALENDAR, URL OPENED]
Note: [DIASPORA/ISRAEL DIFFERENCES, SUNSET ISSUES]
```

## Plain-Language Pattern

> In 2026, 13 September (daytime) falls on 2 Tishrei 5787, the second day of Rosh Hashanah. (Source: Hebcal date converter.)

Verify any date you write against the converter before using this example.

## Do Not

- Give a Hebrew date without the year
- Reuse last year's correspondence for this year
- Treat a Gregorian date as fixed to a festival
- Compute a Hebrew date by hand when a converter is available
