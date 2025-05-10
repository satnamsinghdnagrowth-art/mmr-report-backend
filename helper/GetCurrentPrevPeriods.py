def getCurrentAndPreviousPeriods(year: int, months: list[int], reportType: str):
    currentYear = year
    currentMonths = months

    if reportType.lower() == "month":
        if months[0] == 1:
            prevMonths = [12]
            prevYear = year - 1
        else:
            prevMonths = [months[0] - 1]
            prevYear = year
    else:  # reportType is "year"
        prevMonths = months
        prevYear = year - 1

    return currentYear, currentMonths, prevYear, prevMonths
