import unittest
from datetime import datetime
import decimal
from hsabackend.utils.api_validators import parse_and_return_decimal, parse_and_return_date, parse_and_return_int, password_strength_validator

class UtilsTests(unittest.TestCase):

    # Test for parse_and_return_date function
    def test_parse_and_return_date_valid_date(self):
        self.assertEqual(parse_and_return_date("2025-05-04"), datetime(2025, 5, 4).date())
        
    def test_parse_and_return_date_invalid_date(self):
        self.assertIsNone(parse_and_return_date("2025-05-32"))  # Invalid day
        self.assertIsNone(parse_and_return_date("invalid-date"))  # Invalid format
        
    # Test for parse_and_return_decimal function
    def test_parse_and_return_decimal_valid(self):
        self.assertEqual(parse_and_return_decimal("123.45"), decimal.Decimal("123.45"))
        
    def test_parse_and_return_decimal_invalid(self):
        self.assertIsNone(parse_and_return_decimal("invalid-decimal"))
        self.assertIsNone(parse_and_return_decimal("123.45.67"))  # Invalid decimal format
        
    # Test for password_strength_validator function
    def test_password_strength_validator_valid(self):
        valid_password = "Valid1@password"
        self.assertEqual(password_strength_validator(valid_password), valid_password)
        
    def test_password_strength_validator_invalid_length(self):
        self.assertIsNone(password_strength_validator("Short1@"))  # Too short
        self.assertIsNone(password_strength_validator("ThisIsAVeryLongPassword1@"))  # Too long
        
    def test_password_strength_validator_missing_uppercase(self):
        self.assertIsNone(password_strength_validator("nouppercase1@"))
        
    def test_password_strength_validator_missing_special_char(self):
        self.assertIsNone(password_strength_validator("NoSpecialChar123"))
        
    def test_password_strength_validator_missing_number(self):
        self.assertIsNone(password_strength_validator("NoNumber@Password"))
        
        
    def test_parse_and_return_int_valid(self):
        self.assertEqual(parse_and_return_int("123"), 123)
        
    def test_parse_and_return_int_invalid(self):
        self.assertIsNone(parse_and_return_int("123.45"))  
        self.assertIsNone(parse_and_return_int("abc"))  