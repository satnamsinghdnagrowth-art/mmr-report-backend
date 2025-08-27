from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetValueSymbol import getValueSymbol


from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetValueSymbol import getValueSymbol


def generateSummaryRow(
    label: str, year: int, staticMonths: list, calc_function
) -> list:
    row = [ValueObjectModel(Value=label, isPositive=True, Type="", Symbol="")]

    grand_total = 0.0

    valueData = getValueSymbol(label)

    valueType = valueData["type"]
    valueSymbol = valueData["symbol"]

    # Calculate month-wise values
    for month, yr in staticMonths:
        val = calc_function(yr, [month])
        grand_total += val

        row.append(
            ValueObjectModel(
                Value=val,
                isPositive=True,
                Type=valueType,
                Symbol=valueSymbol,
            )
        )

    # Special handling for margin values
    if label in ["Gross Profit Margin(%)", "Net Income Margin(%)"]:
        months = [m for m, _ in staticMonths]  # flat list of months
        year_for_calc = year
        grand_total = calc_function(year_for_calc, months)  # pass months directly


    # Append total/summary column
    row.append(
        ValueObjectModel(
            Value=grand_total,
            isPositive=True,
            Type=valueType,
            Symbol=valueSymbol,
        )
    )

    return row
