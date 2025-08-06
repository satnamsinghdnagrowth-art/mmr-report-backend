from fastapi import APIRouter
from core.models.base.ResultModel import Result
from services.reportSection.cashFlowAnalysis.sectionData.SectionData import (
    getSectionData,
)
from core.models.visualsModel.CardModel import CardDataModel,FooterModel
from helper.GetValueSymbol import getValueSymbol
from core.models.visualsModel.TableModel import TableModel
from core.models.visualsModel.ValueObject import ValueObjectModel
from core.models.visualsModel.SectionData import SectionData
import pandas as pd
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from helper.readExcel import readExcelFile

BudgetSectionRouter = APIRouter()

# # Get Financial Higlights Section All Data
@BudgetSectionRouter.post("/get/report/60847/sectionData/")
def getSection():

    configs = SECTION_CARD_CONFIGS.get('Budget Comparison')

    cardsList = [card['mainFunction'] for card in configs['cards']]

    tableComponentsList = [table['func'] for table in configs['tables'][0]['rows']]

    data = pd.read_excel("tempFiles/DXone ERP May 2025_07.11.2025-1200.xlsx",sheet_name="KPI Sheet")

    headerRow = list(data.columns)

    headerRow = list(data.columns)

    data = data.fillna("")
    cards = []

    # Cards Section
    for row in data.to_dict(orient="records"):

        kpi = str(row["KPI"]).strip()

        if not kpi or kpi not in cardsList:
            continue


        if row["This Month"] != "":
            valueData = getValueSymbol(row["KPI"])

            valueType = valueData["type"]
            valueSymbol = valueData["symbol"]

            if kpi in ['Total Customer Count','Live']:
                valueSymbol = ""
                valueType = ""

            if kpi == 'Cash RunWay':
                valueSymbol = " Months"
                valueType = "months"

            title = row["KPI"]
            content = ValueObjectModel(
                    Value=row ["This Month"],
                    isPositive=True,     # or compute from cell if needed
                    Type=valueType,             # set if needed
                    Symbol=valueSymbol           # set if needed
                )
            comparisonValue = ValueObjectModel(
                    Value=row["Variance %"],
                    isPositive=True,     # or compute from cell if needed
                    Type="percentage",             # set if needed
                    Symbol="%"           # set if needed
                )
            comparisontext = "From Prev Month"

            footerModelObj = FooterModel(ComparisonValue=comparisonValue,ComparisonText=comparisontext)

            cardModelObj = CardDataModel(Title=title,Content=content,Footer=footerModelObj)
            
            cards.append(cardModelObj)

    # Table for the budget section
    Rows = []

    for row in data.values.tolist():

        kpiName = row[0]

        if not kpiName or kpiName not in tableComponentsList:
            continue

        valueData = getValueSymbol(row[0])
        
        valueSymbol = ""
        valueType = ""
        
        if row[1] != "" :
            valueType = valueData["type"] 
            valueSymbol = valueData["symbol"]

        if kpiName in ['Total Customer Count','Cash RunWay','Live']:
            valueSymbol = ""
            valueType = ""

        if kpiName == 'Burn Rate':
            valueSymbol = "%"
            valueType = "percentage"


 
        row_objs = []
        for cell in row:
            if cell == '':
                continue

            # Wrap each cell — add your logic for isPositive, Type, Symbol
            row_objs.append(
                ValueObjectModel(
                    Value=cell,
                    isPositive=True,     # or compute from cell if needed
                    Type=valueType,             # set if needed
                    Symbol=valueSymbol           # set if needed
                )
            )
        Rows.append(row_objs)

    table = TableModel(
        Title="Budget Section",
        Column=headerRow,
        Rows=Rows
    )

    cards_data = cards
    charts_data = []

    # Combine into SectionData
    section_data = SectionData(
        Charts=charts_data, Cards=cards_data, Tables=[table]
    )

    return Result(
        Data=section_data,
        Status=1,
        Message="Section data retrieved successfully",
    )

  