from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from services.reportSection.expensesAnalysis.charts.ExpensesAnalysisCharts import (
    getEACharts,
)
from core.models.visualsModel.SectionData import SectionData
from typing import Optional
from services.reportSection.expensesAnalysis.tables.TopOperatingExpenses import (
    getTopOpeatingExpenses,
)


# Get the sections cards
def getSectionData(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:
        months = [i for i in range(1, months[0]+1)] if reportType.lower() == "year" else months
        cardsData = []
        chartsData = getEACharts(year, months, reportType, section, reportId).Data
        tablesData = getTopOpeatingExpenses(
            year, months, reportType, section, reportId
        ).Data
        sectionData = SectionData(Charts=chartsData, Cards=cardsData, Tables=tablesData)

        return Result(
            Data=sectionData, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
