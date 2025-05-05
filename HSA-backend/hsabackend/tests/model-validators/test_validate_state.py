from django.core.exceptions import ValidationError
from django.test import TestCase

from hsabackend.models.model_validators import validate_state


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
