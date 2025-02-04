from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def isValidPhone(phone:str) -> bool:
    """validates a phone number without any separating parentheses 
    ex: not (123) - 456 - 7890, instead use 1234567890
    """
    if len(phone) != 10:
        raise ValidationError(
            _("%(phone)s is not a valid length"),
            params={"value": phone},
        )

def isNonEmpty(input: str) -> bool:
    if len(input) == 0:
        raise ValidationError(
            _("%(input)s is empty"),
            params={"value": input},
        )