import decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from hsabackend.models.model_validators import is_valid_percent


class IsValidPercentTest(TestCase):
    def test_valid_percent(self):
        try:
            is_valid_percent(decimal.Decimal("50"))
        except ValidationError:
            self.fail("is_valid_percent raised ValidationError unexpectedly")

    def test_percent_less_than_zero(self):
        with self.assertRaises(ValidationError):
            is_valid_percent(decimal.Decimal("-1"))

    def test_percent_greater_than_hundred(self):
        with self.assertRaises(ValidationError):
            is_valid_percent(decimal.Decimal("101"))

    def test_percent_zero(self):
        try:
            is_valid_percent(decimal.Decimal("0"))
        except ValidationError:
            self.fail("is_valid_percent raised ValidationError unexpectedly")

    def test_percent_one_hundred(self):
        try:
            is_valid_percent(decimal.Decimal("100"))
        except ValidationError:
            self.fail("is_valid_percent raised ValidationError unexpectedly")
