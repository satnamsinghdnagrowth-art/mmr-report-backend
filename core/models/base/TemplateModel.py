from pydantic import BaseModel
from typing import List, Optional


class TemplatePageCategory(BaseModel):
    """Visual IDs (not objects) assigned to each category on a template page."""
    Cards: List[str] = []
    Charts: List[str] = []
    Tables: List[str] = []


class TemplatePage(BaseModel):
    pageNo: int
    pageName: str
    category: TemplatePageCategory


class Template(BaseModel):
    id: str
    name: str
    isDefault: bool = False
    pages: List[TemplatePage]


class CreateTemplateRequest(BaseModel):
    name: str
    pages: List[TemplatePage]


class UpdateTemplateRequest(BaseModel):
    pages: List[TemplatePage]


class TemplatesFile(BaseModel):
    templates: List[Template] = []
