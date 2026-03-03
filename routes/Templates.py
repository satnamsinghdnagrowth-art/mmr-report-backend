from fastapi import APIRouter
from core.models.base.ResultModel import Result
from core.models.base.TemplateModel import CreateTemplateRequest, UpdateTemplateRequest
from services.templates.TemplateService import (
    getDefaultTemplate,
    getCustomTemplates,
    createCustomTemplate,
    deleteCustomTemplate,
    updateCustomTemplate,
)

TemplatesRouter = APIRouter()


@TemplatesRouter.get("/default", response_model=Result)
def fetchDefaultTemplate():
    return getDefaultTemplate()


@TemplatesRouter.get("/get/report/{reportId}", response_model=Result)
def fetchCustomTemplates(reportId: int):
    return getCustomTemplates(reportId)


@TemplatesRouter.post("/create/report/{reportId}", response_model=Result)
def saveCustomTemplate(reportId: int, request: CreateTemplateRequest):
    return createCustomTemplate(reportId, request)


@TemplatesRouter.put("/update/{templateId}/report/{reportId}", response_model=Result)
def updateTemplate(templateId: str, reportId: int, request: UpdateTemplateRequest):
    return updateCustomTemplate(reportId, templateId, request)


@TemplatesRouter.delete("/delete/{templateId}/report/{reportId}", response_model=Result)
def removeTemplate(templateId: str, reportId: int):
    return deleteCustomTemplate(reportId, templateId)
