from datetime import datetime
from core.models.base.ResultModel import Result
from services.reportSection.consolidateSection.AllSectionDataServices import (
    AllSectionDataService,
)
from helper.SaveConsolidateDataResponse import consolidateDataResponse
from core.models.visualsModel.SectionData import (
    ConsolidateSectionDate,
    SectionDataModel,
)
from core.models.base.SectionNamesEnum import SectionName, get_section_id
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
                section_id = get_section_id(name)
                temp_results[name] = ConsolidateSectionDate(
                    SectionId=section_id,
                    SectionName=name,
                    SectionData=data.Data
                )
            except Exception as e:
                print(f"Error in section {name}: {e}")

        #  Preserve order as in sectionMethods keys
        results = [temp_results[name] for name in sectionMethods.keys()]

        CombinedData = SectionDataModel(Sections=results)

        saveResponse(reportId, CombinedData)

        CustomKpisList = getCustomKpisList(reportId)
        
        # Get the original data
        data = consolidateDataResponse.get(reportId)
        actualData = data.model_dump()
        
        # Initialize custom data structure
        customData = {"Sections": []}
        
        if CustomKpisList is not None and reportId in CustomKpisList:
            # Create a mapping for quick lookup
            sectionDataMap = {sec["SectionName"]: sec for sec in actualData["Sections"]}
            
            for customKpi in CustomKpisList[reportId]:
                # Find or create section in customData
                customSection = next(
                    (s for s in customData["Sections"] if s["SectionName"] == customKpi.SectionName),
                    None
                )
                
                if customSection is None:
                    section_id = get_section_id(customKpi.SectionName)
                    customSection = {
                        "SectionId": section_id,
                        "SectionName": customKpi.SectionName,
                        "SectionData": {"Cards": [], "Charts": [], "Tables": []},
                        "Visbility": True
                    }
                    customData["Sections"].append(customSection)
                
                # Ensure all visual containers exist
                customSection["SectionData"].setdefault("Cards", [])
                customSection["SectionData"].setdefault("Charts", [])
                customSection["SectionData"].setdefault("Tables", [])

                # Map VisualType to SectionData key
                if customKpi.VisualType == "Chart":
                    visualType = "Charts"
                elif customKpi.VisualType == "Table":
                    visualType = "Tables"
                elif customKpi.VisualType == "Card":
                    visualType = "Cards"
                else:
                    continue  # Unsupported visual type

                requestModel = CustomKpiCreationModel(
                    Year=year,
                    Months=months,
                    VisualType=customKpi.VisualType,
                    Items=customKpi.Items,
                )

                kpiResponse = customKPICreation(requestModel, reportId).Data
                customSection["SectionData"][visualType].append(kpiResponse)
        else:
            print(f"No custom KPIs defined for report {reportId}")

        # Prepare the separated response
        separatedData = {
            "ActualData": actualData,
            "CustomData": customData
        }

        return Result(
            Data=separatedData, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getSectionData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
