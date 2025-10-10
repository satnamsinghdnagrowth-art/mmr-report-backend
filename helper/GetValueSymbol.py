from core.models.base.VisualUnitModel import UnitModel

PERCENTAGE_KEYWORDS = {"margin", "growth", "ratio","%"}


def getValueSymbol(title: str) -> dict:

    title_lower = title.lower()

    if any(keyword in title_lower for keyword in PERCENTAGE_KEYWORDS):
        return UnitModel(type="percentage",symbol="%").dict()

    return UnitModel(type="currency",symbol="$").dict()
