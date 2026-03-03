"""
Unit tests for the flat consolidated section data response.

Verifies that getConsolidateSectionData() returns a single-level
{ Cards: [...], Charts: [...], Tables: [...] } structure instead of the
previous nested { ActualData: { Sections: [...] }, CustomData: {...} } structure.
"""

import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Path setup — make backend the import root (mirrors how the server runs)
# ---------------------------------------------------------------------------
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, os.path.abspath(BACKEND_DIR))

# ---------------------------------------------------------------------------
# Helpers to build minimal stub objects
# ---------------------------------------------------------------------------

def _make_card(card_id: str):
    from core.models.visualsModel.CardModel import CardDataModel, FooterModel
    from core.models.visualsModel.ValueObject import ValueObjectModel

    content = ValueObjectModel(Value=1000.0, isPositive=True, Type="currency", Symbol="$")
    comparison = ValueObjectModel(Value=5.0, isPositive=True, Type="percentage", Symbol="%")
    footer = FooterModel(
        ComparisonValue=comparison,
        ComparisonText="From Last Month",
        Visibility=True,
    )
    return CardDataModel(Id=card_id, Title=card_id, Content=content, Footer=footer)


def _make_chart(chart_id: str):
    from core.models.visualsModel.ChartModel import ChartDataModel, YAxisSeriesModel, YaxisControllerModel

    series = YAxisSeriesModel(
        Title="Revenue",
        Type="Bar",
        UnitType="currency",
        Symbol="$",
        AreaFill=False,
        Values=[1000.0, 2000.0],
        YaxisId="left",
        Color="#8FBFD9",
    )
    controller = YaxisControllerModel(Id="left", Orientation="left", Unit="$")
    return ChartDataModel(
        Id=chart_id,
        Title=chart_id,
        Xaxis=["Jan 2025", "Feb 2025"],
        YaxisSeries=[series],
        IndexAxis="x",
        RightYaxis=False,
        YaxisController=[controller],
    )


def _make_table(table_id: str):
    from core.models.visualsModel.TableModel import TableModel

    return TableModel(
        Id=table_id,
        Title=table_id,
        Column=["Particulars", "Value"],
        Rows=[[{"Value": "Revenue", "isPositive": True, "Type": "", "Symbol": ""}]],
    )


def _make_section_data(cards=None, charts=None, tables=None):
    from core.models.visualsModel.SectionData import SectionData

    return SectionData(
        Cards=cards or [],
        Charts=charts or [],
        Tables=tables or [],
    )


def _make_section_result(section_id, section_name, section_data):
    from core.models.visualsModel.SectionData import ConsolidateSectionDate
    from core.models.base.ResultModel import Result

    return Result(
        Data=section_data,
        Status=1,
        Message="ok",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestFlatSectionResponse:
    """Test that the API response is flattened across all sections."""

    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.getCustomKpisList")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.saveResponse")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.AllSectionDataService")
    def test_response_has_flat_keys(self, MockService, mock_save, mock_kpis):
        """Data should contain Cards, Charts, Tables — not ActualData/CustomData/Sections."""
        from services.reportSection.consolidateSection.ConsolidateDataReporting import (
            getConsolidateSectionData,
        )

        # No custom KPIs
        mock_kpis.return_value = None

        # All sections return empty data
        svc = MockService.return_value
        empty = _make_section_data()
        for method in [
            "getFinancialHighlightsSection",
            "getExpensesAnalysisSection",
            "getProfitablitySection",
            "getBreakEvenAnalysisSection",
            "getCashFlowSection",
        ]:
            from core.models.base.ResultModel import Result
            getattr(svc, method).return_value = Result(Data=empty, Status=1, Message="ok")

        result = getConsolidateSectionData(
            year=2025, months=[11], reportType="Month",
            section="", reportId=99999, companyId=123,
        )

        assert result.Status == 1
        data = result.Data
        # Must be a dict or Pydantic model — not nested under ActualData
        if hasattr(data, "model_dump"):
            data = data.model_dump()

        assert "Cards" in data, "Top-level 'Cards' key missing"
        assert "Charts" in data, "Top-level 'Charts' key missing"
        assert "Tables" in data, "Top-level 'Tables' key missing"
        assert "ActualData" not in data, "'ActualData' should not be present in flat response"
        assert "CustomData" not in data, "'CustomData' should not be present in flat response"
        assert "Sections" not in data, "'Sections' should not be present in flat response"

    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.getCustomKpisList")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.saveResponse")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.AllSectionDataService")
    def test_cards_from_all_sections_are_combined(self, MockService, mock_save, mock_kpis):
        """Cards from every section must be merged into one list."""
        from services.reportSection.consolidateSection.ConsolidateDataReporting import (
            getConsolidateSectionData,
        )
        from core.models.base.ResultModel import Result

        mock_kpis.return_value = None
        svc = MockService.return_value

        # Section 1 has 2 cards, others are empty
        section_with_cards = _make_section_data(
            cards=[_make_card("CARD_A"), _make_card("CARD_B")]
        )
        section_with_cards_2 = _make_section_data(
            cards=[_make_card("CARD_C")]
        )
        empty = _make_section_data()

        svc.getFinancialHighlightsSection.return_value = Result(Data=section_with_cards, Status=1, Message="ok")
        svc.getExpensesAnalysisSection.return_value = Result(Data=section_with_cards_2, Status=1, Message="ok")
        svc.getProfitablitySection.return_value = Result(Data=empty, Status=1, Message="ok")
        svc.getBreakEvenAnalysisSection.return_value = Result(Data=empty, Status=1, Message="ok")
        svc.getCashFlowSection.return_value = Result(Data=empty, Status=1, Message="ok")

        result = getConsolidateSectionData(
            year=2025, months=[11], reportType="Month",
            section="", reportId=99999, companyId=123,
        )

        data = result.Data
        if hasattr(data, "model_dump"):
            data = data.model_dump()

        assert len(data["Cards"]) == 3, f"Expected 3 cards combined, got {len(data['Cards'])}"
        card_ids = [c["Id"] for c in data["Cards"]]
        assert "CARD_A" in card_ids
        assert "CARD_B" in card_ids
        assert "CARD_C" in card_ids

    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.getCustomKpisList")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.saveResponse")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.AllSectionDataService")
    def test_charts_from_all_sections_are_combined(self, MockService, mock_save, mock_kpis):
        """Charts from every section must be merged into one list."""
        from services.reportSection.consolidateSection.ConsolidateDataReporting import (
            getConsolidateSectionData,
        )
        from core.models.base.ResultModel import Result

        mock_kpis.return_value = None
        svc = MockService.return_value

        section_a = _make_section_data(charts=[_make_chart("CHART_1"), _make_chart("CHART_2")])
        section_b = _make_section_data(charts=[_make_chart("CHART_3")])
        empty = _make_section_data()

        svc.getFinancialHighlightsSection.return_value = Result(Data=section_a, Status=1, Message="ok")
        svc.getExpensesAnalysisSection.return_value = Result(Data=section_b, Status=1, Message="ok")
        svc.getProfitablitySection.return_value = Result(Data=empty, Status=1, Message="ok")
        svc.getBreakEvenAnalysisSection.return_value = Result(Data=empty, Status=1, Message="ok")
        svc.getCashFlowSection.return_value = Result(Data=empty, Status=1, Message="ok")

        result = getConsolidateSectionData(
            year=2025, months=[11], reportType="Month",
            section="", reportId=99999, companyId=123,
        )

        data = result.Data
        if hasattr(data, "model_dump"):
            data = data.model_dump()

        assert len(data["Charts"]) == 3
        chart_ids = [c["Id"] for c in data["Charts"]]
        assert "CHART_1" in chart_ids
        assert "CHART_2" in chart_ids
        assert "CHART_3" in chart_ids

    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.getCustomKpisList")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.saveResponse")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.AllSectionDataService")
    def test_tables_from_all_sections_are_combined(self, MockService, mock_save, mock_kpis):
        """Tables from every section must be merged into one list."""
        from services.reportSection.consolidateSection.ConsolidateDataReporting import (
            getConsolidateSectionData,
        )
        from core.models.base.ResultModel import Result

        mock_kpis.return_value = None
        svc = MockService.return_value

        section_a = _make_section_data(tables=[_make_table("TABLE_1")])
        section_b = _make_section_data(tables=[_make_table("TABLE_2"), _make_table("TABLE_3")])
        empty = _make_section_data()

        svc.getFinancialHighlightsSection.return_value = Result(Data=section_a, Status=1, Message="ok")
        svc.getExpensesAnalysisSection.return_value = Result(Data=section_b, Status=1, Message="ok")
        svc.getProfitablitySection.return_value = Result(Data=empty, Status=1, Message="ok")
        svc.getBreakEvenAnalysisSection.return_value = Result(Data=empty, Status=1, Message="ok")
        svc.getCashFlowSection.return_value = Result(Data=empty, Status=1, Message="ok")

        result = getConsolidateSectionData(
            year=2025, months=[11], reportType="Month",
            section="", reportId=99999, companyId=123,
        )

        data = result.Data
        if hasattr(data, "model_dump"):
            data = data.model_dump()

        assert len(data["Tables"]) == 3
        table_ids = [t["Id"] for t in data["Tables"]]
        assert "TABLE_1" in table_ids
        assert "TABLE_2" in table_ids
        assert "TABLE_3" in table_ids

    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.customKPICreation")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.getCustomKpisList")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.saveResponse")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.AllSectionDataService")
    def test_custom_kpi_card_appended_to_flat_cards(self, MockService, mock_save, mock_kpis, mock_custom):
        """Custom KPI cards must be merged into the flat Cards list."""
        from services.reportSection.consolidateSection.ConsolidateDataReporting import (
            getConsolidateSectionData,
        )
        from core.models.base.ResultModel import Result

        svc = MockService.return_value
        empty = _make_section_data()
        for method in [
            "getFinancialHighlightsSection",
            "getExpensesAnalysisSection",
            "getProfitablitySection",
            "getBreakEvenAnalysisSection",
            "getCashFlowSection",
        ]:
            getattr(svc, method).return_value = Result(Data=empty, Status=1, Message="ok")

        # One custom card KPI
        custom_kpi = MagicMock()
        custom_kpi.VisualType = "Card"
        custom_kpi.SectionName = "Custom Section"
        custom_kpi.Items = []
        mock_kpis.return_value = {99999: [custom_kpi]}

        custom_card = _make_card("CUSTOM_CARD_1")
        mock_custom.return_value = Result(Data=custom_card, Status=1, Message="ok")

        result = getConsolidateSectionData(
            year=2025, months=[11], reportType="Month",
            section="", reportId=99999, companyId=123,
        )

        data = result.Data
        if hasattr(data, "model_dump"):
            data = data.model_dump()

        assert len(data["Cards"]) == 1
        assert data["Cards"][0]["Id"] == "CUSTOM_CARD_1"

    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.getCustomKpisList")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.saveResponse")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.AllSectionDataService")
    def test_empty_sections_return_empty_lists(self, MockService, mock_save, mock_kpis):
        """When all sections are empty and no custom KPIs, all lists must be empty."""
        from services.reportSection.consolidateSection.ConsolidateDataReporting import (
            getConsolidateSectionData,
        )
        from core.models.base.ResultModel import Result

        mock_kpis.return_value = None
        svc = MockService.return_value
        empty = _make_section_data()
        for method in [
            "getFinancialHighlightsSection",
            "getExpensesAnalysisSection",
            "getProfitablitySection",
            "getBreakEvenAnalysisSection",
            "getCashFlowSection",
        ]:
            getattr(svc, method).return_value = Result(Data=empty, Status=1, Message="ok")

        result = getConsolidateSectionData(
            year=2025, months=[11], reportType="Month",
            section="", reportId=99999, companyId=123,
        )

        data = result.Data
        if hasattr(data, "model_dump"):
            data = data.model_dump()

        assert data["Cards"] == []
        assert data["Charts"] == []
        assert data["Tables"] == []

    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.getCustomKpisList")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.saveResponse")
    @patch("services.reportSection.consolidateSection.ConsolidateDataReporting.AllSectionDataService")
    def test_status_is_success(self, MockService, mock_save, mock_kpis):
        """Status should be 1 on a successful response."""
        from services.reportSection.consolidateSection.ConsolidateDataReporting import (
            getConsolidateSectionData,
        )
        from core.models.base.ResultModel import Result

        mock_kpis.return_value = None
        svc = MockService.return_value
        empty = _make_section_data()
        for method in [
            "getFinancialHighlightsSection",
            "getExpensesAnalysisSection",
            "getProfitablitySection",
            "getBreakEvenAnalysisSection",
            "getCashFlowSection",
        ]:
            getattr(svc, method).return_value = Result(Data=empty, Status=1, Message="ok")

        result = getConsolidateSectionData(
            year=2025, months=[11], reportType="Month",
            section="", reportId=99999, companyId=123,
        )

        assert result.Status == 1
        assert result.Message == "Section Data retrieved Successfully"
