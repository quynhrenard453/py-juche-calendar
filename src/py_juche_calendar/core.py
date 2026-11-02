"""Core conversion logic for the Juche calendar.

Design decisions:

* The Juche year is Gregorian year minus 1911.  This makes 1912 -> 1 and
  1911 -> 0.  Negative Juche years are allowed and documented; refusing them
  would make the arithmetic less useful and would force callers to special
  case the boundary themselves.

* A date is represented by a small immutable dataclass.  We do not use
  ``datetime.date`` internally because Juche years can be <= 0, which
  ``datetime.date`` rejects.  Using plain integers keeps the conversion
  exact and dependency free.

* Leap years follow the Gregorian rule because the Juche calendar does not
  define its own month lengths.  This is the interpretation used by the
  DPRK and by every published converter I could find.
"""

from __future__ import annotations

from dataclasses import dataclass

# The Gregorian year that corresponds to Juche year 1.
_EPOCH_GREGORIAN_YEAR = 1912

# Offset between the two year numbers.
_YEAR_OFFSET = _EPOCH_GREGORIAN_YEAR - 1


def _is_leap(year: int) -> bool:
    """Return True if *year* is a Gregorian leap year.

    The rule is the standard one: divisible by 4, except centuries that are
    not divisible by 400.  We accept negative years too; Python's modulo
    operator gives the mathematically correct remainder for negative
    operands, which is what the rule needs.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(year: int, month: int) -> int:
    """Return the number of days in *month* of *year*."""
    if month == 2:
        return 29 if _is_leap(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


@dataclass(frozen=True)
class GregorianDate:
    """A calendar date in the Gregorian system.

    Fields are validated on construction.  The year may be negative, which
    represents a year before the common era; the conversion to Juche is
    still well defined.
    """

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if self.month < 1 or self.month > 12:
            raise ValueError(f"month out of range: {self.month}")
        max_day = _days_in_month(self.year, self.month)
        if self.day < 1 or self.day > max_day:
            raise ValueError(
                f"day out of range for {self.year}-{self.month:02d}: {self.day}"
            )

    def to_juche(self) -> "JucheDate":
        """Translate this Gregorian date to the Juche calendar."""
        return JucheDate(self.year - _YEAR_OFFSET, self.month, self.day)


@dataclass(frozen=True)
class JucheDate:
    """A calendar date in the Juche system.

    ``year`` is the Juche year.  Year 1 is 1912 Gregorian.  Years <= 0 are
    allowed and represent Gregorian years 1911 and earlier.
    """

    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        if self.month < 1 or self.month > 12:
            raise ValueError(f"month out of range: {self.month}")
        gregorian_year = self.year + _YEAR_OFFSET
        max_day = _days_in_month(gregorian_year, self.month)
        if self.day < 1 or self.day > max_day:
            raise ValueError(
                f"day out of range for Juche {self.year}-{self.month:02d}: {self.day}"
            )

    def to_gregorian(self) -> GregorianDate:
        """Translate this Juche date to the Gregorian calendar."""
        return GregorianDate(self.year + _YEAR_OFFSET, self.month, self.day)


def gregorian_to_juche(date: GregorianDate) -> JucheDate:
    """Convert a :class:`GregorianDate` to a :class:`JucheDate`."""
    if not isinstance(date, GregorianDate):
        raise TypeError("expected a GregorianDate")
    return date.to_juche()


def juche_to_gregorian(date: JucheDate) -> GregorianDate:
    """Convert a :class:`JucheDate` to a :class:`GregorianDate`."""
    if not isinstance(date, JucheDate):
        raise TypeError("expected a JucheDate")
    return date.to_gregorian()
