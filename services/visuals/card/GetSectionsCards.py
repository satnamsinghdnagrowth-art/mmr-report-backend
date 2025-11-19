from datetime import datetime
from typing import List, Optional
from core.models.base.ResultModel import Result
from helper.LoadJsonData import SECTION_CARD_CONFIGS
from services.visuals.card.retrieveCard import retrieveCard


def getSectionCards(
    year: int,
    months: List[int],
    reportType: str,
    section: str,
    reportId: int,
    config="",
) -> Result:
    try:
        compared_to = (
            "From Last Year" if reportType.lower() == "year" else "From Last Month"
        )

        configs = SECTION_CARD_CONFIGS.get(section)

        if not configs or "cards" not in configs:
            return Result(
                Data=[],
                Status=1,
                Message=f"No cards configured for section '{section}'",
            )

        # Retrieve card data for each configured card
        section_cards = []
        for config in configs["cards"]:
            card_result = retrieveCard(
                reportId=reportId,
                year=year,
                months=months,
                title=config["title"],
                functionName=config["mainFunction"],
                comparisonFunc=config["comparisonFunction"],
                comparedTo=compared_to,
                visualId=config["visualId"],
            )

            section_cards.append(card_result.Data)

        return Result(
            Data=section_cards, Status=1, Message="Section cards retrieved successfully"
        )

    except Exception as ex:
        message = f"Error occurred in getSectionCards: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Data=None, Status=0, Message=message)
