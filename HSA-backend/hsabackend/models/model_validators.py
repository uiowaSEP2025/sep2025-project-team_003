from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import decimal

def is_valid_phone(phone: str):
    """Validates a phone number without any separating characters.
    Example: not (123) - 456 - 7890, instead use 1234567890.
    """
    if len(phone) != 10 or not phone.isdigit():
        raise ValidationError(
            _("%(phone)s is not a valid phone number"),
            params={"phone": phone},
        )

def is_non_empty(value: str):
    """Validates that a string is not empty."""
    if not value.strip():  # Handles spaces-only input
        raise ValidationError(
            _("%(value)s is empty"),
            params={"value": value},
        )
    
def validate_state(state: str):
    """Validates that the state is a valid U.S. state name or abbreviation."""
    states_list = [
        "AL", "Alabama",
        "AK", "Alaska",
        "AZ", "Arizona",
        "AR", "Arkansas",
        "AS", "American Samoa",
        "CA", "California",
        "CO", "Colorado",
        "CT", "Connecticut",
        "DE", "Delaware",
        "DC", "District of Columbia",
        "FL", "Florida",
        "GA", "Georgia",
        "GU", "Guam",
        "HI", "Hawaii",
        "ID", "Idaho",
        "IL", "Illinois",
        "IN", "Indiana",
        "IA", "Iowa",
        "KS", "Kansas",
        "KY", "Kentucky",
        "LA", "Louisiana",
        "ME", "Maine",
        "MD", "Maryland",
        "MA", "Massachusetts",
        "MI", "Michigan",
        "MN", "Minnesota",
        "MS", "Mississippi",
        "MO", "Missouri",
        "MT", "Montana",
        "NE", "Nebraska",
        "NV", "Nevada",
        "NH", "New Hampshire",
        "NJ", "New Jersey",
        "NM", "New Mexico",
        "NY", "New York",
        "NC", "North Carolina",
        "ND", "North Dakota",
        "MP", "Northern Mariana Islands",
        "OH", "Ohio",
        "OK", "Oklahoma",
        "OR", "Oregon",
        "PA", "Pennsylvania",
        "PR", "Puerto Rico",
        "RI", "Rhode Island",
        "SC", "South Carolina",
        "SD", "South Dakota",
        "TN", "Tennessee",
        "TX", "Texas",
        "TT", "Trust Territories",
        "UT", "Utah",
        "VT", "Vermont",
        "VA", "Virginia",
        "VI", "Virgin Islands",
        "WA", "Washington",
        "WV", "West Virginia",
        "WI", "Wisconsin",
        "WY", "Wyoming",
    ]
    if state not in states_list:
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
