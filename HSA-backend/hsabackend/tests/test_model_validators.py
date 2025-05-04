from django.test import TestCase
from django.core.exceptions import ValidationError
import decimal
from hsabackend.models.model_validators import isValidPhone, isNonEmpty, validate_state, is_valid_percent

class IsValidPhoneTest(TestCase):
    def test_valid_phone(self):
        try:
            isValidPhone("1234567890")
        except ValidationError:
            self.fail("isValidPhone raised ValidationError unexpectedly")

    def test_invalid_phone_length(self):
        with self.assertRaises(ValidationError):
            isValidPhone("12345")

    def test_invalid_phone_non_digit(self):
        with self.assertRaises(ValidationError):
            isValidPhone("12345678a0")

class IsNonEmptyTest(TestCase):
    def test_non_empty_value(self):
        try:
            isNonEmpty("Valid Value")
        except ValidationError:
            self.fail("isNonEmpty raised ValidationError unexpectedly")

    def test_empty_value(self):
        with self.assertRaises(ValidationError):
            isNonEmpty("   ")  # Spaces only

    def test_empty_string(self):
        with self.assertRaises(ValidationError):
            isNonEmpty("")

class ValidateStateTest(TestCase):
    def test_valid_state_name(self):
        try:
            validate_state("California")
        except ValidationError:
            self.fail("validate_state raised ValidationError unexpectedly")

    def test_valid_state_code(self):
        try:
            validate_state("CA")
        except ValidationError:
            self.fail("validate_state raised ValidationError unexpectedly")

    def test_invalid_state(self):
        with self.assertRaises(ValidationError):
            validate_state("InvalidState")

    
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
