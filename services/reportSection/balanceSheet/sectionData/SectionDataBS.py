from datetime import datetime
from core.models.base.ResultModel import Result
from services.visuals.card.GetSectionsCards import getSectionCards
from services.visuals.charts.GetSectionCharts import getSectionCharts
from core.models.visualsModel.SectionData import SectionData
from services.reportSection.detailedSheet.table import getDetailedTable
from core.models.visualsModel.CardModel import CardsListModel
from core.models.visualsModel.ChartModel import ChartsListModel
from core.models.visualsModel.TableModel import TableListModel
from typing import Optional, List


class BalanceSheetDataService:
    """
    Service class for the Balance Sheet section: Cards, Charts, and Tables.
    Primary visual is the combined Balance Sheet + Equity table (BALANCE_SHEET_TABLE).
    """

    def __init__(
        self,
        year: int,
        reportType: str,
        section: str,
        reportId: Optional[int] = None,
        months: Optional[List[int]] = None,
    ):
        self.year = year
        self.reportType = reportType
        self.section = section
        self.reportId = reportId
        self.months = (
            [i for i in range(1, months[-1] + 1)]
            if reportType.lower() == "year"
            else months
        )

    def get(self) -> Result:
        try:
            cards_data = getSectionCards(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data or []

            charts_data = getSectionCharts(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data or []

            bs_table = getDetailedTable(
                self.year, self.months, ["BalanceSheet", "EQUITY"], self.reportId
            ).Data
            tables_data = [t for t in [bs_table] if t is not None]

            section_data = SectionData(
                Charts=charts_data, Cards=cards_data, Tables=tables_data
            )
            return Result(
                Data=section_data,
                Status=1,
                Message="Section data retrieved successfully",
            )
        except Exception as ex:
            message = f"Exception in BalanceSheetDataService.get(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    def getCardsOnly(self) -> Result:
        try:
            cards = getSectionCards(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data
            return Result(
                Data=CardsListModel(Cards=cards), Status=1, Message="Cards retrieved successfully"
            )
        except Exception as ex:
            message = f"Exception in getCardsOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    def getChartsOnly(self) -> Result:
        try:
            charts = getSectionCharts(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data or []
            return Result(
                Data=ChartsListModel(Charts=charts), Status=1, Message="Charts retrieved successfully"
            )
        except Exception as ex:
            message = f"Exception in getChartsOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    def getTablesOnly(self) -> Result:
        try:
            bs_table = getDetailedTable(
                self.year, self.months, ["BalanceSheet", "EQUITY"], self.reportId
            ).Data
            tables = TableListModel(Tables=[t for t in [bs_table] if t is not None])
            return Result(
                Data=tables, Status=1, Message="Tables retrieved successfully"
            )
        except Exception as ex:
            message = f"Exception in getTablesOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)
