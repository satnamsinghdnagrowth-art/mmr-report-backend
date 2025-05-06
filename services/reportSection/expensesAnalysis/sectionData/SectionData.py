from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from services.reportSection.expensesAnalysis.charts.ExpensesAnalysisCharts import getEACharts
from core.models.visualsModel.SectionData import SectionData
from services.reportSection.financialHeights.tables.IncomeStatementTablesKPI import (
    getISTable,
)

from services.reportSection.expensesAnalysis.tables.TopOperatingExpenses import getTopOpeatingExpenses


# Get the sections cards
def getSectionData(year: int, months: list[int], reportType: str, section: str):
    try:
        cardsData = []
        chartsData = getEACharts(year, months, reportType, section).Data
        tablesData = getTopOpeatingExpenses(year, months, reportType, section).Data
        sectionData = SectionData(Charts=chartsData, Cards=cardsData, Tables=tablesData)

        return Result(
            Data=sectionData, Status=1, Message="Section Data retrieved Successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
