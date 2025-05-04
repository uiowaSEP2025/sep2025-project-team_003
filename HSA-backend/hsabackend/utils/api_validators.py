from datetime import datetime
import decimal

def parse_and_return_date(date: str):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except:
        return None
    
def parse_and_return_decimal(s: str):
    try:
        return decimal.Decimal(s)
    except:
        return None
    
import re

def password_strength_validator(password: str) -> dict | None:
    if len(password) <= 8 or len(password) >= 16:
        return None

    has_upper_case = bool(re.search(r'[A-Z]', password))
    has_special_char = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]', password))
    has_number = bool(re.search(r'\d', password))
    if not has_upper_case:
        return None
    if not has_special_char:
        return None
    if not has_number:
        return None
    
    return password

def parse_and_return_int(value):
    try:
        res = int(value)
        return res
    except ValueError:
        return None