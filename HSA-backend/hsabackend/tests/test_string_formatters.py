import unittest
from datetime import date
from decimal import Decimal
from hsabackend.utils.string_formatters import (
    format_title_case, truncate_description_for_table, format_phone_number,
    format_phone_number_with_parens, format_maybe_null_date, format_address,
    format_date_to_iso_string, format_currency, format_percent, format_tax_percent
)

class TestFormattingFunctions(unittest.TestCase):

    def test_format_title_case(self):
        self.assertEqual(format_title_case("hello world"), "Hello World")
        self.assertEqual(format_title_case("HELLO"), "Hello")

    def test_truncate_description_for_table(self):
        self.assertEqual(truncate_description_for_table("This is a short description."), "This is a short description....")
        self.assertEqual(truncate_description_for_table("One two three four five six"), "One two three four five...")

    def test_format_phone_number(self):
        self.assertEqual(format_phone_number("1234567890"), "123-456-7890")

    def test_format_phone_number_with_parens(self):
        self.assertEqual(format_phone_number_with_parens("1234567890"), "(123) - 456 - 7890")

    def test_format_maybe_null_date(self):
        self.assertEqual(format_maybe_null_date(None), "N/A")
        self.assertEqual(format_maybe_null_date(date(2023, 1, 1)), date(2023, 1, 1))

    def test_format_address(self):
        self.assertEqual(format_address("123 Main St", "Anytown", "CA", "90210"),
                         "123 Main St, Anytown, CA 90210")

    def test_format_date_to_iso_string(self):
        self.assertEqual(format_date_to_iso_string(date(2022, 12, 25)), "2022-12-25")

    def test_format_currency(self):
        self.assertEqual(format_currency(Decimal("123.456")), "$123.46")
        self.assertEqual(format_currency(Decimal("100")), "$100.00")

    def test_format_percent(self):
        self.assertEqual(format_percent("30.00"), "30.00 %")

    def test_format_tax_percent(self):
        self.assertEqual(format_tax_percent("1.05"), "5%")
        self.assertEqual(format_tax_percent("1.13"), "13%")

if __name__ == "__main__":
    unittest.main()
