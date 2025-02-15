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
    
def validate_state(state:str, validate_by:str):
    states =  {"state_names": ["Alabama", "Alaska", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
        "state_codes": ["AL", "AK", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    }
    if state not in states[validate_by]:
        raise ValidationError(
            _("%(input)s not a valid state"),
            params={"value": input},
        )