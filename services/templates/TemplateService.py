import uuid
from core.models.base.ResultModel import Result
from core.models.base.TemplateModel import (
    Template,
    TemplatePage,
    TemplatePageCategory,
    CreateTemplateRequest,
    UpdateTemplateRequest,
)
from helper.TemplateStorage import (
    loadTemplates,
    addTemplate,
    removeTemplate,
    updateTemplatePages,
)

# ──────────────────────────────────────────────────────────────────────────────
# Default template derived from SectionComponents.json section groupings.
# Each page corresponds to a report section, with only the visual IDs that
# belong to that section (duplicates across sections are kept in their
# primary section only).
# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_TEMPLATE = Template(
    id="default",
    name="Default Layout",
    isDefault=True,
    pages=[
        TemplatePage(
            pageNo=1,
            pageName="Financial Highlights",
            category=TemplatePageCategory(
                Cards=[
                    "REVENUE_CARD",
                    "COST_OF_GOODS_SOLD_CARD",
                    "OPERATING_EXPENSES_CARD",
                    "NET_INCOME_CARD",
                ],
                Charts=[
                    "REVENUE_CHART",
                    "REVENUE_BUDGET_CHART",
                    "COS_BUDGET_CHART",
                ],
                Tables=["INCOME_STATEMENT_TABLE"],
            ),
        ),
        TemplatePage(
            pageNo=2,
            pageName="Expenses Analysis",
            category=TemplatePageCategory(
                Cards=[],
                Charts=[
                    "KEY_METRICS_CHART",
                    "EXPENSES_TO_REVENUE_RATION_CHART",
                ],
                Tables=[],
            ),
        ),
        TemplatePage(
            pageNo=3,
            pageName="Profitability",
            category=TemplatePageCategory(
                Cards=[],
                Charts=["PROFITABILITY_CHART", "NET_PROFIT_MARGIN_CHART"],
                Tables=[],
            ),
        ),
        TemplatePage(
            pageNo=4,
            pageName="Breakeven Analysis",
            category=TemplatePageCategory(
                Cards=[
                    "EXPENSES_TO_REVENUE_RATION_CARD",
                    "BREAKEVEN_GAP_OF_SAFETY_CARD",
                    "BREAKEVEN_POINT_CARD",
                ],
                Charts=[],
                Tables=[],
            ),
        ),
        TemplatePage(
            pageNo=5,
            pageName="Cash Flow Analysis",
            category=TemplatePageCategory(
                Cards=[
                    "OPERATING_CASH_FLOW_CARD",
                    "FREE_CASH_FLOW_CARD",
                    "CASH_ON_HAND_CARD",
                ],
                Charts=["CASH_POSITION_CHART"],
                Tables=[],
            ),
        ),
    ],
)


def getDefaultTemplate() -> Result:
    return Result(Data=DEFAULT_TEMPLATE.model_dump(), Status=1, Message="Default template")


def getCustomTemplates(reportId: int) -> Result:
    file = loadTemplates(reportId)
    return Result(
        Data=[t.model_dump() for t in file.templates],
        Status=1,
        Message="Custom templates retrieved",
    )


def createCustomTemplate(reportId: int, request: CreateTemplateRequest) -> Result:
    template = Template(
        id=str(uuid.uuid4()),
        name=request.name,
        isDefault=False,
        pages=request.pages,
    )
    addTemplate(reportId, template)
    return Result(
        Data=template.model_dump(),
        Status=1,
        Message="Template saved successfully",
    )


def deleteCustomTemplate(reportId: int, templateId: str) -> Result:
    deleted = removeTemplate(reportId, templateId)
    if not deleted:
        return Result(Data=None, Status=0, Message=f"Template '{templateId}' not found")
    return Result(Data=None, Status=1, Message="Template deleted successfully")


def updateCustomTemplate(reportId: int, templateId: str, request: UpdateTemplateRequest) -> Result:
    updated = updateTemplatePages(reportId, templateId, request.pages)
    if not updated:
        return Result(Data=None, Status=0, Message=f"Template '{templateId}' not found")
    return Result(Data=updated.model_dump(), Status=1, Message="Template updated successfully")
