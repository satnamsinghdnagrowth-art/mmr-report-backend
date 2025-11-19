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
from services.reportSection.financialHighlights.tables.RevenuebreakdownTable import (
    getRevenueBreakdownTable,
)
from helper.metricCheck import isMetricPositive
from helper.GetFileByReportId import getReportData
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
from datetime import datetime


def getISTable(year: int, months: list[int], reportType: str, section: str, reportId):
    try:
        financialData = getReportData(reportId)["Report Details"]
        financialMonth = financialData[
            "Financial Year"
        ]  # Expected format: int (e.g., 4 for April)

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
                    "Particulars",
                    f"{currentYear} Year",
                    f"{prevYear} Year",
                    "This Year vs Last Year(%)",
                    "This Year vs Last Year($)",
                    f"{year} (YTD)",
                ]
            else:
                Headers = [
                    "Particulars",
                    f"{calendar.month_abbr[currentMonths[0]]} {year}",
                    f"{calendar.month_abbr[prevMonths[0]]} {year}",
                    "This Month vs Last Month(%)",
                    "This Month vs Last Month($)",
                    f"{year} (YTD)",
                ]

            rows = []
            for entry in config["rows"]:
                valueData = getValueSymbol(entry["label"])

                valueType = valueData["type"]

                valueSymbol = valueData["symbol"]

                func = functionRegistry.get(entry["func"])

                thisMonthValue = func(
                    year=currentYear, month=currentMonths, reportId=reportId
                ).Data

                prevMonthValue = func(
                    year=prevYear, month=prevMonths, reportId=reportId
                ).Data

                # ✅ YTD months logic: span across years if needed
                latest_month = currentMonths[0]  # assumed to be the latest month
                ytd_months = []

                if latest_month >= financialMonth:
                    # Same year: financialMonth to latest_month
                    for m in range(financialMonth, latest_month + 1):
                        ytd_months.append((currentYear, m))
                else:
                    # Across two years: (finMonth to Dec of last year) + (Jan to latest_month)
                    for m in range(financialMonth, 13):
                        ytd_months.append((currentYear - 1, m))
                    for m in range(1, latest_month + 1):
                        ytd_months.append((currentYear, m))

                # ✅ Compute YTD total
                if entry["func"] == "grossProfitMargin":
                    ytdValue = func(
                        year=2025, month=[1, 2, 3, 4, 5, 6, 7,8,9,10,11,12], reportId=reportId
                    ).Data

                elif entry["func"] == "netIncomeMargin":
                    ytdValue = func(
                        year=2025, month=[1, 2, 3, 4, 5, 6, 7,8,9,10,11,12], reportId=reportId
                    ).Data

                else:
                    ytdValue = sum(
                        [
                            func(year=y, month=[m], reportId=reportId).Data
                            for y, m in ytd_months
                        ]
                    )

                print(entry["label"], ytdValue)

                result = diffrenceAndPercentage(thisMonthValue, prevMonthValue).Data

                if result["Diffrence"] == 0:
                    continue

                row = [
                    ValueObjectModel(
                        Value=entry["label"], isPositive=True, Type="", Symbol=""
                    )
                ]

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
                        Value=ytdValue,
                        isPositive=isMetricPositive(entry["label"], ytdValue),
                        Type=valueType,
                        Symbol=valueSymbol,
                    )
                )

                rows.append(row)

            tableObj = TableModel(
                Title=config["title"],
                Column=Headers,
                Rows=rows,
                TableType="Variance",
                Id=config["visualId"]
            )

            tables.append(tableObj)

        # tables.append(
        #     getRevenueBreakdownTable( year, months, reportType, reportId).Data
        # )

        return Result(
            Data=tables, Status=1, Message="Income Statement generated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getISTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    except Exception as ex:
        message = f"Error occurred at getISTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
