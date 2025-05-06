from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import decimal
from urllib.parse import urlparse
from django.core.validators import URLValidator


def isValidPhone(phone: str):
    """Validates a phone number without any separating characters.
    Example: not (123) - 456 - 7890, instead use 1234567890.
    """
    if len(phone) != 10 or not phone.isdigit():
        raise ValidationError(
            _("%(phone)s is not a valid phone number"),
            params={"phone": phone},
        )

def isNonEmpty(value: str):
    """Validates that a string is not empty."""
    if not value.strip():  # Handles spaces-only input
        raise ValidationError(
            _("%(value)s is empty"),
            params={"value": value},
        )
    
def validate_state(state: str):
    """Validates that the state is a valid U.S. state name or abbreviation."""
    states = {
        "state_names": ["Alabama", "Alaska", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
        "state_codes": ["AL", "AK", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    }
    if state not in states["state_names"] and state not in states["state_codes"]:
        raise ValidationError(
            _("%(state)s is not a valid state"),
            params={"state": state},
        )
    
def is_valid_percent(percent: decimal.Decimal):
    """Validates that a percentage is between 0 and 100."""
    if percent < 0 or percent > 100:
        raise ValidationError(
            _("%(percent)s is not a valid percentage"),
            params={"percent": percent},
        )

def is_valid_http_url(url: str):
    """Validates that a URL is a properly structured HTTP or HTTPS URL."""
    validator = URLValidator()
    validator(url)
    scheme = urlparse(url).scheme
    if scheme not in ("http", "https"):
        raise ValidationError(
            _("%(url)s does not use HTTP or HTTPS"),
            params={"url": url},
        )
