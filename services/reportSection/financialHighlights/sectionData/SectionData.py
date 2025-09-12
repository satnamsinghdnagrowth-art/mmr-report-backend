from datetime import datetime
from core.models.base.ResultModel import Result
from services.visuals.card.GetSectionsCards import getSectionCards
from services.visuals.charts.GetSectionCharts import getSectionCharts
from core.models.visualsModel.SectionData import SectionData
from typing import Optional
from services.reportSection.financialHighlights.tables.IncomeStatementTablesKPI import (
    getISTable,
)
from services.reportSection.financialHighlights.charts.RevenueBreakdown import (
    getRevenueBreakdownChart,
)
from core.models.visualsModel.CardModel import CardsListModel
from core.models.visualsModel.ChartModel import ChartsListModel
from core.models.visualsModel.TableModel import TableListModel
from datetime import datetime
from typing import Optional, List


class FinancialHighlightSectionDataService:
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

    # Complete  Section
    def get(self) -> Result:
        """
        Retrieves all section data: Cards, Charts, and Tables.
        Returns a Result object containing a SectionData model.
        """
        try:
            # Retrieve individual data types
            cards_data = getSectionCards(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data

            charts_data = getSectionCharts(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data


            # charts_data.append(getRevenueBreakdownChart(self.year, self.months, self.reportId).Data)


            tables_data = getISTable(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data

            # tables_data.append(getRevenueBreakdownTable( self.year, self.months, self.reportType,  self.reportId).Data)

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
            print(self.months,self.year,"------------------")
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
            charts = getSectionCharts(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data


            charts.append(getRevenueBreakdownChart(self.year, self.months, self.reportId).Data)

            response = ChartsListModel(Charts=charts)
            return Result(
                Data=charts, Status=1, Message="Charts retrieved successfully"
            )

        except Exception as ex:
            message = f"Exception in getChartsOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Tables
    def getTablesOnly(self) -> Result:
        """
        Retrieves only the Tables data for the section.
        """
        try:
            tables = getISTable(
                self.year, self.months, self.reportType, self.section, self.reportId
            ).Data
            tables = TableListModel(Tables=tables)
            return Result(
                Data=tables, Status=1, Message="Tables retrieved successfully"
            )

        except Exception as ex:
            message = f"Exception in getTablesOnly(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)
