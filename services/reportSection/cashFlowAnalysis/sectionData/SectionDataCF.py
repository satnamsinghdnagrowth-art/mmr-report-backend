from datetime import datetime
from core.models.base.ResultModel import Result
from services.visuals.card.GetSectionsCards import getSectionCards
from services.visuals.charts.GetSectionCharts import getSectionCharts
from services.reportSection.cashFlowAnalysis.charts.cashFlowChart import getEACharts
from core.models.visualsModel.SectionData import SectionData
from typing import Optional
from services.reportSection.detailedSheet.table import getDetailedTable
from services.reportSection.detailedSheet.cashFlowTable import getCashFlowTable
from core.models.visualsModel.CardModel import CardsListModel
from core.models.visualsModel.ChartModel import ChartsListModel
from core.models.visualsModel.TableModel import TableListModel
from typing import Optional, List


class CashFlowAnalysisDataService:
    """
    Service class to handle Financial Highlights data section-wise: Cards, Charts, and Tables.
    """

    def __init__(
        self,
        year: int,
        reportType: str,
        section: str,
        reportId: Optional[int] = None,
        months: Optional[List[int]] = None,
    ):
        """
        Initialize with basic parameters. If months are not provided,
        it defaults to all months in a year or October (for single-month reports).
        """
        self.year = year
        self.reportType = reportType
        self.section = section
        self.reportId = reportId
        self.months = (
            [i for i in range(1, months[-1] + 1)]
            if reportType.lower() == "year"
            else months
        )

    # Complete Section
    def get(self) -> Result:
        """
        Retrieves all section data: Cards, Charts, and Tables.
        Returns a Result object containing a SectionData model.
        """
        try:
            # Cards
            cards_result = getSectionCards(
                self.year, self.months, self.reportType, self.section, self.reportId
            )
            cards_data = cards_result.Data or []

            # Charts from JSON config (e.g. CASH_POSITION_CHART)
            config_charts_result = getSectionCharts(
                self.year, self.months, self.reportType, self.section, self.reportId
            )
            config_charts = config_charts_result.Data or []

            # Waterfall cash-flow chart (CASH_FLOW_CHART) — built separately
            cf_chart_result = getEACharts(self.year, self.months, self.reportId)
            cf_charts = cf_chart_result.Data or [] if cf_chart_result else []

            charts_data = config_charts + cf_charts

            # Tables — filter out None entries in case any sub-call failed
            # Note: Balance Sheet table moved to the dedicated Balance Sheet section
            raw_tables = [
                getDetailedTable(
                    self.year, self.months, ["PROFIT & LOSS"], self.reportId
                ).Data,
                getCashFlowTable(self.year, self.months, self.reportId).Data,
            ]
            tables_data = [t for t in raw_tables if t is not None]

            # Combine into SectionData
            section_data = SectionData(
                Charts=charts_data, Cards=cards_data, Tables=tables_data
            )

            return Result(
                Data=section_data,
                Status=1,
                Message="Section data retrieved successfully",
            )

        except Exception as ex:
            # Catch-all for unexpected issues
            message = f"Exception in get(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Cards
    def getCardsOnly(self) -> Result:
        """
        Retrieves only the Cards data for the section.
        """
        try:
            cards = getSectionCards(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data

            response = CardsListModel(Cards=cards)

            return Result(
                Data=response, Status=1, Message="Cards retrieved successfully"
            )

        except Exception as ex:
            message = f"Exception in getCardsOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Charts
    def getChartsOnly(self) -> Result:
        """
        Retrieves only the Charts data for the section.
        """
        try:
            config_charts = getSectionCharts(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data or []

            cf_chart_result = getEACharts(self.year, self.months, self.reportId)
            cf_charts = cf_chart_result.Data or [] if cf_chart_result else []

            all_charts = config_charts + cf_charts
            response = ChartsListModel(Charts=all_charts)
            return Result(
                Data=response, Status=1, Message="Charts retrieved successfully"
            )

        except Exception as ex:
            message = f"Exception in getChartsOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Tables
    def getTablesOnly(self) -> Result:
        """
        Retrieves only the Tables data for the section.
        Note: Balance Sheet table is in the dedicated Balance Sheet section.
        """
        try:
            tables = [
                getDetailedTable(
                    self.year, self.months, ["PROFIT & LOSS"], self.reportId
                ).Data,
                getCashFlowTable(self.year, self.months, self.reportId).Data,
            ]
            tables = TableListModel(Tables=tables)
            return Result(
                Data=tables, Status=1, Message="Tables retrieved successfully"
            )

        except Exception as ex:
            message = f"Exception in getTablesOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)
