from datetime import datetime
from core.models.base.ResultModel import Result
from services.reportSection.consolidateSection.AllSectionDataServices import AllSectionDataService
from core.models.visualsModel.SectionData import ConsolidateSectionDate
from core.models.base.SectionNamesEnum import SectionName

# Get the sections cards
def getConsolidateSectionData(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:

        months = (
            [i for i in range(1, months[-1] + 1)]
            if reportType.lower() == "year"
            else months
        )

        serviceObj = AllSectionDataService(
            reportId=reportId, year=year, months=months, reportType=reportType
        )

        FH_dataResponse = ConsolidateSectionDate(SectionName=SectionName.FinancialHighlights.value,
            SectionData=serviceObj.getFinancialHighlightsSection().Data)
        
        EXP_dataResponse = ConsolidateSectionDate(SectionName=SectionName.ExpensesAnalysis.value,
            SectionData=serviceObj.getExpensesAnalysisSection().Data)
        
        PA_dataResponse =ConsolidateSectionDate(SectionName=SectionName.Profitability.value,
            SectionData=serviceObj.getProfitablitySection().Data)
        
        BE_dataResponse = ConsolidateSectionDate(SectionName=SectionName.BreakevenAnlaysis.value,
            SectionData=serviceObj.getBreakEvenAnalysisSection().Data)
        
        CF_dataResponse = ConsolidateSectionDate(SectionName=SectionName.CashFlowAnalysis.value,
            SectionData=serviceObj.getCashFlowSection().Data)
        
        CombinedData = {
            "Sections": [
                FH_dataResponse,
                EXP_dataResponse,
                PA_dataResponse,
                BE_dataResponse,
                CF_dataResponse
            ]
        }

        return Result(
            Data=CombinedData, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getSectionData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
