PERCENTAGE_KEYWORDS = {"margin", "growth", "ratio"}


def getValueSymbol(title: str) -> dict:
    currency_symbol: str = "$"

    title_lower = title.lower()
    
    if any(keyword in title_lower for keyword in PERCENTAGE_KEYWORDS):
        return {"type": "percentage", "symbol": "%"}

    return {"type": "currency", "symbol": currency_symbol}
