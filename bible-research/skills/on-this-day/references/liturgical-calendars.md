# Liturgical Calendars

How to find what the church calendar marks on a given date, and how to cite it.

## The Rule

Cite the specific calendar or source for every entry. "The church marks..." is not a citation. Name the calendar (Revised Common Lectionary, Book of Common Prayer calendar, Roman Catholic General Roman Calendar, and so on), and name the year when the date moves.

## Calendars to Use

| Calendar | Used by | Notes |
|---|---|---|
| **Revised Common Lectionary (RCL)** | Many Protestant churches (Lutheran, Reformed, Methodist, Anglican, others) | A three-year cycle of readings (Years A, B, C). The Sunday readings follow the church year. Published by the Consultation on Common Texts (1992) |
| **Western liturgical calendar (General Roman Calendar)** | Roman Catholic Church | Feasts, memorials and optional memorials; saints' days |
| **Church of England / Book of Common Prayer calendars** | Anglican churches | Different editions and provinces differ. Name the edition and province |
| **Lutheran calendars** (for example the Lutheran Service Book calendar) | Lutheran churches | Name the book; commemorations vary |
| **Eastern Orthodox calendar** | Orthodox churches | Many use the Julian calendar for fixed feasts, so the same feast falls on a different Gregorian date. State which calendar (Julian or Revised Julian) |
| **Protestant observances** (Reformation Day, Thanksgiving, Epiphany observances) | Various | Name the church or denomination that observes them |

If a date has no entry in a recognized calendar, say so. Do not make one up.

## Movable and Fixed Dates

- **Fixed feasts** fall on the same date each year (Christmas, 25 December; Epiphany, 6 January)
- **Movable feasts** depend on the date of Easter (Ash Wednesday, Palm Sunday, Ascension, Pentecost). Compute Easter first, then count

### Computing Western Easter (Gregorian)

The Meeus/Jones/Butcher algorithm for year Y:

```
a = Y mod 19
b = Y div 100          c = Y mod 100
d = b div 4            e = b mod 4
f = (b + 8) div 25
g = (b - f + 1) div 3
h = (19a + b - d - g + 15) mod 30
i = c div 4            k = c mod 4
l = (32 + 2e + 2i - h - k) mod 7
m = (a + 11h + 22l) div 451
month = (h + l - 7m + 114) div 31
day   = ((h + l - 7m + 114) mod 31) + 1
```

Worked check: Y = 2026 gives month 4, day 5 (5 April 2026). Always confirm a computed date against a published table before use. Orthodox Easter uses the Julian computus and differs; use a published table for it.

### Lectionary Year

The RCL year runs from the First Sunday of Advent. Take the calendar year in which Advent begins and divide by 3: remainder 0 is **Year A**, remainder 1 is **Year B**, remainder 2 is **Year C**. (Advent 2022 began Year A, Advent 2024 began Year C, and Advent 2026 begins Year B.) Check the year against a published RCL table (the Vanderbilt Divinity Library hosts the Revised Common Lectionary readings at lectionary.library.vanderbilt.edu).

## How to Verify

1. Fetch the calendar or the lectionary page for the date
2. Confirm the entry text names the observance and the date
3. For a saint's day, name the calendar (for example the General Roman Calendar) and say whether it is an obligatory memorial, an optional memorial or a feast
4. For a lectionary entry, give the Sunday or day name, the year (A, B or C), and the readings by reference (book, chapter, verse)
5. Check that the day is not displaced by a higher observance

## Entry Format

```
Calendar: [NAME, EDITION OR PROVINCE WHERE RELEVANT]
Observance: [NAME]
Rank: [feast / memorial / optional memorial / commemoration / ordinary]
Date: [DATE, YEAR]
Readings: [REFERENCES, IF LECTIONARY]
Source: [PAGE OR URL OPENED]
```

## Notes

- A saint's day marks a commemoration, not necessarily the date of death or birth. Do not present it as a historical date unless the source says so
- Some entries mark traditional dates with no documented basis; label them traditional and do not merge them with documented events
