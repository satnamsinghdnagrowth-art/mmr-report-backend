from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from services.reportSection.breakEvenAnalysis.cards.BreakAnalysisCards import getBACards
from core.models.visualsModel.SectionData import SectionData
from services.reportSection.financialHighlights.cards.cardsKPIs import getSectionCards
from services.reportSection.breakEvenAnalysis.charts.BACharts import getBACharts
from services.reportSection.detailedSheet.table import getDetailedTable
from services.reportSection.detailedSheet.cashFlowTable import getCashFlowTable
import time
from services.reportSection.cashFlowAnalysis.charts.cashFlowChart import getEACharts


# Get the sections cards
def getSectionData(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:
        months = [i for i in range(1, months[0]+1)] if reportType.lower() == "year" else months

        cardsData = getSectionCards(year, months, reportType, section, reportId).Data
        chartsData = getEACharts(year, months, reportId).Data
        tablesData = [
            getDetailedTable(year, "PROFIT & LOSS").Data,
            getDetailedTable(year, "BalanceSheet").Data,
            getDetailedTable(year, "EQUITY").Data,
            getCashFlowTable(year).Data,
        ]
        sectionData = SectionData(Charts=chartsData, Cards=cardsData, Tables=tablesData)

        return Result(
            Data=sectionData, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getSectionData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
