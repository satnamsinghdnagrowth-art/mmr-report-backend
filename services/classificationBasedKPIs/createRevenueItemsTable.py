from datetime import datetime
from core.models.base.ResultModel import Result
from helper.GetFileByReportId import getReportData
from helper.LoadJsonData import financialDataTest
import calendar
from core.models.visualsModel.TableModel import TableModel, TableListModel

from core.models.visualsModel.ValueObject import ValueObjectModel
from datetime import datetime
from core.models.base.SourceModel import SourceDataTypes
from helper.GetFinancialData import getFinancialData

def createRevenueItemsTable():
    try:
        current_month = 9
        reportId = 72669
        classification_code = "REVENUE"

        financialData = getFinancialData(reportId, SourceDataTypes.Actuals)
        # Table header
        header_values = [
            "REVENUE",
            f"{calendar.month_abbr[current_month]}-2025",
            f"{calendar.month_abbr[current_month - 1]}-2025",
            "This month vs budget($)",
            "This month vs last month($)",
            "2025 (YTD)",
            f"Common Size % ({calendar.month_abbr[current_month]}-2025)",
        ]

        rows = []

        for key, item in financialData.items():
            if classification_code in list(item.keys()):
                for _, j in item[classification_code]["LineItems"].items():
                    months = {8: "Aug 2025", 9: "Sep 2025"}

                    for source, records in j.items():
                        record_dict = {
                            months.get(r["Month"], f"{r['Month']}-{r['Year']}"): r[
                                "Value"
                            ]
                            for r in records
                        }

                        sep = record_dict.get("Sep 2025", 0)
                        aug = record_dict.get("Aug 2025", 0)

                        budget = 0
                        diff_budget = sep - budget
                        diff_month = sep - aug

                        # Build row with ValueObjectModel
                        row = [
                            ValueObjectModel(Value=source, isPositive=True),
                            ValueObjectModel(
                                Value=sep, isPositive=sep >= 0, Symbol="$"
                            ),
                            ValueObjectModel(
                                Value=aug, isPositive=aug >= 0, Symbol="$"
                            ),
                            ValueObjectModel(
                                Value=diff_budget,
                                isPositive=diff_budget >= 0,
                                Symbol="$",
                            ),
                            ValueObjectModel(
                                Value=diff_month, isPositive=diff_month >= 0, Symbol="$"
                            ),
                            ValueObjectModel(
                                Value=0, isPositive=True, Symbol="$"
                            ),  # YTD placeholder
                            ValueObjectModel(
                                Value=0, isPositive=True, Symbol="%"
                            ),  # Common Size placeholder
                        ]

                        rows.append(row)
                break

        # Build table object
        table = TableModel(
            Title="Revenue Items Table",
            Column=header_values,
            Rows=rows,
        )

        # Return TableListModel
        table_list = TableListModel(Tables=[table])

        return Result(
            Data=table_list.dict(), Status=1, Message="Data fetched successfully"
        )

    except Exception as ex:
        message = f"Error occur at fileUpload: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
