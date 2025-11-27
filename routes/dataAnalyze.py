from fastapi import APIRouter
from core.models.base.ResultModel import Result
from services.ExtractDataRange import retriveDataRange
from fastapi import APIRouter, Body
from core.models.base.ResultModel import Result
from weasyprint import HTML

ReportRouter = APIRouter()

#  <-------------------- Get report Date Range ---------------------->
@ReportRouter.get("/{reportId}/get/range", response_model=Result)
def getReportDataRange(reportId: int):
    return retriveDataRange(reportId)


# <-------------------- Download Report PDF ---------------------->
@ReportRouter.post("/download/PDF", response_model=Result)
def pdfGenerator(base64str=Body(...)):
    htmlContent = base64str["base64str"]

    # Save PDF to a file path
    html = HTML(string=htmlContent)

    file_path = "database/ReportsPdf/test.pdf"

    html.write_pdf(file_path)

    return Result(
        Data="/database/ReportsPdf/test.pdf",
        Status=0,
        Message="PDF generated and ready for download",
    )
