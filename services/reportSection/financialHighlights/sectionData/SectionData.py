from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from services.reportSection.financialHighlights.cards.cardsKPIs import getSectionCards
from services.reportSection.financialHighlights.charts.chartsKPIs import (
    getSectionCharts,
)
from core.models.visualsModel.SectionData import SectionData
from typing import Optional
from services.reportSection.financialHighlights.tables.IncomeStatementTablesKPI import (
    getISTable,
)


# Get the sections cards
def getSectionData(
    year: int,
    months: list[int],
    reportType: str,
    section: str,
    reportId: Optional[int] = None,
):
    try:
        if reportType == "Year":
            months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        cardsData = getSectionCards(year, months, reportType, section, reportId).Data
        chartsData = getSectionCharts(year, months, reportType, section, reportId).Data
        tablesData = getISTable(year, months, reportType, section, reportId).Data
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
