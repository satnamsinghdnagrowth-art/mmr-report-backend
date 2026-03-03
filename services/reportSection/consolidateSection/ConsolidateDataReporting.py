from datetime import datetime
from core.models.base.ResultModel import Result
from services.reportSection.consolidateSection.AllSectionDataServices import (
    AllSectionDataService,
)
from core.models.visualsModel.SectionData import (
    ConsolidateSectionDate,
    FlatSectionData,
    SectionDataModel,
    SectionMeta,
    CombinedSectionResponse,
)
from core.models.base.SectionNamesEnum import SectionName, get_section_id
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

        # Preserve order as in sectionMethods keys
        results = [temp_results[name] for name in sectionMethods.keys() if name in temp_results]

        CombinedData = SectionDataModel(Sections=results)

        saveResponse(reportId, CombinedData)

        # Flatten actual section data into combined lists,
        # stamping SectionID, PageNo, and Order onto each visual
        all_cards = []
        all_charts = []
        all_tables = []

        # Build a lookup: section_id -> page_no (based on ordered results)
        section_page_map = {
            section.SectionId: page_no
            for page_no, section in enumerate(results, start=1)
        }

        # ── Discover custom KPI sections that fall outside the 5 known sections ──
        # Load custom KPIs early so we can discover their SectionIds and assign
        # page numbers (6, 7, …) before stamping visuals.
        CustomKpisListRaw = getCustomKpisList(reportId)
        _registry = None
        try:
            from core.registry.SectionRegistry import get_section_registry
            _registry = get_section_registry()
        except Exception:
            pass

        next_page_no = len(results) + 1  # first custom page number (e.g. 6)
        custom_section_meta = []          # extra SectionMeta entries

        if CustomKpisListRaw is not None and reportId in CustomKpisListRaw:
            seen_custom_sections = {}  # section_id -> page_no (ordered by first occurrence)
            for customKpi in CustomKpisListRaw[reportId]:
                sid = customKpi.SectionId
                if sid and sid not in section_page_map and sid not in seen_custom_sections:
                    seen_custom_sections[sid] = next_page_no
                    # Resolve human-readable name from registry
                    section_name = "Custom Page"
                    if _registry:
                        resolved = _registry.get_section_name(sid)
                        if resolved:
                            section_name = resolved
                    custom_section_meta.append(
                        SectionMeta(
                            SectionId=sid,
                            SectionName=section_name,
                            PageNo=next_page_no,
                            Visibility=True,
                        )
                    )
                    next_page_no += 1

            # Merge into the main lookup so stamping works for all custom KPIs
            section_page_map.update(seen_custom_sections)

        for page_no, section in enumerate(results, start=1):
            section_id = section.SectionId
            if not section.SectionData:
                continue

            for order, card in enumerate(section.SectionData.Cards or [], start=1):
                card.SectionID = section_id
                card.PageNo = page_no
                card.Order = order
                all_cards.append(card)

            for order, chart in enumerate(section.SectionData.Charts or [], start=1):
                chart.SectionID = section_id
                chart.PageNo = page_no
                chart.Order = order
                all_charts.append(chart)

            for order, table in enumerate(section.SectionData.Tables or [], start=1):
                table.SectionID = section_id
                table.PageNo = page_no
                table.Order = order
                all_tables.append(table)

        # Append custom KPI visuals, stamping SectionID / PageNo / Order
        # using the SectionId stored at creation time.
        # NOTE: CustomKpisListRaw was already loaded above during orphan-section discovery.

        # Per-type order counters beyond the actuals visuals already appended
        custom_order_counters = {"Card": {}, "Chart": {}, "Table": {}}

        if CustomKpisListRaw is not None and reportId in CustomKpisListRaw:
            for customKpi in CustomKpisListRaw[reportId]:
                requestModel = CustomKpiCreationModel(
                    Year=year,
                    Months=months,
                    VisualType=customKpi.VisualType,
                    Items=customKpi.Items,
                    VisualId=customKpi.VisualId,
                )
                kpiResponse = customKPICreation(requestModel, reportId).Data
                if kpiResponse is None:
                    continue

                # Handle list of items or single item
                items_to_process = kpiResponse if isinstance(kpiResponse, list) else [kpiResponse]

                for item in items_to_process:
                    # Resolve which page this custom KPI belongs to (now includes custom pages)
                    kpi_section_id = customKpi.SectionId
                    kpi_page_no = section_page_map.get(kpi_section_id)  # None only if SectionId is truly unknown

                    # Determine order within that page+type
                    counter_key = (kpi_page_no, customKpi.VisualType)
                    current_order = custom_order_counters[customKpi.VisualType].get(counter_key, 0) + 1
                    custom_order_counters[customKpi.VisualType][counter_key] = current_order

                    # Stamp the visual
                    item.SectionID = kpi_section_id
                    item.PageNo = kpi_page_no
                    item.Order = current_order

                    if customKpi.VisualType == "Card":
                        all_cards.append(item)
                    elif customKpi.VisualType == "Chart":
                        all_charts.append(item)
                    elif customKpi.VisualType == "Table":
                        all_tables.append(item)
        else:
            print(f"No custom KPIs defined for report {reportId}")

        # Build lean section metadata list (no nested visuals — they are in the flat pools)
        # Include custom pages (6, 7 …) discovered from orphan SectionIds above.
        section_meta_list = [
            SectionMeta(
                SectionId=section.SectionId,
                SectionName=section.SectionName,
                PageNo=page_no,
                Visibility=section.Visbility,
            )
            for page_no, section in enumerate(results, start=1)
        ] + custom_section_meta  # append custom page SectionMeta

        combinedResponse = CombinedSectionResponse(
            Sections=section_meta_list,
            Cards=all_cards,
            Charts=all_charts,
            Tables=all_tables,
        )

        return Result(
            Data=combinedResponse, Status=1, Message="Section Data retrieved Successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getSectionData: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
