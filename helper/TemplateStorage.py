import json
import os
from config.FilesBaseDIR import TEMPLATES_DIR
from core.models.base.TemplateModel import Template, TemplatesFile


def _report_path(reportId: int) -> str:
    return f"{TEMPLATES_DIR}/{reportId}.json"


def _ensure_dir():
    os.makedirs(TEMPLATES_DIR, exist_ok=True)


def loadTemplates(reportId: int) -> TemplatesFile:
    """Load all custom templates for a given report."""
    path = _report_path(reportId)
    if not os.path.exists(path):
        return TemplatesFile(templates=[])
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return TemplatesFile(**data)
    except Exception as ex:
        print(f"[TemplateStorage] Error loading templates for report {reportId}: {ex}")
        return TemplatesFile(templates=[])


def saveTemplates(reportId: int, templatesFile: TemplatesFile):
    """Persist all templates for a given report."""
    _ensure_dir()
    path = _report_path(reportId)
    try:
        with open(path, "w") as f:
            json.dump(templatesFile.model_dump(), f, indent=2)
    except Exception as ex:
        print(f"[TemplateStorage] Error saving templates for report {reportId}: {ex}")
        raise


def addTemplate(reportId: int, template: Template):
    """Append a new template to the report's file."""
    file = loadTemplates(reportId)
    file.templates.append(template)
    saveTemplates(reportId, file)


def removeTemplate(reportId: int, templateId: str) -> bool:
    """Remove a template by id. Returns True if found and removed."""
    file = loadTemplates(reportId)
    original_count = len(file.templates)
    file.templates = [t for t in file.templates if t.id != templateId]
    if len(file.templates) == original_count:
        return False
    saveTemplates(reportId, file)
    return True


def updateTemplatePages(reportId: int, templateId: str, pages: list):
    """Replace the pages of an existing template. Returns the updated Template or None if not found."""
    file = loadTemplates(reportId)
    for template in file.templates:
        if template.id == templateId:
            template.pages = pages
            saveTemplates(reportId, file)
            return template
    return None
