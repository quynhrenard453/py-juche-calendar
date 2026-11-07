# py-juche-calendar

Translate dates between the Gregorian calendar and North Korea's Juche calendar, whose epoch is 1912 (Juche year 1).

```python
from py_juche_calendar import GregorianDate, JucheDate, gregorian_to_juche, juche_to_gregorian

# Gregorian -> Juche
g = GregorianDate(2024, 3, 15)
j = gregorian_to_juche(g)          # JucheDate(year=113, month=3, day=15)

# Juche -> Gregorian
back = juche_to_gregorian(j)       # GregorianDate(year=2024, month=3, day=15)

# The same conversion is available as a method on either date type.
assert g.to_juche() == j
assert j.to_gregorian() == back
```

## Why this exists

The Juche year is simply `Gregorian year - 1911`, so the arithmetic is trivial. The problem is that most converters silently reject dates before 1912, or they assume a single direction. This library keeps the arithmetic total: Juche year 0 is 1911 Gregorian, and negative Juche years are valid. That choice makes round-tripping exact across the epoch and avoids forcing callers to special-case the boundary themselves.

The trade-off is that a `JucheDate` with a non-positive year is not something you will see in official DPRK usage. It is documented here, tested, and supported because it is the only way to make the conversion a total function on dates.

## The awkward edge

Leap years follow the Gregorian rule, not a Juche-specific one. This matters for dates like 1900-02-29, which does not exist under the Gregorian rule (1900 is not a leap year) and therefore cannot be represented. The constructors raise `ValueError` for impossible dates, so you get an error at the point where the invalid date is created, not later during conversion.

## API

The package exports four names:

- `GregorianDate(year, month, day)` — immutable; validates month and day.
- `JucheDate(year, month, day)` — immutable; validates month and day against the corresponding Gregorian year.
- `gregorian_to_juche(date)` — accepts a `GregorianDate`, returns a `JucheDate`.
- `juche_to_gregorian(date)` — accepts a `JucheDate`, returns a `GregorianDate`.

Both date classes also provide `.to_juche()` and `.to_gregorian()` methods that do the same work without the type check.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

