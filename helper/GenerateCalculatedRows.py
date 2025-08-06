from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetValueSymbol import getValueSymbol

def generateSummaryRow(
    label: str, year: int, staticMonths: list, calc_function
) -> list:
    print("Static months:", staticMonths)

    row = [
        ValueObjectModel(
            Value=label,
            isPositive=True,
            Type="",
            Symbol=""
        )
    ]

    grand_total = 0.0

    valueData = getValueSymbol(label)

    valueType = valueData["type"]
    valueSymbol = valueData["symbol"]

    for month, year in staticMonths:
        val = calc_function(year, month)
        grand_total += val

        row.append(
            ValueObjectModel(
                Value=val,
                isPositive=True,
                Type=valueType,
                Symbol=valueSymbol,
            )
        )

    row.append(
        ValueObjectModel(
            Value=grand_total,
            isPositive=True,
            Type=valueType,
            Symbol=valueSymbol,
        )
    )

    return row
