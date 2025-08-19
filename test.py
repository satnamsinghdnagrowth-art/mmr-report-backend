import matplotlib.pyplot as plt

# Example inputs (replace with your actual function calls)
totalRev = 500000    # totalRevenue(year, months, reportId).Data
fixedCost = 200000   # totalOperatingExpenses(year, months, reportId).Data

if totalRev == 0 or fixedCost == 0:
    raise ValueError("Total Revenue or Fixed Cost is zero. Cannot build chart.")

# Contribution margin and variable cost percentage
contribution_margin = (totalRev - fixedCost) / totalRev
variable_cost_percent = 1 - contribution_margin

# Revenue range for X-axis
revenue = list(range(0, int(totalRev * 2) + 1, 20000))

# Total costs for each revenue point
total_costs = [fixedCost + (variable_cost_percent * r) for r in revenue]

# --- 1️⃣ Break-even point calculation ---
break_even_revenue = fixedCost / contribution_margin
break_even_cost = break_even_revenue  # at break-even, revenue = total cost

print(f"Break-even Revenue: {break_even_revenue:,.0f}")

# --- 2️⃣ Plot the chart ---
plt.figure(figsize=(10, 6))
plt.plot(revenue, total_costs, label="Total Costs", color='red')
plt.plot(revenue, revenue, label="Revenue Line", color='blue')
plt.axhline(y=fixedCost, color='gray', linestyle='--', label="Fixed Cost")

# Mark break-even point
plt.scatter(break_even_revenue, break_even_cost, color='green', s=100, zorder=5)
plt.annotate(f"Break-even\n({break_even_revenue:,.0f})",
             (break_even_revenue, break_even_cost),
             textcoords="offset points", xytext=(-40,10), fontsize=10,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# Labels and legend
plt.xlabel("Revenue")
plt.ylabel("Amount")
plt.title("Break-even Analysis")
plt.legend()
# Instead of plt.show()
plt.savefig("breakeven_chart.png", dpi=300)

plt.show()
