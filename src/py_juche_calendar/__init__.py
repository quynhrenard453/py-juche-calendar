"""py-juche-calendar: convert between Gregorian and Juche calendar dates.

The Juche calendar numbers years from 1912, the birth year of Kim Il-sung.
Gregorian year 1912 is Juche year 1.  Years before 1912 are represented as
Juche years <= 0, which is unusual but keeps the arithmetic total.
"""

from .core import GregorianDate, JucheDate, gregorian_to_juche, juche_to_gregorian

__all__ = [
    "GregorianDate",
    "JucheDate",
    "gregorian_to_juche",
    "juche_to_gregorian",
]
