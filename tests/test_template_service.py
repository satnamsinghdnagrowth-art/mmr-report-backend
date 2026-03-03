"""
Unit tests for the template service and storage layer.

Tests cover:
  1. getDefaultTemplate — structure and key fields
  2. createCustomTemplate — persists + returns the new template
  3. getCustomTemplates — returns saved templates for a report
  4. deleteCustomTemplate — removes an existing template; rejects unknown id
  5. TemplateStorage helpers — load / save / add / remove in isolation
"""

import json
import os
import shutil
import tempfile
import pytest

# ── Patch TEMPLATES_DIR before any service import ──────────────────────────

TEMP_DIR = tempfile.mkdtemp()

import config.FilesBaseDIR as _fbd

_original_templates_dir = _fbd.TEMPLATES_DIR
_fbd.TEMPLATES_DIR = TEMP_DIR

# Now import after patching
import importlib
import helper.TemplateStorage as ts
importlib.reload(ts)
from helper.TemplateStorage import (
    loadTemplates,
    saveTemplates,
    addTemplate,
    removeTemplate,
)
from core.models.base.TemplateModel import (
    Template,
    TemplatePage,
    TemplatePageCategory,
    TemplatesFile,
    CreateTemplateRequest,
)
from services.templates.TemplateService import (
    getDefaultTemplate,
    getCustomTemplates,
    createCustomTemplate,
    deleteCustomTemplate,
    DEFAULT_TEMPLATE,
)


# ── Fixtures ────────────────────────────────────────────────────────────────

REPORT_ID = 99999  # unlikely to collide


@pytest.fixture(autouse=True)
def clean_report_file():
    """Remove the test report's template file before and after each test."""
    path = f"{TEMP_DIR}/{REPORT_ID}.json"
    if os.path.exists(path):
        os.remove(path)
    yield
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture(scope="session", autouse=True)
def cleanup_temp_dir():
    yield
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    _fbd.TEMPLATES_DIR = _original_templates_dir


def _make_template(name="Test Tmpl") -> Template:
    return Template(
        id="test-id-001",
        name=name,
        isDefault=False,
        pages=[
            TemplatePage(
                pageNo=1,
                pageName="Page One",
                category=TemplatePageCategory(
                    Cards=["REVENUE_CARD"],
                    Charts=["REVENUE_CHART"],
                    Tables=[],
                ),
            )
        ],
    )


# ── Default template ────────────────────────────────────────────────────────

class TestGetDefaultTemplate:
    def test_status_is_success(self):
        result = getDefaultTemplate()
        assert result.Status == 1

    def test_returns_dict_data(self):
        result = getDefaultTemplate()
        assert isinstance(result.Data, dict)

    def test_default_is_flagged(self):
        result = getDefaultTemplate()
        assert result.Data["isDefault"] is True

    def test_has_five_pages(self):
        result = getDefaultTemplate()
        assert len(result.Data["pages"]) == 5

    def test_first_page_is_financial_highlights(self):
        result = getDefaultTemplate()
        assert result.Data["pages"][0]["pageName"] == "Financial Highlights"

    def test_first_page_has_revenue_card(self):
        result = getDefaultTemplate()
        cards = result.Data["pages"][0]["category"]["Cards"]
        assert "REVENUE_CARD" in cards

    def test_profitability_page_has_profitability_chart(self):
        result = getDefaultTemplate()
        page = next(p for p in result.Data["pages"] if p["pageName"] == "Profitability")
        assert "PROFITABILITY_CHART" in page["category"]["Charts"]

    def test_cash_flow_page_has_cash_position_chart(self):
        result = getDefaultTemplate()
        page = next(p for p in result.Data["pages"] if "Cash Flow" in p["pageName"])
        assert "CASH_POSITION_CHART" in page["category"]["Charts"]


# ── Create custom template ──────────────────────────────────────────────────

class TestCreateCustomTemplate:
    def test_status_is_success(self):
        req = CreateTemplateRequest(
            name="My Template",
            pages=_make_template().pages,
        )
        result = createCustomTemplate(REPORT_ID, req)
        assert result.Status == 1

    def test_returned_data_has_id(self):
        req = CreateTemplateRequest(name="T1", pages=_make_template().pages)
        result = createCustomTemplate(REPORT_ID, req)
        assert result.Data["id"]

    def test_returned_name_matches(self):
        req = CreateTemplateRequest(name="Named Template", pages=_make_template().pages)
        result = createCustomTemplate(REPORT_ID, req)
        assert result.Data["name"] == "Named Template"

    def test_template_persisted_to_file(self):
        req = CreateTemplateRequest(name="Persist Me", pages=_make_template().pages)
        createCustomTemplate(REPORT_ID, req)
        file = loadTemplates(REPORT_ID)
        assert len(file.templates) == 1
        assert file.templates[0].name == "Persist Me"


# ── Get custom templates ────────────────────────────────────────────────────

class TestGetCustomTemplates:
    def test_empty_when_no_file(self):
        result = getCustomTemplates(REPORT_ID)
        assert result.Status == 1
        assert result.Data == []

    def test_returns_saved_template(self):
        addTemplate(REPORT_ID, _make_template("My Saved"))
        result = getCustomTemplates(REPORT_ID)
        assert len(result.Data) == 1
        assert result.Data[0]["name"] == "My Saved"

    def test_returns_multiple_templates(self):
        addTemplate(REPORT_ID, _make_template("T1"))
        addTemplate(REPORT_ID, _make_template("T2"))
        result = getCustomTemplates(REPORT_ID)
        assert len(result.Data) == 2


# ── Delete custom template ──────────────────────────────────────────────────

class TestDeleteCustomTemplate:
    def test_delete_existing_returns_success(self):
        tmpl = _make_template()
        addTemplate(REPORT_ID, tmpl)
        result = deleteCustomTemplate(REPORT_ID, tmpl.id)
        assert result.Status == 1

    def test_delete_removes_from_file(self):
        tmpl = _make_template()
        addTemplate(REPORT_ID, tmpl)
        deleteCustomTemplate(REPORT_ID, tmpl.id)
        file = loadTemplates(REPORT_ID)
        assert len(file.templates) == 0

    def test_delete_unknown_id_returns_failure(self):
        result = deleteCustomTemplate(REPORT_ID, "nonexistent-id")
        assert result.Status == 0

    def test_delete_only_removes_target(self):
        t1 = Template(id="id-1", name="Keep", isDefault=False, pages=_make_template().pages)
        t2 = Template(id="id-2", name="Remove", isDefault=False, pages=_make_template().pages)
        addTemplate(REPORT_ID, t1)
        addTemplate(REPORT_ID, t2)
        deleteCustomTemplate(REPORT_ID, "id-2")
        file = loadTemplates(REPORT_ID)
        assert len(file.templates) == 1
        assert file.templates[0].id == "id-1"


# ── TemplateStorage helpers ─────────────────────────────────────────────────

class TestTemplateStorage:
    def test_load_returns_empty_when_no_file(self):
        file = loadTemplates(REPORT_ID)
        assert isinstance(file, TemplatesFile)
        assert file.templates == []

    def test_save_and_reload(self):
        tf = TemplatesFile(templates=[_make_template()])
        saveTemplates(REPORT_ID, tf)
        loaded = loadTemplates(REPORT_ID)
        assert len(loaded.templates) == 1

    def test_add_appends_template(self):
        addTemplate(REPORT_ID, _make_template("A"))
        addTemplate(REPORT_ID, _make_template("B"))
        file = loadTemplates(REPORT_ID)
        assert len(file.templates) == 2

    def test_remove_returns_true_when_found(self):
        t = _make_template()
        addTemplate(REPORT_ID, t)
        assert removeTemplate(REPORT_ID, t.id) is True

    def test_remove_returns_false_when_not_found(self):
        assert removeTemplate(REPORT_ID, "fake-id") is False
