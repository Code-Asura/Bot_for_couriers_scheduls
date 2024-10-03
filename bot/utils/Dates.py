from datetime import datetime, timedelta
from .lexicon import ruMonths, ruWeekdays

class Dates:
    def __init__(self, msg: str | None = None) -> None:
        self.msg = msg
        
    # Сегодня
    def today() -> str:
        today = datetime.now().date()
        weekday = ruWeekdays[today.weekday()]
        month = ruMonths[today.month]
        current_date = datetime.now().strftime(f"{weekday}, {today.strftime('%d')} {month} %Y г.")
        dates = today.strftime("%d.%m.%Y")
        return [current_date, dates]

    # Завтра
    def tomorrow_day() -> str:
        tomorrow = datetime.now().date() + timedelta(days=1)
        weekday = ruWeekdays[tomorrow.weekday()]
        month = ruMonths[tomorrow.month]
        tomorrows_date = datetime.now().strftime(f"{weekday}, {tomorrow.strftime('%d')} {month} %Y г.") 
        dates = tomorrow.strftime("%d.%m.%Y")
        return [tomorrows_date, dates]

    # Послезавтра
    def after_tomorrow_day() -> str:
        after_tomorrow = datetime.now().date() + timedelta(days=2)
        weekday = ruWeekdays[after_tomorrow.weekday()]
        month = ruMonths[after_tomorrow.month]
        after_tomorrows_date = datetime.now().strftime(f"{weekday}, {after_tomorrow.strftime('%d')} {month} %Y г.") 
        dates = after_tomorrow.strftime("%d.%m.%Y")

        return [after_tomorrows_date, dates]

    # Преобразование
    def transfomation(str_date: str) -> str:
        parse_date = datetime.strptime(str_date, "%d.%m.%Y").date()
        weekday = ruWeekdays[parse_date.weekday()]
        month = ruMonths[parse_date.month]
        another_date = datetime.now().strftime(
            f"{weekday}, {parse_date.strftime('%d')} {month} {parse_date.strftime('%Y')} г."
        )

        return another_date
        