from datetime import date
from decimal import Decimal, ROUND_HALF_UP

def format_title_case(s: str):
    words = s.split()
    title_case_words = [word.capitalize() for word in words]
    return ' '.join(title_case_words)

def truncate_description_for_table(s):
    tmp = s.split()[0:5]
    return f"{' '.join(tmp)}..."

def format_phone_number(phoneNo):
    return f"{phoneNo[0:3]}-{phoneNo[3:6]}-{phoneNo[6:10]}"

def format_phone_number_with_parens(phoneNo):
    return f"({phoneNo[0:3]}) - {phoneNo[3:6]} - {phoneNo[6:10]}"

def format_maybe_null_date(date):
    return "N/A" if date == None else date

def format_address(street_address, city, state, zipcode):
    return f"{street_address}, {city}, {state} {zipcode}"

def format_date_to_iso_string(date: date):
    return date.strftime('%Y-%m-%d')

def format_currency(amount:Decimal):
    formatted_amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Ensure two decimal places
    return f"${formatted_amount}"

def format_percent(s:str):
    return f"{s} %"