from datetime import datetime

def birthday_in_this_year(date_birthday: datetime):
    new_date = datetime(year=2023, month=date_birthday.month, day=date_birthday.day)
    return new_date