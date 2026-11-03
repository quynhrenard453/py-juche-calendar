import unittest

from py_juche_calendar import (
    GregorianDate,
    JucheDate,
    gregorian_to_juche,
    juche_to_gregorian,
)


class TestGregorianToJuche(unittest.TestCase):
    def test_epoch(self):
        self.assertEqual(gregorian_to_juche(GregorianDate(1912, 1, 1)), JucheDate(1, 1, 1))

    def test_ordinary(self):
        self.assertEqual(gregorian_to_juche(GregorianDate(2024, 3, 15)), JucheDate(113, 3, 15))

    def test_before_epoch(self):
        # 1911 is Juche year 0; 1910 is Juche year -1.
        self.assertEqual(gregorian_to_juche(GregorianDate(1911, 12, 31)), JucheDate(0, 12, 31))
        self.assertEqual(gregorian_to_juche(GregorianDate(1910, 1, 1)), JucheDate(-1, 1, 1))

    def test_method_form(self):
        self.assertEqual(GregorianDate(2000, 2, 29).to_juche(), JucheDate(89, 2, 29))


class TestJucheToGregorian(unittest.TestCase):
    def test_epoch(self):
        self.assertEqual(juche_to_gregorian(JucheDate(1, 1, 1)), GregorianDate(1912, 1, 1))

    def test_ordinary(self):
        self.assertEqual(juche_to_gregorian(JucheDate(113, 3, 15)), GregorianDate(2024, 3, 15))

    def test_before_epoch(self):
        self.assertEqual(juche_to_gregorian(JucheDate(0, 12, 31)), GregorianDate(1911, 12, 31))
        self.assertEqual(juche_to_gregorian(JucheDate(-1, 1, 1)), GregorianDate(1910, 1, 1))

    def test_method_form(self):
        self.assertEqual(JucheDate(89, 2, 29).to_gregorian(), GregorianDate(2000, 2, 29))


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_gregorian(self):
        for date in [
            GregorianDate(1912, 1, 1),
            GregorianDate(1912, 2, 29),
            GregorianDate(2000, 2, 29),
            GregorianDate(1900, 2, 28),
            GregorianDate(2023, 12, 31),
            GregorianDate(1, 1, 1),
            GregorianDate(-1, 12, 31),
        ]:
            self.assertEqual(date.to_juche().to_gregorian(), date)

    def test_round_trip_juche(self):
        for date in [
            JucheDate(1, 1, 1),
            JucheDate(1, 2, 29),
            JucheDate(89, 2, 29),
            JucheDate(-12, 2, 28),
            JucheDate(113, 12, 31),
            JucheDate(-1911, 1, 1),
        ]:
            self.assertEqual(date.to_gregorian().to_juche(), date)


class TestValidation(unittest.TestCase):
    def test_invalid_month(self):
        with self.assertRaises(ValueError):
            GregorianDate(2024, 0, 1)
        with self.assertRaises(ValueError):
            GregorianDate(2024, 13, 1)
        with self.assertRaises(ValueError):
            JucheDate(113, 0, 1)
        with self.assertRaises(ValueError):
            JucheDate(113, 13, 1)

    def test_invalid_day(self):
        with self.assertRaises(ValueError):
            GregorianDate(2023, 2, 29)  # not a leap year
        with self.assertRaises(ValueError):
            GregorianDate(2024, 4, 31)
        with self.assertRaises(ValueError):
            JucheDate(112, 2, 29)  # 2023 Gregorian, not a leap year
        with self.assertRaises(ValueError):
            JucheDate(113, 4, 31)

    def test_day_zero_and_negative(self):
        with self.assertRaises(ValueError):
            GregorianDate(2024, 1, 0)
        with self.assertRaises(ValueError):
            GregorianDate(2024, 1, -1)
        with self.assertRaises(ValueError):
            JucheDate(113, 1, 0)

    def test_leap_year_boundary(self):
        # 1900 is not a leap year (century not divisible by 400).
        with self.assertRaises(ValueError):
            GregorianDate(1900, 2, 29)
        # 2000 is a leap year.
        GregorianDate(2000, 2, 29)


class TestTypeChecking(unittest.TestCase):
    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            gregorian_to_juche(JucheDate(1, 1, 1))
        with self.assertRaises(TypeError):
            juche_to_gregorian(GregorianDate(1912, 1, 1))


if __name__ == "__main__":
    unittest.main()
