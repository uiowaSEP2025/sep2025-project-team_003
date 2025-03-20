from datetime import datetime
import decimal

def parseAndReturnDate(date: str):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except:
        return None
    
def parse_and_return_decimal(s: str):
    try:
        return decimal.Decimal(s)
    except:
        return None