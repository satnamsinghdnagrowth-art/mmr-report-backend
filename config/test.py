import requests

# Example: replace with actual financial input
financial_input = """
Current Month:
Revenue: $64,930
Gross Margin: 76.98%
Operational Cost: $21,424
EBIT Margin: 43.99%

Last Month:
Revenue: $50,086
Gross Margin: 55.96%
Operational Cost: $23,429
EBIT Margin: 9.19%

Notes:
- Product Sales Income increased
- COGS for coffee and baked goods decreased
- Advertisement & Marketing, Supplies & Materials, and Legal & Professional Fees decreased
"""

# Request to LM Studio (change the model name as needed)
response = requests.post(
    "http://localhost:1234/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json={
        "model": "your-model-name",  # e.g., "mistral-7b-instruct"
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a financial analyst generating professional executive summaries. "
                    "Format the output with an 'Executive Summary' title, then use bullet points. "
                    "Include monthly figures, percent change, dollar change, and short insights in business language."
                )
            },
            {
                "role": "user",
                "content": f"Generate an executive summary from the following financial report:\n\n{financial_input}"
            }
        ],
        "temperature": 0.3
    }
)

summary = response.json()["choices"][0]["message"]["content"]
print(summary)
