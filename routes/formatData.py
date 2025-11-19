from fastapi import APIRouter, Body, UploadFile, File, Form
from core.models.base.ResultModel import Result
from services.fileUploadHandling.FileUpload import fileUpload
from services.reports.UpdateReportData import updateReportFields
from typing import Optional
from core.models.base.SectionDataRequestBody import SectionRequestData
from weasyprint import HTML
from services.generateSummary.ExecutiveSummaryGenerator import generateExecutiveSummary


dataFormat = APIRouter()


# File upload endpoint
@dataFormat.post("/upload", response_model=Result)
def formatReportData(
    file: Optional[UploadFile] = File(None),
    FileBase64Str: Optional[str] = Form(None),
    CompanyLogo: Optional[UploadFile] = File(None),
):
    if not file and not FileBase64Str:
        return Result(
            Status=400, Message="Either file or FileBase64Str must be provided."
        )

    return fileUpload(file, FileBase64Str, CompanyLogo)


@dataFormat.patch("/update/report/{reportId}/")
def uploadLogo(reportId: int, CompanyLogo: Optional[UploadFile] = File(None)):
    return updateReportFields(reportId, CompanyLogo)


# downloadPDF
@dataFormat.post("/downloadPDF", response_model=Result)
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
