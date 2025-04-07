from datetime import date
from decimal import Decimal, ROUND_HALF_UP

def format_title_case(s: str):
    words = s.split()
    title_case_words = [word.capitalize() for word in words]
    return ' '.join(title_case_words)

def truncate_description_for_table(s):
    tmp = s.split()[0:5]
    return f"{' '.join(tmp)}..."

def format_phone_number(phone):
    return f"{phone[0:3]}-{phone[3:6]}-{phone[6:10]}"

def format_phone_number_with_parens(phone):
    return f"({phone[0:3]}) - {phone[3:6]} - {phone[6:10]}"

def format_maybe_null_date(maybe_date):
    return "N/A" if maybe_date == None else maybe_date

def format_address(street_address, city, state, zipcode):
    return f"{street_address}, {city}, {state} {zipcode}"

def format_date_to_iso_string(iso_date: date):
    return iso_date.strftime('%Y-%m-%d')

def format_currency(amount:Decimal):
    formatted_amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Ensure two decimal places
    return f"${formatted_amount}"

def format_percent(s:str):
    """Only things like 30.00 -> 30.00%"""
    return f"{s} %"

def format_tax_percent(s: str) -> str:
    percent = s.split('.')[1]
    if percent[0] == '0':
        return f"{percent[1]}%"
    return f"{percent}%"

