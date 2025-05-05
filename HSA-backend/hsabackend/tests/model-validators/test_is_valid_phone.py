from django.core.exceptions import ValidationError
from django.test import TestCase

from hsabackend.models.model_validators import is_valid_phone, is_non_empty


class IsValidPhoneTest(TestCase):
    def test_valid_phone(self):
        try:
            is_valid_phone("1234567890")
        except ValidationError:
            self.fail("isValidPhone raised ValidationError unexpectedly")

    def test_invalid_phone_length(self):
        with self.assertRaises(ValidationError):
            is_valid_phone("12345")

    def test_invalid_phone_non_digit(self):
        with self.assertRaises(ValidationError):
            is_valid_phone("12345678a0")

class IsNonEmptyTest(TestCase):
    def test_non_empty_value(self):
        try:
            is_non_empty("Valid Value")
        except ValidationError:
            self.fail("isNonEmpty raised ValidationError unexpectedly")

    def test_empty_value(self):
        with self.assertRaises(ValidationError):
            is_non_empty("   ")  # Spaces only

    def test_empty_string(self):
        with self.assertRaises(ValidationError):
            is_non_empty("")
