from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from core.models.visualsModel.SectionData import SectionData
from services.reportSection.detailedSheet.BS_Table import getBalanaceSheetTable
from services.reportSection.detailedSheet.PNL_Table import getProfitLossTable
from services.reportSection.detailedSheet.cashFlowTable import getCashFlowTable
import time
from services.visuals.card.GetSectionsCards import getSectionCards
from services.visuals.charts.GetSectionCharts import getSectionCharts


# Get the sections cards
def getSectionData(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:
        months = (
            [i for i in range(1, months[0] + 1)]
            if reportType.lower() == "year"
            else months
        )

        cardsData = getSectionCards(year, months, reportType, section, reportId).Data
        chartsData = getSectionCharts(year, months, reportType, section, reportId).Data
        # cards = []
        # charts = []

        tablesData = [
            getProfitLossTable(year, months, ["PROFIT & LOSS"], reportId).Data,
            getBalanaceSheetTable(
                year, months, ["BalanceSheet", "EQUITY"], reportId
            ).Data,
            getCashFlowTable(year, months, reportId).Data,
        ]

        sectionData = SectionData(Charts=chartsData, Cards=cardsData, Tables=tablesData)

        return Result(
            Data=sectionData, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getSectionData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
