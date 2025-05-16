from core.models.visualsModel.ValueObject import ValueObjectModel


def generateSummaryRow(
    label: str, year: int, staticMonths: list, calc_function
) -> list:
    row = [ValueObjectModel(Value=label, isPositive=True, Type="", Symbol="")]
    grand_total = 0.0

    for m in staticMonths:
        val = calc_function(year, m)
        grand_total += val
        row.append(
            ValueObjectModel(
                Value=val,
                isPositive=True,
                Type="currency",
                Symbol="$",
            )
        )

    row.append(
        ValueObjectModel(
            Value=grand_total,
            isPositive=True,
            Type="currency",
            Symbol="$",
        )
    )

    return row
