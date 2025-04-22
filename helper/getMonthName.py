import calendar


def getMonthName(month: int) -> str:
    month_name = calendar.month_abbr[month]
    return month_name
