from datetime import datetime
from core.models.base.ResultModel import Result
from core.models.visualsModel.SectionData import SectionData
from typing import Optional, List
from services.reportSection.financialHighlights.sectionData.SectionData import (
    FinancialHighlightSectionDataService,
)
from services.reportSection.profitAbility.sectionData.SectionDataPA import (
    ProfitAbilityDataService,
)
from services.reportSection.expensesAnalysis.sectionData.SectionDataEA import (
    ExpensesAnalysisDataService,
)
from services.reportSection.cashFlowAnalysis.sectionData.SectionDataCF import (
    CashFlowAnalysisDataService,
)
from services.reportSection.breakEvenAnalysis.sectionData.SectionDataBE import (
    BreakEvenDataService,
)


class AllSectionDataService:
    """
    Service class to handle Financial Highlights data section-wise: Cards, Charts, and Tables.
    """

    def __init__(
        self,
        year: int,
        reportType: str,
        reportId: Optional[int] = None,
        months: Optional[List[int]] = None,
    ):
        """
        Initialize with basic parameters. If months are not provided,
        it defaults to all months in a year or October (for single-month reports).
        """
        self.year = year
        self.reportType = reportType
        self.reportId = reportId
        self.months = (
            [i for i in range(1, months[-1] + 1)]
            if reportType.lower() == "year"
            else months
        )

    # Financial Highlights  Section
    def getFinancialHighlightsSection(self) -> Result:
        """
        Retrieves all section data: Cards, Charts, and Tables.
        Returns a Result object containing a SectionData model.
        """
        try:
            sectionName = "Financial Heights"
            FH_Obj = FinancialHighlightSectionDataService(
                self.year, self.reportType, sectionName, self.reportId, self.months
            )

            data = FH_Obj.get().Data

            return Result(
                Data=data,
                Status=1,
                Message="Section data retrieved successfully",
            )
        except Exception as ex:
            # Catch-all for unexpected issues
            message = f"Exception in getFinancialHighlightsSection: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Get Expenses Analysis Section
    def getExpensesAnalysisSection(self) -> Result:
        """
        Retrieves all section data: Cards, Charts, and Tables.
        Returns a Result object containing a SectionData model.
        """
        try:
            sectionName = "Expenses Analysis"

            # Retrieve individual data types
            EXP_Obj = ExpensesAnalysisDataService(
                self.year, self.reportType, sectionName, self.reportId, self.months
            )

            data = EXP_Obj.get().Data

            return Result(
                Data=data,
                Status=1,
                Message="Section data retrieved successfully",
            )
        except Exception as ex:
            # Catch-all for unexpected issues
            message = f"Exception in get(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Get CashFlow Analysis Section
    def getCashFlowSection(self) -> Result:
        """
        Retrieves all section data: Cards, Charts, and Tables.
        Returns a Result object containing a SectionData model.
        """
        try:
            # Retrieve individual data types
            sectionName = "Cash Flow Analysis"

            CF_Obj = CashFlowAnalysisDataService(
                self.year, self.reportType, sectionName, self.reportId, self.months
            )

            data = CF_Obj.get().Data

            return Result(
                Data=data,
                Status=1,
                Message="Section data retrieved successfully",
            )
        except Exception as ex:
            # Catch-all for unexpected issues
            message = f"Exception in get(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Get Profitability Section
    def getProfitablitySection(self) -> Result:
        """
        Retrieves all section data: Cards, Charts, and Tables.
        Returns a Result object containing a SectionData model.
        """
        try:
            sectionName = "ProfitAbility"
            # Retrieve individual data types
            PA_Obj = ProfitAbilityDataService(
                self.year, self.reportType, sectionName, self.reportId, self.months
            )

            data = PA_Obj.get().Data

            return Result(
                Data=data,
                Status=1,
                Message="Section data retrieved successfully",
            )
        except Exception as ex:
            # Catch-all for unexpected issues
            message = f"Exception in get(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)

    # Get Break-Even Analysis Section
    def getBreakEvenAnalysisSection(self) -> Result:
        """
        Retrieves all section data: Cards, Charts, and Tables.
        Returns a Result object containing a SectionData model.
        """
        try:
            sectionName = "Breakeven-Analysis"

            BE_Obj = BreakEvenDataService(
                self.year, self.reportType, sectionName, self.reportId, self.months
            )

            data = BE_Obj.get().Data

            return Result(
                Data=data, Status=1, Message="Section Data retrieved Successfully"
            )
        except Exception as ex:
            # Catch-all for unexpected issues
            message = f"Exception in get(): {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Data=None, Status=0, Message=message)
