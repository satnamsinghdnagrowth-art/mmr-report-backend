from helper.LoadJsonData import financialDataTest
from datetime import datetime
from services.accountValues.GetKPIsData import retreiveKPIsValue
from core.models.base.ResultModel import Result
from typing import Optional, List
from helper.GetFileByReportId import getReportData


def getValues(
    mainSection: str,
    section: str,
    reportId: int,
    subSection: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[List[int]] = None,
):
    try:
        # Initialize total and data as an empty list by default
        total = 0
        data = []

        if mainSection == "KPIs":
            total = retreiveKPIsValue(section, subSection, month, year, reportId).Data

        # Normalize month value if it's zero
        if month == [0]:
            month = None

        # Check if it's a "Chart of Accounts" main section
        if mainSection == "Chart of Accounts":
            # Check PROFIT & LOSS first
            data = getReportData(reportId)["Financial Data"]
            section_income = data.get("PROFIT & LOSS", {}).get(section, {})
            income_lineitems = section_income.get("LineItems", {})

            for item_group in income_lineitems.values():
                # item_group might be Variable Cost dict → {"Data Contractors": [...]}
                if subSection in list(item_group.keys()):
                    data = item_group[subSection]  # This will be a list of dicts

                    break

            # if subSection in income_lineitems:
            #     data = income_lineitems.get(subSection, [])
            else:
                # Fallback to BalanceSheet
                data = getReportData(reportId)["Financial Data"]
                section_balance = data.get("BalanceSheet", {}).get(section, {})

                balance_lineitems = section_balance.get("LineItems", {})

                for item_group in balance_lineitems.values():
                    # item_group might be Variable Cost dict → {"Data Contractors": [...]}
                    if subSection in list(item_group.keys()):
                        data = item_group[subSection]  # This will be a list of dicts

                        break

        else:
            # Handling other sections or cases
            if subSection is None:
                financeData = getReportData(reportId)["Financial Data"]
                data = (
                    financeData.get(mainSection, {}).get(section, {}).get("Total", [])
                )

            else:
                financeData = getReportData(reportId)["Financial Data"]
                data = (
                    financeData.get(mainSection, {}).get(section, {}).get("Total", [])
                )

        # Calculate total only if we have data and year/month is provided
        if data:
            total = sum(
                entry.get("Value", 0)
                for entry in data
                if (entry.get("Year") == year)
                and (month is None or entry.get("Month") in month)
            )

        # Return the result
        return Result(Data=round(total, 0), Status=1, Message="SUCCESS")

    except Exception as ex:
        error_message = f"Error occurred in getTestValues: {ex}"
        print(f"{datetime.now()} {error_message}")
        return Result(Status=0, Message=error_message)
