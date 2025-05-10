from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.TableModel import TableModel
from datetime import datetime
from services.calculations.GrossProfit import grossProfit
from services.calculations.Expenses import totalOperatingExpenses
from services.calculations.Ebit import EBIT
from services.calculations.EarningBefore import (
    earningBeforeInterestandTax,
    earningBeforeTax,
)
from core.models.visualsModel.ValueObject import ValueObjectModel
import calendar


# Get the sections cards
# year: int, months: list[int], reportType: str, section: str, reportId
def getTable(year:int,tableType:str):
    reportId= 12345
    
    try:
        financialData = getReportData(reportId) if reportId else financialDataTest

        incomeStatements = financialData[tableType]

        staticMonths = range(1, 13)  # or [9, 10, 11, 12] if you want specific months only

        Headers = ["Income Statement"] + [f"{calendar.month_abbr[m]} {year}" for m in staticMonths] + ["Total"]

    
        rows = []
        
        for key, value in incomeStatements.items():
            # Section Header
            rows.append([
                ValueObjectModel(
                    Value=key,
                    isPositive=True,
                    Type="",
                    Symbol="",
                )
            ])

            lineItems = value["LineItems"]

            # Initialize monthly totals for this section
            monthly_totals = {m: 0.0 for m in staticMonths}

            for k, v in lineItems.items():
                rowData = [ValueObjectModel(
                    Value=k,
                    isPositive=True,
                    Type="",
                    Symbol=""
                )]

                filtered_2024 = [item for item in v if item['Year'] == year]

                # Build row & accumulate monthly totals
                total_2024 = 0.0
                for m in staticMonths:
                    val = next((item["Value"] for item in filtered_2024 if item["Month"] == m), 0.0)
                    total_2024 += val
                    monthly_totals[m] += val

                    rowData.append(
                        ValueObjectModel(
                            Value=val,
                            isPositive=True,
                            Type="currency",
                            Symbol="$",
                        )
                    )

                rowData.append(
                    ValueObjectModel(
                        Value=total_2024,
                        isPositive=True,
                        Type="currency",
                        Symbol="$",
                    )
                )
                rows.append(rowData)

            # Add total row after line items
            totalRow = [
                ValueObjectModel(
                    Value="Total",
                    isPositive=True,
                    Type="",
                    Symbol=""
                )
            ]

            grandTotal = 0.0
            for m in staticMonths:
                month_total = monthly_totals[m]
                grandTotal += month_total
                totalRow.append(
                    ValueObjectModel(
                        Value=month_total,
                        isPositive=True,
                        Type="currency",
                        Symbol="$"
                    )
                )

            totalRow.append(
                ValueObjectModel(
                    Value=grandTotal,
                    isPositive=True,
                    Type="currency",
                    Symbol="$"
                )
            )

            rows.append(totalRow)

            if key.upper() == "COST OF SALES":

                # Add total row after line items
                grandTotal = 0.0
                
                grossProfitRow = [
                    ValueObjectModel(
                        Value="Gross Profit",
                        isPositive=True,
                        Type="",
                        Symbol=""
                    )
                ]

                
                for m in staticMonths:
                    grossProfitValue = grossProfit(year,[m],"12345").Data
                    grandTotal += grossProfitValue
                    grossProfitRow.append(
                        ValueObjectModel(
                            Value=grossProfitValue,
                            isPositive=True,
                            Type="currency",
                            Symbol="$"
                        )
                    )

                grossProfitRow.append(
                ValueObjectModel(
                    Value=grandTotal,
                    isPositive=True,
                    Type="currency",
                    Symbol="$"
                )
            )

                rows.append(grossProfitRow)


            if key.upper() == "EXPENSES":
                # Add total row after line items
                grossProfitRow = [
                    ValueObjectModel(
                        Value="Operating Profit",
                        isPositive=True,
                        Type="",
                        Symbol=""
                    )
                ]

                grandTotal = 0.0
                for m in staticMonths:
                    grossProfitValue = grossProfit(year,[m],"12345").Data - totalOperatingExpenses(year,[m],"12345").Data
                    grandTotal += grossProfitValue
                    grossProfitRow.append(
                        ValueObjectModel(
                            Value=grossProfitValue,
                            isPositive=True,
                            Type="currency",
                            Symbol="$"
                        )
                    )

                grossProfitRow.append(
                ValueObjectModel(
                    Value=grandTotal,
                    isPositive=True,
                    Type="currency",
                    Symbol="$"
                )
            )

                rows.append(grossProfitRow)

            if key.upper() == "OTHER INCOME":
                # Add total row after line items
                grossProfitRow = [
                    ValueObjectModel(
                        Value="Earnings Before Interest & Tax",
                        isPositive=True,
                        Type="",
                        Symbol=""
                    )
                ]

                grandTotal = 0.0
                for m in staticMonths:
                    grossProfitValue = EBIT(year,[m],"12345").Data
                    grandTotal += grossProfitValue
                    grossProfitRow.append(
                        ValueObjectModel(
                            Value=grossProfitValue,
                            isPositive=True,
                            Type="currency",
                            Symbol="$"
                        )
                    )

                grossProfitRow.append(
                ValueObjectModel(
                    Value=grandTotal,
                    isPositive=True,
                    Type="currency",
                    Symbol="$"
                )
            )

                rows.append(grossProfitRow)


            # Add total row after line items
                grossProfitRow = [
                    ValueObjectModel(
                        Value="Earnings Before Tax",
                        isPositive=True,
                        Type="",
                        Symbol=""
                    )
                ]

                grandTotal = 0.0
                for m in staticMonths:
                    grossProfitValue = earningBeforeTax(year,[m],"12345").Data
                    grandTotal += grossProfitValue
                    grossProfitRow.append(
                        ValueObjectModel(
                            Value=grossProfitValue,
                            isPositive=True,
                            Type="currency",
                            Symbol="$"
                        )
                    )

                grossProfitRow.append(
                ValueObjectModel(
                    Value=grandTotal,
                    isPositive=True,
                    Type="currency",
                    Symbol="$"
                )
            )

                rows.append(grossProfitRow)





                    
        tableObj = TableModel(Title="Detailed Financial Statement", Column=Headers, Rows=rows)

        return Result(
            Data=tableObj, Status=1, Message="Revenue Card calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    
    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
