from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from helper.LoadJsonData import financialDataTest
from services.calculations.NetIncome import netIncome
from helper.GetValueSum import getValueSum
from services.calculations.CashFlowActivities import getOperatingActivitiesCashFlow
from helper.GetFileByReportId import getReportData
from core.models.visualsModel.ChartModel import ChartDataModel, YAxisSeriesModel
from services.calculations.CashFlowActivities import getOperatingActivitiesCashFlow
from services.calculations.CurrentAssestAndLiabilities import getTotalCurrentLiabilities


# Get the sections cards
def getEACharts(year: int, months: list[int], reportId):
    try:
        financialData = getReportData(reportId) if reportId else financialDataTest

        netProfitTotal = netIncome(year, months, reportId).Data

        totalInterestIncome = getValueSum(
            financialData,
            ["PROFIT & LOSS", "OTHER INCOME", "Classification", "Interest Income"],
            year,
            months,
        ).Data

        totalDepreciation = getValueSum(
            financialData,
            ["PROFIT & LOSS", "EXPENSES", "Classification", "Depreciation"],
            year,
            months,
        ).Data

        totalInterestExpense = getValueSum(
            financialData,
            ["PROFIT & LOSS", "OTHER EXPENSES", "Classification", "Interest Expense"],
            year,
            months,
        ).Data

        netIncomeAfterAdjustment = (
            netProfitTotal
            + totalDepreciation
            + totalInterestExpense
            - totalInterestIncome
        )

        changeInAR = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "Classification",
                    "Accounts Receivable",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "Classification",
                    "Accounts Receivable",
                ],
                year,
                [months[-1]],
            ).Data
        )

        changeInPreExp = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "LineItems",
                    "Other Current Assets",
                    "Prepaid Expenses 0",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT ASSETS",
                    "LineItems",
                    "Other Current Assets",
                    "Prepaid Expenses 0",
                ],
                year,
                [months[-1]],
            ).Data
        )

        changeInCA = changeInAR + changeInPreExp

        # Current Liabilities
        changeInOCL = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Other Current Liabilities",
                ],
                year,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Other Current Liabilities",
                ],
                year - 1,
                [months[-1]],
            ).Data
        )

        changeInAP = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Accounts Payable",
                ],
                year,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Accounts Payable",
                ],
                year - 1,
                [months[-1]],
            ).Data
        )

        changeInCL = (
            getTotalCurrentLiabilities(year, [months[-1]]).Data
            - getTotalCurrentLiabilities(year - 1, [months[-1]]).Data
        )

        operatingCashFlow = getOperatingActivitiesCashFlow(year, months, reportId).Data

        changeInFA = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Fixed Assets",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Fixed Assets",
                ],
                year,
                [months[-1]],
            ).Data
        )

        changeInIA = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Intangible Assets",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Intangible Assets",
                ],
                year,
                [months[-1]],
            ).Data
        )

        changeInONCA = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Other Non-Current Assets",
                ],
                year - 1,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "NON-CURRENT ASSETS",
                    "Classification",
                    "Other Non-Current Assets",
                ],
                year,
                [months[-1]],
            ).Data
        )

        investigatingActivitiesCashFlow = (
            changeInFA + changeInIA + changeInONCA + totalInterestIncome
        )

        freeCashFlow = operatingCashFlow + investigatingActivitiesCashFlow

        # Current Assets
        changeinOE = (
            getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Other Equity",
                ],
                year,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Other Equity",
                ],
                year - 1,
                [months[-1]],
            ).Data
        )

        changeinSTD = (
            getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Short-term Debt",
                ],
                year,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "BalanceSheet",
                    "CURRENT LIABILITIES",
                    "Classification",
                    "Short-term Debt",
                ],
                year - 1,
                [months[-1]],
            ).Data
        )

        # Current Assets
        changeinRE = (
            getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Retained Earnings",
                ],
                year,
                [months[-1]],
            ).Data
            - getValueSum(
                financialData,
                [
                    "EQUITY",
                    "EQUITY",
                    "Classification",
                    "Retained Earnings",
                ],
                year - 1,
                [months[-1]],
            ).Data
        )

        totalCE = getValueSum(
            financialData,
            [
                "EQUITY",
                "EQUITY",
                "Classification",
                "Current Earnings",
            ],
            year - 1,
            [months[-1]],
        ).Data

        totalChangeinRE = changeinRE - totalCE

        print(changeinOE, changeinSTD, changeinRE)

        financingActivitiesCashFlow = changeinOE + changeinSTD + totalChangeinRE

        netCashFlow = freeCashFlow + financingActivitiesCashFlow

        openingCashBalance = getValueSum(
            financialData,
            ["BalanceSheet", "CURRENT ASSETS", "Classification", "Cash"],
            year - 1,
            [months[-1]],
        ).Data

        closingCashBalance = getValueSum(
            financialData,
            ["BalanceSheet", "CURRENT ASSETS", "Classification", "Cash"],
            year,
            [months[-1]],
        ).Data

        xAxisValue = [
            "Net income",
            "Add: Depreciation (DA)",
            "Add: Interest expenses (IEXP)",
            "Less: Interest income (IINC)",
            "Net income after adjustments",
            "Change in AR",
            "Change in Prepaid Expenses",
            "Change in Current Assets (excluding Cash & Equivalent)",
            "Change in Accounts Payable",
            "Change in Other Current Liabilities",
            "Change in Current Liabilities",
            "Cash Flow from Operating Activities",
            "Change in Fixed Assets",
            "Change in Intangible Assets",
            "Change in Investments or Other Non-Current Assets",
            "Interest income",
            "Cash Flow from Investing Activities",
            "Free Cash Flow",
            # "change in Other Equity",
            # "Change in Retained Earnings ",
            # "Change in short term debt",
            # "Cash Flow from Financing Activities",
            # "Net Cash Flow",
            # "Opening Cash Balance",
            # "Closing Cash Balance",
        ]

        yAxisValue = [
            netProfitTotal,
            totalDepreciation,
            totalInterestExpense,
            totalInterestIncome,
            netIncomeAfterAdjustment,
            changeInAR,
            changeInPreExp,
            changeInCA,
            changeInAP,
            changeInOCL,
            changeInCL,
            operatingCashFlow,
            changeInCL,
            operatingCashFlow,
            changeInFA,
            changeInIA,
            changeInONCA,
            investigatingActivitiesCashFlow,
            freeCashFlow,
            # changeinOE,
            # totalChangeinRE,
            # changeinSTD,
            # financingActivitiesCashFlow,
            # netCashFlow,
            # openingCashBalance,
            # closingCashBalance,
        ]

        data = ChartDataModel(
            Title="Cash Flow Statements",
            Xaxis=xAxisValue,
            YaxisSeries=[
                YAxisSeriesModel(
                    Title="Revenue Flow",
                    Type="Bar",
                    Symbol="$",
                    AreaFill=False,
                    Values=yAxisValue,  # Values, 0 if total is auto
                )
            ],
            IndexAxis="y",
            RightYaxis=False,
        )

        return Result(
            Data=[data],
            Status=1,
            Message="Cash Flow Statement calculated successfully",
        )

    except Exception as e:
        print(f"Error in getEACharts: {e}")
        return None
