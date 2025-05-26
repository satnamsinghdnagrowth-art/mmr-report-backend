from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from core.models.visualsModel.ValueObject import ValueObjectModel
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from core.models.visualsModel.TableModel import TableModel
from services.reportSection.financialHighlights.tables.RevenueBreakDown import (
    getRevenueTable,
)
import calendar
from config.FunctionMaping import functionRegistry
from helper.GetValueSymbol import getValueSymbol
from helper.metricCheck import isMetricPositive
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
from datetime import datetime


# Get the sections cards
def getISTable(year: int, months: list[int], reportType: str, section: str, reportId):
    try:
        configs = SECTION_CARD_CONFIGS.get(section)
        if not configs:
            return Result(
                Data=[],
                Status=1,
                Message=f"No tables configured for section '{section}'",
            )

        tables = []

        currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
            year, months, reportType
        )

        for config in configs.get("tables"):
            if reportType.lower() == "year":
                Headers = [
                    "Income Statement",
                    f"{currentYear} Year",
                    f"{prevYear} Year",
                    "This Year vs Last Year($)",
                    "This Year vs Last Year(%)",
                ]
            else:
                Headers = [
                    "Income Statement",
                    f"{calendar.month_abbr[currentMonths[0]]} Month",
                    f"{calendar.month_abbr[prevMonths[0]]} Month",
                    "This Month vs Last Month($)",
                    "This Month vs Last Month(%)",
                ]

            rows = []
            for entry in config["rows"]:
                valueData = getValueSymbol(entry["label"])
                valueType = valueData["type"]
                valueSymbol = valueData["symbol"]

                row = [
                    ValueObjectModel(
                        Value=entry["label"], isPositive=True, Type="", Symbol=""
                    )
                ]

                func = functionRegistry.get(entry["func"])

                thisMonthValue = func(
                    year=currentYear, month=currentMonths, reportId=reportId
                ).Data
                prevMonthValue = func(
                    year=prevYear, month=prevMonths, reportId=reportId
                ).Data

                row.append(
                    ValueObjectModel(
                        Value=thisMonthValue,
                        isPositive=True,
                        Type=valueType,
                        Symbol=valueSymbol,
                    )
                )
                row.append(
                    ValueObjectModel(
                        Value=prevMonthValue,
                        isPositive=True,
                        Type=valueType,
                        Symbol=valueSymbol,
                    )
                )

                result = diffrenceAndPercentage(thisMonthValue, prevMonthValue).Data

                row.append(
                    ValueObjectModel(
                        Value=result["Diffrence"],
                        isPositive=isMetricPositive(
                            entry["label"], result["Diffrence"]
                        ),
                        Type=valueType,
                        Symbol=valueSymbol,
                    )
                )
                row.append(
                    ValueObjectModel(
                        Value=result["PercentChange"],
                        isPositive=isMetricPositive(
                            entry["label"], result["PercentChange"]
                        ),
                        Type="percentage",
                        Symbol="%",
                    )
                )

                rows.append(row)

            tableObj = TableModel(Title="Income Statement", Column=Headers, Rows=rows)
            tables.append(tableObj)

        tables.append(
            getRevenueTable(currentYear, currentMonths, reportId, reportType).Data
        )

        return Result(
            Data=tables, Status=1, Message="Revenue Card calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
