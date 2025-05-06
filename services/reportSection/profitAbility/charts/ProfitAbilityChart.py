from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.charts.retrieveChart import retrieveChart
from services.reportSection.financialHeights.charts.RevenueBreakdown import (
    getRevenueBreakdownChart,
)
from datetime import datetime


# Get the sections cards
def getPACharts(year: int, months: list[int], reportType: str, section: str):
    try:
        configs = SECTION_CARD_CONFIGS.get("Expenses Analysis")

        if not configs:
            return Result(
                Data=[],
                Status=1,
                Message=f"No cards configured for section '{section}'",
            )

        charts = []

        for config in configs.get("charts"):
            card = retrieveChart(
                year=year,
                months=months,
                title=config["title"],
                chartData=config["data"],
                axisChoice=config["indexAxis"],
            )
            charts.append(card.Data)


        return Result(
            Data=charts, Status=1, Message="Revenue Card calculated successfully"
        )

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
