from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.TableModel import TableModel
from datetime import datetime
from services.calculations.NetIncome import netIncome
from helper.GetValueSum import getValueSum
from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
import calendar


def generateChangeRow(title, financialData, pathKeys, year, staticMonths, isAsset):
    row = [ValueObjectModel(Value=title, isPositive=True, Type="", Symbol="")]

    for m in staticMonths:
        currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
            year, [m], "month"
        )


        sumThis = getValueSum(financialData, pathKeys, currentYear, currentMonths).Data
        sumPrev = getValueSum(financialData, pathKeys, prevYear, prevMonths).Data

        result = sumThis - sumPrev

        if isAsset:
            result = -result  # reverse for asset

        row.append(
            ValueObjectModel(
                Value=result,
                isPositive=True,
                Type="currency",
                Symbol="$",
            )
        )

    return row


def calculateSectionTotal(section_rows, staticMonths):
    totals = []
    for col_index in range(1, len(staticMonths) + 1):
        col_sum = 0
        for row in section_rows:
            if len(row) > col_index:
                val = row[col_index].Value
                if isinstance(val, (int, float)):
                    col_sum += val
        totals.append(col_sum)

    total_row = (
        [ValueObjectModel(Value="Total", isPositive=True, Type="", Symbol="")]
        + [
            ValueObjectModel(
                Value=val, isPositive=(val >= 0), Type="currency", Symbol="$"
            )
            for val in totals
        ]
        
    )
    return total_row


def getCashFlowTable(year: int, tableType="CashFlow Table", reportId=12345):
    try:
        financialData = getReportData(reportId) if reportId else financialDataTest

        staticMonths = range(1, 13)

        Headers = (
            [tableType]
            + [f"{calendar.month_abbr[m]} {year}" for m in staticMonths]
        )

        rows = []

        # ---------------- Operating Activities ----------------
        rows.append(
            [
                ValueObjectModel(
                    Value="OPERATING Activities", isPositive=True, Type="", Symbol=""
                )
            ]
        )

        operating_rows = []

        # Net Income row
        row = [
            ValueObjectModel(Value="Net Income", isPositive=True, Type="", Symbol="")
        ]
        for m in staticMonths:
            currentYear, currentMonths, prevYear, prevMonths = (
                getCurrentAndPreviousPeriods(year, [m], "month")
            )
            thisMonth = netIncome(currentYear, currentMonths, reportId).Data
            row.append(
                ValueObjectModel(
                    Value=thisMonth, isPositive=True, Type="currency", Symbol="$"
                )
            )


        operating_rows.append(row)

        # Operating changes (with isAsset flag)
        change_rows_config = [
            # LIABILITIES (isAsset=False)
            (
                "Change in Other Current Liabilities",
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Other Current Liabilities",
                ],
                False,
            ),
            (
                "Change in Accounts Payable",
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Accounts Payable",
                ],
                False,
            ),
            # ASSETS (isAsset=True)
            (
                "Change in Accounts Receivable",
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "Classification",
                    "Accounts Receivable",
                ],
                True,
            ),
            (
                "Change in Other Current Assets",
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "Classification",
                    "Other Current Assets",
                ],
                True,
            ),
        ]

        for title, keys, isAsset in change_rows_config:
            row = generateChangeRow(
                title, financialData, keys, year, staticMonths, isAsset=isAsset
            )
            operating_rows.append(row)

        rows.extend(operating_rows)
        rows.append(calculateSectionTotal(operating_rows, staticMonths))

        # ---------------- Investing Activities ----------------
        rows.append(
            [
                ValueObjectModel(
                    Value="INVESTING Activities", isPositive=True, Type="", Symbol=""
                )
            ]
        )
        investing_rows = []

        row = generateChangeRow(
            "Change in Fixed Assets",
            financialData,
            ["BalanceSheet", "NON-CURRENT ASSETS", "Classification", "Fixed Assets"],
            year,
            staticMonths,
            isAsset=True,  # Fixed Assets is also an asset
        )
        
        investing_rows.append(row)

        rows.extend(investing_rows)
        rows.append(calculateSectionTotal(investing_rows, staticMonths))

        # ---------------- Financing Activities ----------------
        rows.append(
            [
                ValueObjectModel(
                    Value="FINANCING ACTIVITIES", isPositive=True, Type="", Symbol=""
                )
            ]
        )
        financing_rows = []

        finance_change_rows = [
            (
                "Change in Other Equity",
                ["EQUITY", "EQUITY", "Classification", "Other Equity"],
                False,
            ),
            (
                "Change in Short Term Debt",
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Short-term Debt",
                ],
                False,
            ),
        ]

        for title, keys, isAsset in finance_change_rows:
            row = generateChangeRow(
                title, financialData, keys, year, staticMonths, isAsset=isAsset
            )
           
            financing_rows.append(row)

        rows.extend(financing_rows)
        rows.append(calculateSectionTotal(financing_rows, staticMonths))

        financing_rows = []

        finance_change_rows = [
            (
                "Change in Cash & Equivalent",
                ["BalanceSheet", "CURRENT ASSETS", "Classification", "Cash"],
                True,
            ),
            
        ]

        for title, keys, isAsset in finance_change_rows:
            row = generateChangeRow(
                title, financialData, keys, year, staticMonths, isAsset=isAsset
            )
            
            financing_rows.append(row)
         
        
        rows.extend(financing_rows)


        OpenRows = [ ValueObjectModel(
                    Value="Cash & Equivalents, Opening Balance", isPositive=True, Type="", Symbol=""
                )] 
        
        closeRows = [ ValueObjectModel(
                    Value="Cash & Equivalents, Closing Balance", isPositive=True, Type="", Symbol=""
                )] 
        for m in staticMonths:

            currentYear, currentMonths, prevYear, prevMonths = getCurrentAndPreviousPeriods(
                year, [m], "month"
            )

            result = getValueSum(financialData,["BalanceSheet", "CURRENT ASSETS", "Classification", "Cash"],prevYear,prevMonths).Data
            result2 = getValueSum(financialData,["BalanceSheet", "CURRENT ASSETS", "Classification", "Cash"],year,[m]).Data
            OpenRows.append(ValueObjectModel(
                    Value=result, isPositive=True, Type="", Symbol=""
                ))
            closeRows.append(ValueObjectModel(
                    Value=result2, isPositive=True, Type="", Symbol=""
                ))

        rows.extend([OpenRows,closeRows])



        # ---------------- Final Table ----------------
        tableObj = TableModel(Title="CASH FLOW STATEMENT", Column=Headers, Rows=rows)

        return Result(
            Data=tableObj,
            Status=1,
            Message="Cash Flow Statement calculated successfully",
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getCashFlowTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getCashFlowTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

