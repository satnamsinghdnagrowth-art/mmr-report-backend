import calendar


def getMonthName(month: int) -> str:
    month_name = calendar.month_abbr[month]
    return month_name


def getQuarterMonthsFromMonth(month):
    # Determine quarter based on month
    quarter = (month - 1) // 3 + 1

    # Return months in that quarter
    return list(range(3 * (quarter - 1) + 1, 3 * quarter + 1))
