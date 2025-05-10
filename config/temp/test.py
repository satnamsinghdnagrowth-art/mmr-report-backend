import plotly.graph_objects as go

# Values for each category (could be dynamically fetched from a database)
values = [
    5,   # Revenue
    -5,  # Cost of Goods Sold
    10,  # Other Income
    2,   # Other Income 2
    -3,  # Cash Tax Paid
    6,   # Change in A/P
    -9,  # Change in A/R
    0,   # Change in Inventory
    0,   # Change in WIP
    -7,  # Other Assets
    0,   # OPERATING CASH FLOW
    8,   # Change in Fixed Assets
    7,   # Intangibles
    0,   # Other Non-Current Assets
    8 + 7 + 0,  # TOTAL INVESTING ACTIVITIES (sum of Fixed Assets, Intangibles, Other Non-Current Assets)
    0,   # FREE CASH FLOW
    -7,  # Net Interest
    0,   # Other Liabilities
    0,   # Dividends
    -4   # Retained Earnings
]

# Labels corresponding to each category
labels = [
    "Revenue", "Cost of Goods Sold", "Other Income", "Other Income 2", "Cash Tax Paid",
    "Change in A/P", "Change in A/R", "Change in Inventory", "Change in WIP", "Other Assets",
    "OPERATING CASH FLOW",
    "Change in Fixed Assets", "Intangibles", "Other Non-Current Assets",
    "TOTAL INVESTING ACTIVITIES",
    "FREE CASH FLOW",
    "Net Interest", "Other Liabilities", "Dividends", "Retained Earnings"
]

# Measures corresponding to each category (relative for everything except totals)
measures = [
    "relative", "relative", "relative", "relative", "relative",
    "relative", "relative", "relative", "relative", "relative",
    "total",  # OPERATING CASH FLOW
    "relative", "relative", "relative",  # Change in Fixed Assets, Intangibles, and Other Non-Current Assets
    "total",  # TOTAL INVESTING ACTIVITIES (sum of previous three)
    "total",  # FREE CASH FLOW
    "relative", "relative", "relative", "relative"
]

# Format the values for text display on the chart
formatted_values = [f"${v:,.0f}" if v >= 0 else f"(${abs(v):,.0f})" for v in values]

# Create the Waterfall chart
fig = go.Figure(go.Waterfall(
    orientation="v",
    measure=measures,
    x=labels,
    y=values,
    text=formatted_values,
    textposition="outside",
    connector={"line": {"color": "gray"}},
    increasing={"marker": {"color": "#98D185"}},
    decreasing={"marker": {"color": "#DB3E39"}},
    totals={"marker": {"color": "gray"}}
))

# Update layout for the chart
fig.update_layout(
    title="Cash Flow Waterfall Chart",
    showlegend=False,
    height=700,
    margin=dict(l=50, r=50, t=100, b=50),
    xaxis_title="Components",
    yaxis_title="Amount"
)

# Show the chart
fig.show()
