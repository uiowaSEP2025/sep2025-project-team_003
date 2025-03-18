from datetime import datetime

def parseAndReturnDate(date: str):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except:
        return None