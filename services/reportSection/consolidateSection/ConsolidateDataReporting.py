from datetime import datetime
from core.models.base.ResultModel import Result
from services.reportSection.consolidateSection.AllSectionDataServices import (
    AllSectionDataService,
)
from helper.SaveConsolidateDataResponse import consolidateDataResponse
from core.models.visualsModel.SectionData import ConsolidateSectionDate,SectionDataModel
from core.models.base.SectionNamesEnum import SectionName
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from helper.SaveConsolidateDataResponse import saveResponse
from core.models.visualsModel.CustomKpiModel import CustomKpiCreationModel
from services.customKPIs.CustomKPIsCreation import customKPICreation
from concurrent.futures import ThreadPoolExecutor, as_completed
from helper.SaveCustomKpisList import getCustomKpisList

# Get the sections cards
def getConsolidateSectionData(
    year: int,
    months: list[int],
    reportType: str,
    section: str,
    reportId: int,
    companyId: int,
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

        sectionMethods = {
            SectionName.FinancialHighlights.value: serviceObj.getFinancialHighlightsSection,
            SectionName.ExpensesAnalysis.value: serviceObj.getExpensesAnalysisSection,
            SectionName.Profitability.value: serviceObj.getProfitablitySection,
            SectionName.BreakevenAnlaysis.value: serviceObj.getBreakEvenAnalysisSection,
            SectionName.CashFlowAnalysis.value: serviceObj.getCashFlowSection,
        }

        # Submit all tasks
        future_to_name = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            for name, func in sectionMethods.items():
                future = executor.submit(func)
                future_to_name[future] = name

        # Collect results in a dict first
        temp_results = {}
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                data = future.result()
                temp_results[name] = ConsolidateSectionDate(SectionName=name, SectionData=data.Data)
            except Exception as e:
                print(f"Error in section {name}: {e}")

        #  Preserve order as in sectionMethods keys
        results = [temp_results[name] for name in sectionMethods.keys()]

        CombinedData = SectionDataModel(Sections=results)

        saveResponse(reportId, CombinedData)

        CustomKpisList = getCustomKpisList(reportId)

        if CustomKpisList is not None:

            data = consolidateDataResponse.get(reportId)
            formattedData = data.model_dump()
            sectionData = formattedData["Sections"]

            # Inject custom KPIs if any
            if reportId in CustomKpisList:
                for customKpi in CustomKpisList[reportId]:
                    for sec in sectionData:
                        if sec["SectionName"] == customKpi.SectionName:
                            visualType = (
                                "Charts" if customKpi.VisualType == "Chart" else "Tables"
                            )
                            requestModel = CustomKpiCreationModel(
                                Year=year,
                                Months=months,
                                VisualType=customKpi.VisualType,
                                Items=customKpi.Items,
                            )
                            kpiResponse = customKPICreation(requestModel, reportId).Data
                            sec["SectionData"][visualType].append(kpiResponse)
        else:
            formattedData = CombinedData
            print(f"No custom KPIs defined for report {reportId}")

        return Result(
            Data=formattedData, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getSectionData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
