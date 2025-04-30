from datetime import datetime
from core.models.base.ResultModel import Result
from datetime import datetime
from services.reportSection.financialHeights.cardsKPIs import getSectionCards
from services.reportSection.financialHeights.chartsKPIs import getSectionCharts
from core.models.visualsModel.SectionData import SectionData
from services.reportSection.financialHeights.IncomeStatementTablesKPI import getISTable
 

# Get the sections cards
def getSectionData(year:int,months:list[int],reportType:str,section:str):
    try:
        cardsData = getSectionCards(year,months,reportType,section).Data
        chartsData = getSectionCharts(year,months,reportType,section).Data
        tablesData = getISTable(year,months,reportType,section).Data
        sectionData = SectionData(Charts=chartsData,Cards=cardsData,Tables=tablesData)

        return Result(
            Data=sectionData,
            Status=1,
            Message="Section Data retrieved Successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    
