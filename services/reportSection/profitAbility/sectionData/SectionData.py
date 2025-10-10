from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from services.reportSection.profitAbility.tables.GetProfitAbilityTable import getPATable
from core.models.visualsModel.SectionData import SectionData
from services.visuals.charts.GetSectionCharts import getSectionCharts


# Get the sections cards
def getSectionData(
    year: int, months: list[int], reportType: str, section: str, reportId
):
    try:
        months = (
            [i for i in range(1, months[0] + 1)]
            if reportType.lower() == "year"
            else months
        )
        cardsData = []
        chartsData = getSectionCharts(year, months, reportType, section, reportId).Data
        tablesData = getPATable(year, months, reportType, section, reportId).Data
        sectionData = SectionData(Charts=chartsData, Cards=cardsData, Tables=tablesData)

        return Result(
            Data=sectionData, Status=1, Message="Section Data retrieved Successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
