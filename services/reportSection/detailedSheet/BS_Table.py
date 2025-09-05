from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import financialDataTest
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.TableModel import TableModel
from core.models.visualsModel.ValueObject import ValueObjectModel
import calendar


def getBalanaceSheetTable(year: int, months, tableTypes: list[str], reportId):
    try:
        financialData = (
            getReportData(reportId)["Financial Data"] if reportId else financialDataTest
        )

        reportDatarange = getReportData(reportId)["Report Details"]["Data Range"]

        totalLiablities = []
        totalEquity = []

        available_months = sorted(
            [(d["Month"], d["Year"]) for d in reportDatarange],
            key=lambda x: (x[1], x[0]),  # Sort by year, then month
        )

        available_months_set = set(available_months)

        combinedRows = []
        combinedHeaders = None

        for tableIndex, tableType in enumerate(tableTypes):
            data = financialData[tableType]
            last_month = max(months)

            # Get last 6 months (month, year) pairs
            staticMonths = []
            current_month = last_month
            current_year = year

            for _ in range(6):
                if (current_month, current_year) in available_months_set:
                    staticMonths.insert(0, (current_month, current_year))
                current_month -= 1
                if current_month == 0:
                    current_month = 12
                    current_year -= 1


            # Correct headers
            headers = [tableType] + [
                f"{calendar.month_abbr[m]} {y}" for (m, y) in staticMonths
            ]

            if combinedHeaders is None:
                combinedHeaders = headers

            rows = []

            total_assets_monthly = {k: 0.0 for k in staticMonths}
            total_liablities_monthly = {k: 0.0 for k in staticMonths}

            for sectionName, sectionContent in data.items():
                sectionRows = []

                if sectionName.upper() == "CURRENT ASSETS":
                    sectionRows.insert(
                        1,
                        [
                            ValueObjectModel(
                                Value="ASSETS", isPositive=True, Type="", Symbol=""
                            )
                        ],
                    )

                elif sectionName.upper() == "CURRENT LIABILITIES":
                    sectionRows.insert(
                        1,
                        [
                            ValueObjectModel(
                                Value="LIABLITIES", isPositive=True, Type="", Symbol=""
                            )
                        ],
                    )

                sectionRows.insert(
                    1,
                    [
                        ValueObjectModel(
                            Value=sectionName, isPositive=True, Type="", Symbol=""
                        )
                    ],
                )

                sectionMonthlyTotals = {(m, y): 0.0 for (m, y) in staticMonths}


                for subSectionName, subSectionContent in sectionContent[
                    "LineItems"
                ].items():
                    
                
                    
                    monthlyTotals = {(m, y): 0.0 for (m, y) in staticMonths}

                    subSectionRows = []

                    if tableType.lower() in ["balancesheet", "equity"]:
                        subSectionRows.append(
                            [
                                ValueObjectModel(
                                    Value=subSectionName,
                                    isPositive=True,
                                    Type="",
                                    Symbol="",
                                )
                            ]
                        )

                    for itemLabel, itemData in subSectionContent.items():

                        rowData = [
                            ValueObjectModel(
                                Value=itemLabel, isPositive=True, Type="", Symbol=""
                            )
                        ]
                        monthlySum = 0.0

                        for m, y in staticMonths:
                            val = next(
                                (
                                    item["Value"]
                                    for item in itemData
                                    if item["Month"] == m and item["Year"] == y
                                ),
                                0.0,
                            )
                            monthlySum += val
                            monthlyTotals[(m, y)] += val
                            sectionMonthlyTotals[(m, y)] += val

                            rowData.append(
                                ValueObjectModel(
                                    Value=val,
                                    isPositive=True,
                                    Type="currency",
                                    Symbol="$",
                                )
                            )

                        if monthlySum == 0.0:
                            continue

                        subSectionRows.append(rowData)



                    if tableType.lower() in ["balancesheet", "equity"]:
                        grandTotal = sum(monthlyTotals.values())
                        if grandTotal != 0.0:
                            totalRow = [
                                ValueObjectModel(
                                    Value=f"Total {subSectionName}",
                                    isPositive=True,
                                    Type="",
                                    Symbol="",
                                )
                            ]
                            for m, y in staticMonths:
                                totalRow.append(
                                    ValueObjectModel(
                                        Value=monthlyTotals[(m, y)],
                                        isPositive=True,
                                        Type="currency",
                                        Symbol="$",
                                    )
                                )
                            subSectionRows.append(totalRow)
                            sectionRows.extend(subSectionRows)
                    else:
                        sectionRows.extend(subSectionRows)  


                sectionGrandTotal = sum(sectionMonthlyTotals.values())


                if sectionName.strip().upper() in [
                    "CURRENT ASSETS",
                    "NON-CURRENT ASSETS",
                ]:
                    for key in staticMonths:
                        total_assets_monthly[key] += sectionMonthlyTotals[key]

                if sectionName.strip().upper() in [
                    "CURRENT LIABILITIES",
                    "NON-CURRENT LIABILITIES",
                ]:
                    for key in staticMonths:
                        total_liablities_monthly[key] += sectionMonthlyTotals[key]

                totalSectionRow = [
                    ValueObjectModel(
                        Value=f"Total {sectionName}",
                        isPositive=True,
                        Type="",
                        Symbol="",
                    )
                ]

                for m, y in staticMonths:
                    totalSectionRow.append(
                        ValueObjectModel(
                            Value=sectionMonthlyTotals[(m, y)],
                            isPositive=True,
                            Type="currency",
                            Symbol="$",
                        )
                    )

                    if sectionName.lower() == 'equity':
                        totalEquity.append(sectionMonthlyTotals[(m, y)])

            
                sectionRows.append(totalSectionRow)


                if sectionGrandTotal == 0.0 :
                    sectionRows = []


                if (
                    sectionName == "NON-CURRENT ASSETS" 
                ):  # Only relevant for Balance Sheet
                    totalAssetsRow = [
                        ValueObjectModel(
                            Value="Total Assets", isPositive=True, Type="", Symbol=""
                        )
                    ]
                    for m, y in staticMonths:
                        totalAssetsRow.append(
                            ValueObjectModel(
                                Value=total_assets_monthly[(m, y)],
                                isPositive=True,
                                Type="currency",
                                Symbol="$",
                            )
                        )
                    sectionRows.append(totalAssetsRow)

                if (
                    sectionName == "NON-CURRENT LIABILITIES" 
                ):  
                    # Only relevant for Balance Sheet
                    totalAssetsRow = [
                        ValueObjectModel(
                            Value="Total Liablities",
                            isPositive=True,
                            Type="",
                            Symbol="",
                        )
                    ]

                    for m, y in staticMonths:
                        totalLiablities.append(total_liablities_monthly[(m, y)])
                        totalAssetsRow.append(
                            ValueObjectModel(
                                Value=total_liablities_monthly[(m, y)],
                                isPositive=True,
                                Type="currency",
                                Symbol="$",
                            )
                        )
                    sectionRows.append(totalAssetsRow)

                rows.extend(sectionRows)

            combinedRows.extend(rows)

            if sectionName.lower() == 'equity':

                totalLiabilitiesAndEquity = [ValueObjectModel(
                    Value="Total Liabilities & Equity", isPositive=True, Type="", Symbol=""
                )]
                
                for l,e in zip(totalLiablities,totalEquity):
                    total_value = l+e
                    totalLiabilitiesAndEquity.append(
                        ValueObjectModel(
                            Value=total_value,
                            isPositive=True,
                            Type="currency",
                            Symbol="$",
                        )
                    )

                combinedRows.append(totalLiabilitiesAndEquity)

        tableObj = TableModel(
            Title=tableTypes[0], Column=combinedHeaders, Rows=combinedRows
        )
        return Result(
            Data=tableObj, Status=1, Message="Combined tables generated successfully"
        )

    except ZeroDivisionError as ex:
        print(f"{datetime.now()} ZeroDivisionError: {ex}")
        return Result(Data=None, Status=0, Message=f"ZeroDivisionError: {ex}")

    except Exception as ex:
        print(f"{datetime.now()} Exception: {ex}")
        return Result(Data=None, Status=0, Message=f"Exception: {ex}")
