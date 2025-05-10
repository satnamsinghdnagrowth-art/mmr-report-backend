from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from services.reportSection.breakEvenAnalysis.cards.BreakAnalysisCards import getBACards
from core.models.visualsModel.SectionData import SectionData
from services.reportSection.financialHighlights.cards.cardsKPIs import getSectionCards
from services.reportSection.cashFlowAnalysis.charts.CashFlowCharts import getCashFlowCharts
from services.reportSection.detailedSheet.table import getTable


# Get the sections cards
def getSectionData(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:
        if reportType == "Year":
            months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        cardsData = getSectionCards(year, months, reportType, section, reportId).Data
        chartsData = []
        tablesData = [getTable(2024,"PROFIT & LOSS").Data,getTable(2024,"BalanceSheet").Data]
        sectionData = SectionData(Charts=chartsData, Cards=cardsData, Tables=tablesData)

        return Result(
            Data=sectionData, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getSectionData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
