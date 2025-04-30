from datetime import datetime
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.card.retrieveCard import retrieveCard
from datetime import datetime

# Get the sections cards
def getSectionCards(year:int,months:list[int],reportType:str,section:str):
    try:
        comparedTo = "From Prev Year" if reportType.lower() == "yearly" else "From Prev Month"

        configs = SECTION_CARD_CONFIGS.get(section)

        if not configs:
            return Result(Data=[], Status=1, Message=f"No cards configured for section '{section}'")

        cards = []

        for config in configs.get("cards"):
            card = retrieveCard(
                year=year,
                months=months,
                title=config["title"],
                functionName=config["mainFunction"],
                comparisonFunc=config["comparisonFunction"],
                comparedTo=comparedTo
            )
            cards.append(card.Data)
         
        return Result(
            Data=cards,
            Status=1,
            Message="Revenue Card calculated successfully"
        )

    except ZeroDivisionError as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)

    except Exception as ex:
        message = f"Error occurred at getFHSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
    
