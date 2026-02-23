from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.TableModel import TableModel
from datetime import datetime
from services.calculations.NetIncome import netIncome
from helper.GetValueSum import getValueSum
from helper.GenerateRowsData import (
    generateChangeRow,
    calculateSectionTotal,
    generateChangeValueRow,
)
from core.models.visualsModel.ValueObject import ValueObjectModel
from helper.GetCurrentPrevPeriods import getCurrentAndPreviousPeriods
import calendar
from core.models.base.SourceModel import SourceDataTypes
from helper.GetFinancialData import getFinancialData

# Generate Cash flow Table
def getCashFlowTable(year: int, months, reportId, tableType="CashFlow Statements"):
    try:
        financialData = getFinancialData(reportId, SourceDataTypes.Actuals)
        reportDatarange = getReportData(reportId)["Report Details"]["Data Range"]

        available_months = sorted(
            [(d["Month"], d["Year"]) for d in reportDatarange],
            key=lambda x: (x[1], x[0]),  # Sort by year, then month
        )

        # Use last 6 months from available months
        staticMonths = available_months[-6:] if len(available_months) >= 6 else available_months
        available_months_set = set(available_months)

        Headers = [tableType] + [
            f"{calendar.month_abbr[m]} {y}" for m, y in staticMonths
        ]

        rows = []

        # ---------------- Operating Activities ----------------
        rows.append(
            [
                ValueObjectModel(
                    Value="OPERATING ACTIVITIES", isPositive=True, Type="", Symbol=""
                )
            ]
        )

        operating_rows = []

        # Net Income row
        row = [
            ValueObjectModel(Value="Net Income", isPositive=True, Type="", Symbol="")
        ]
        for m, y in staticMonths:
            currentYear, currentMonths, prevYear, prevMonths = (
                getCurrentAndPreviousPeriods(y, [m], "month")
            )
            thisMonth = netIncome(currentYear, currentMonths, reportId).Data
            row.append(
                ValueObjectModel(
                    Value=thisMonth, isPositive=True, Type="currency", Symbol="$"
                )
            )

        operating_rows.append(row)

        row = [
            ValueObjectModel(Value="Depreciation", isPositive=True, Type="", Symbol="")
        ]
        for m, y in staticMonths:
            totalDep = getValueSum(
                financialData,
                ["PROFIT & LOSS", "EXPENSES", "Classification", "Depreciation"],
                y,
                [m],
            ).Data
            row.append(
                ValueObjectModel(
                    Value=totalDep, isPositive=True, Type="currency", Symbol="$"
                )
            )

        operating_rows.append(row)

        # Operating changes (with isAsset flag)
        change_rows_config = [
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
        rows.append(
            calculateSectionTotal(operating_rows, staticMonths, "Operating Activities")
        )

        rows.append(
            [
                ValueObjectModel(
                    Value="INVESTING ACTIVITIES", isPositive=True, Type="", Symbol=""
                )
            ]
        )

        investing_rows = []

        FArow = generateChangeValueRow(
            "Change in Fixed Assets",
            financialData,
            ["BalanceSheet", "NON-CURRENT ASSETS", "Classification", "Fixed Assets"],
            year,
            staticMonths,
            isAsset=True,  # Fixed Assets is also an asset
        )

        DArow = []

        for m, y in staticMonths:
            totalDA = getValueSum(
                financialData,
                ["PROFIT & LOSS", "EXPENSES", "Classification", "Depreciation"],
                y,
                [m],
            ).Data
            DArow.append(totalDA)

        DEProw = []

        for m, y in staticMonths:
            totalDep = getValueSum(
                financialData,
                ["PROFIT & LOSS", "COST OF SALES", "Classification", "Depreciation"],
                y,
                [m],
            ).Data
            DEProw.append(totalDep)

        row = [
            ValueObjectModel(
                Value="Change in Fixed Assets", isPositive=True, Type="", Symbol=""
            )
        ]

        for FA, DEP, DA in zip(FArow, DEProw, DArow):
            changeInFA = FA - (DEP + DA)

            row.append(
                ValueObjectModel(
                    Value=changeInFA, isPositive=True, Type="currency", Symbol="$"
                )
            )

        investing_rows.append(row)

        rows.extend(investing_rows)

        rows.append(
            calculateSectionTotal(investing_rows, staticMonths, "Investing Activities")
        )

        # ---------------- Financing Activities ----------------
        rows.append(
            [
                ValueObjectModel(
                    Value="FINANCING ACTIVITIES", isPositive=True, Type="", Symbol=""
                )
            ]
        )
        financing_rows = []

        row = [
            ValueObjectModel(
                Value="Change In other Equity", isPositive=True, Type="", Symbol=""
            )
        ]

        for month, year in staticMonths:
            currentYear, currentMonths, prevYear, prevMonths = (
                getCurrentAndPreviousPeriods(year, [month], "month")
            )

            chaneInOEQ = (
                getValueSum(
                    financialData,
                    [
                        "EQUITY",
                        "EQUITY",
                        "Classification",
                        "Other Equity",
                    ],
                    currentYear,
                    currentMonths,
                ).Data
                - getValueSum(
                    financialData,
                    [
                        "EQUITY",
                        "EQUITY",
                        "Classification",
                        "Other Equity",
                    ],
                    prevYear,
                    prevMonths,
                ).Data
            )

            chaneInRE = (
                getValueSum(
                    financialData,
                    [
                        "EQUITY",
                        "EQUITY",
                        "Classification",
                        "Retained Earnings",
                    ],
                    currentYear,
                    currentMonths,
                ).Data
                - getValueSum(
                    financialData,
                    [
                        "EQUITY",
                        "EQUITY",
                        "Classification",
                        "Retained Earnings",
                    ],
                    prevYear,
                    prevMonths,
                ).Data
            )

            netinc = getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Current Earnings",
                ],
                prevYear,
                prevMonths,
            ).Data

            if month == 1:
                netIncomeValue = netinc
            else:
                netIncomeValue = 0

            result = chaneInOEQ + (chaneInRE - netIncomeValue)

            row.append(
                ValueObjectModel(
                    Value=result, isPositive=True, Type="currency", Symbol="$"
                )
            )

        financing_rows.append(row)

        # Generic implementation - define all finance change rows in one place
        finance_change_rows = [
            (
                "Change in long Term Debt",
                [
                    "BalanceSheet",
                    "NON-CURRENT LIABILITIES",
                    "Classification",
                    "Long-term Debt",
                ],
                False,
            ),
            (
                "Change in Short Term Debt",
                [
                    "BalanceSheet",
                    "NON-CURRENT LIABILITIES",
                    "Classification",
                    "Short-term Debt",
                ],
                False,
            ),
            # Add more finance change rows as needed
            # (
            #     "Change in Share Capital",
            #     [
            #         "BalanceSheet",
            #         "EQUITY",
            #         "Classification",
            #         "Share Capital",
            #     ],
            #     False,
            # ),
        ]

        # Generic processing loop
        for title, keys, isAsset in finance_change_rows:
            row = generateChangeRow(
                title, financialData, keys, year, staticMonths, isAsset=isAsset
            )
            financing_rows.append(row)

        rows.extend(financing_rows)

        rows.append(
            calculateSectionTotal(financing_rows, staticMonths, "Financing Activities")
        )

        financing_rows = []

        finance_change_rows = [
            (
                "Change in Cash & Equivalent",
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "Classification",
                    "Cash & Equivalents",
                ],
                False,
            ),
        ]

        for title, keys, isAsset in finance_change_rows:
            row = generateChangeRow(
                title, financialData, keys, year, staticMonths, isAsset
            )

            financing_rows.append(row)

        rows.extend(financing_rows)

        OpenRows = [
            ValueObjectModel(
                Value="Cash & Equivalents, Opening Balance",
                isPositive=True,
                Type="currency",
                Symbol="$",
            )
        ]

        closeRows = [
            ValueObjectModel(
                Value="Cash & Equivalents, Closing Balance",
                isPositive=True,
                Type="currency",
                Symbol="$",
            )
        ]
        for m, y in staticMonths:
            currentYear, currentMonths, prevYear, prevMonths = (
                getCurrentAndPreviousPeriods(y, [m], "month")
            )

            result = getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "Classification",
                    "Cash & Equivalents",
                ],
                prevYear,
                prevMonths,
            ).Data
            result2 = getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "Classification",
                    "Cash & Equivalents",
                ],
                y,
                [m],
            ).Data
            OpenRows.append(
                ValueObjectModel(
                    Value=result, isPositive=True, Type="currency", Symbol="$"
                )
            )
            closeRows.append(
                ValueObjectModel(
                    Value=result2, isPositive=True, Type="currency", Symbol="$"
                )
            )

        rows.extend([OpenRows, closeRows])

        # ---------------- Final Table ----------------
        tableObj = TableModel(Title="", Column=Headers, Rows=rows, Id="CASH_FLOW_TABLE")

        return Result(
            Data=tableObj,
            Status=1,
            Message="Cash Flow Statement calculated successfully",
        )

    except Exception as ex:
        message = f"Error occurred at getCashFlowTable: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
