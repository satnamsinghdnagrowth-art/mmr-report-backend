from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS

from helper.LoadJsonData import financialDataTest
from services.visuals.charts.retrieveChart import retrieveChart
from services.reportSection.financialHighlights.charts.RevenueBreakdown import (
    getRevenueBreakdownChart,
)
from helper.GetValueSum import getValueSum
from helper.GetFileByReportId import getReportData
from services.calculations.Revenue import totalRevenue
from services.calculations.Expenses  import totalOperatingExpenses,directExpenses
from services.calculations.OtherIncome import otherIncome
from services.calculations.CashFlowActivities import getOperatingActivitiesCashFlow
from services.calculations.CurrentAssestAndLiabilities import (
    getTotalCurrentLiabilities,
    getTotalCurrentAssets,
)
from services.calculations.DiffrenceCalculation import diffrenceAndPercentage
from services.calculations.NetProfit import netProfit
from helper.GetValueSum import getValueSum
from datetime import datetime

def get_change(data, section, category, subcategory, year1, year2, month):
    return (getValueSum(data, ["BalanceSheet", section, category, subcategory], year1, [month]).Data
        - getValueSum(data, ["BalanceSheet", section, category, subcategory], year2, [month]).Data)



# Get the sections cards
def getEACharts(year: int, months: list[int], reportId=12345):
    

    try:
        financialData = getReportData(reportId) if reportId else financialDataTest

        totalRev = totalRevenue(year, months, reportId).Data
        totalOE = totalOperatingExpenses(year, months, reportId).Data
        totalDE = directExpenses(year, months, reportId).Data
        otherInc = otherIncome(year, months, reportId).Data

        last_month = months[-1]

        # Current Liabilities
        changeInAP = get_change(financialData, "CURRENT LIABILITIES", "Classification", "Accounts Payable", year, year - 1, last_month)
        changeinOCL = get_change(financialData, "CURRENT LIABILITIES", "Classification", "Other Current Liabilities", year, year - 1, last_month)

        # Current Assets
        changeinAR = get_change(financialData, "CURRENT ASSETS", "Classification", "Accounts Receivable", year - 1, year, last_month)
        changeinINV = get_change(financialData, "CURRENT ASSETS", "Classification", "Inventory", year - 1, year, last_month)
        changeinWIP = get_change(financialData, "CURRENT ASSETS", "Classification", "Work In Progress", year - 1, year, last_month)
        changeinOCA = get_change(financialData, "CURRENT ASSETS", "Classification", "Other Current Assets", year - 1, year, last_month)

        operatingProfit = getOperatingActivitiesCashFlow(year,months,reportId).Data

        # You can now return or use the computed values as needed
        data =  {
            "totalRevenue": totalRev,
            "totalOperatingExpenses": totalOE,
            "directExpenses": totalDE,
            "otherIncome": otherInc,
            "changeInAccountsPayable": changeInAP,
            "changeInOtherCurrentLiabilities": changeinOCL,
            "changeInAccountsReceivable": changeinAR,
            "changeInInventory": changeinINV,
            "changeInWorkInProgress": changeinWIP,
            "changeInOtherCurrentAssets": changeinOCA,
            "operatingProfit":operatingProfit
        }

        return Result(
            Data=data,
            Status=1,
            Message="Cash Flow Statement calculated successfully",
        )

    except Exception as e:
        print(f"Error in getEACharts: {e}")
        return None
