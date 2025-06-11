from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.charts.retrieveChart import retrieveChart
from services.reportSection.financialHighlights.charts.RevenueBreakdown import (
    getRevenueBreakdownChart,
)
from datetime import datetime


# Get the sections cards
def getSectionCharts(
    year: int, months: list[int], reportType: str, section: str, reportId: int
):
    try:
        months = [1,2,3,4,5,6,7,8,9,10,11,12]

        configs = SECTION_CARD_CONFIGS.get(section)

        if not configs:
            return Result(
                Data=[],
                Status=1,
                Message=f"No cards configured for section '{section}'",
            )

        charts = []

        for config in configs.get("charts"):
            card = retrieveChart(
                reportId=reportId,
                year=year,
                months=months,
                title=config["title"],
                rigthYaxis=config["rigthYaxis"],
                chartData=config["data"],
                axisChoice=config["indexAxis"],
                reportType=reportType,
            )
            charts.append(card.Data)

        charts.append(getRevenueBreakdownChart(year, months, reportId).Data)

        return Result(
            Data=charts, Status=1, Message="Revenue Card calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
