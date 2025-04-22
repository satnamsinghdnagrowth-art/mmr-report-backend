from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from helper.getMonthName import getMonthName
from config.variable import variableMapping
from core.models.base.ResultModel import Result

# Recursively nested defaultdict
def nested_dict():
    return defaultdict(nested_dict)


# Convert nested defaultdicts to plain dict
def convert_defaultdict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_defaultdict(v) for k, v in d.items()}
    elif isinstance(d, dict):
        d = {k: convert_defaultdict(v) for k, v in d.items()}
    return d


# Analyze the data
from helper.readExcel import readExcelFile
from datetime import datetime
from collections import defaultdict
from helper.getMonthName import getMonthName
from config.variable import variableMapping
from core.models.base.ResultModel import Result

def nested_dict():
    return defaultdict(nested_dict)

def convert_defaultdict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_defaultdict(v) for k, v in d.items()}
    elif isinstance(d, dict):
        d = {k: convert_defaultdict(v) for k, v in d.items()}
    return d

def retriveCOAValues(category: str, month=4, year=2023):
    try:
        filePath = "tempFiles/Honest Game Corporation Jan 2025 (4).xlsx"
        excelData = readExcelFile(filePath)
        data = excelData.Data
        cleanedData = data[~data["Classification"].isnull()]
        BSData = variableMapping[category]

        result = defaultdict(lambda: {
            "Classification": {},
            "LineItems": {},
            "Total": []
        })

        for section, categories in BSData.items():
            sectionLineItems = {}

            for category in categories:
                classification = list(category.keys())[0]
                displayname = list(category.values())[0]

                # --- Classification Total ---
                matches = cleanedData[cleanedData["Classification"] == classification]
                matches = matches.drop(columns=["Classification", "Account Name"], errors='ignore')
                month_cols = list(matches.columns)

                classificationTotal = []
                for month in month_cols:
                    try:
                        value = matches[month].fillna(0).sum()
                        date_obj = datetime.strptime(month, "%b %Y")
                        classificationTotal.append({
                            "Month": date_obj.month,
                            "Year": date_obj.year,
                            "Value": round(value, 2),
                        })
                    except:
                        continue

                result[section]["Classification"][displayname] = classificationTotal

                # --- Line Items ---
                for code in category:
                    matches = cleanedData[cleanedData["Classification"] == code]

                    for _, row in matches.iterrows():
                        accountName = row["Account Name"]
                        item_matches = cleanedData[cleanedData["Account Name"] == accountName]
                        item_matches = item_matches.drop(columns=["Classification", "Account Name"], errors='ignore')

                        month_cols = list(item_matches.columns)
                        lineItemsTotal = []

                        for month in month_cols:
                            try:
                                value = item_matches[month].fillna(0).sum()
                                date_obj = datetime.strptime(month, "%b %Y")
                                lineItemsTotal.append({
                                    "Month": date_obj.month,
                                    "Year": date_obj.year,
                                    "Value": round(value, 2),
                                })
                            except:
                                continue

                        sectionLineItems[accountName] = lineItemsTotal

            # Add all line items to result
            result[section]["LineItems"] = sectionLineItems

            # --- Total at section level ---
            total_by_month = defaultdict(float)
            for items in sectionLineItems.values():
                for item in items:
                    key = f"{item['Month']:02d}-{item['Year']}"
                    total_by_month[key] += item["Value"]

            sectionTotal = []
            for key, value in total_by_month.items():
                month, year = map(int, key.split("-"))
                sectionTotal.append({
                    "Month": month,
                    "Year": year,
                    "Value": round(value, 2)
                })

            result[section]["Total"] = sectionTotal

        final_result = convert_defaultdict(result)
        return Result(Data=final_result, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occur at retriveAccountNames: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)
