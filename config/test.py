from weasyprint import HTML

html = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Revenue Report</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 40px;
      }
      h1, h2 {
        color: #2c3e50;
      }
      p {
        line-height: 1.5;
        font-size: 14px;
      }
      .chart-section {
        margin-top: 40px;
      }
    </style>
  </head>
  <body>

    <h1>Monthly Revenue Report</h1>

    <h2>Executive Summary</h2>
    <p>
      This report outlines the monthly revenue performance from April 2024 to March 2025, comparing current figures with last year’s data. Key highlights include:
    </p>
    <ul>
      <li>Highest revenue recorded in January 2025 at <strong>$629.7K</strong>.</li>
      <li>Lowest revenue observed in June 2024 at <strong>$370.4K</strong>.</li>
      <li>Consistent growth seen in Q4 compared to the same period last year.</li>
    </ul>
    <p>
      The chart below visually represents the revenue trends for each month, enabling clear comparison and analysis.
    </p>

    <div class="chart-section">
      <h2>Revenue Chart (Apr 2024 - Mar 2025)</h2>

      <!-- SVG CHART (small size) -->
      <svg width="800" height="300" xmlns="http://www.w3.org/2000/svg" style="font-family: sans-serif; font-size: 10px;">
        <!-- Axes -->
        <line x1="40" y1="260" x2="780" y2="260" stroke="#ccc" />
        <!-- Y Axis labels -->
        <text x="5" y="260">$0</text>
        <text x="5" y="200">$400K</text>
        <text x="5" y="140">$800K</text>

        <!-- Bars (same as previous response) -->
        <!-- Apr 24 -->
        <rect x="50" y="120" width="20" height="140" fill="#4B87C5"/>
        <text x="50" y="115">$549.9K</text>
        <rect x="75" y="140" width="20" height="120" fill="#ccc"/>
        <text x="75" y="135">$501.4K</text>
        <text x="55" y="275">Apr</text>

        <!-- May 24 -->
        <rect x="110" y="115" width="20" height="145" fill="#4B87C5"/>
        <text x="110" y="110">$558.5K</text>
        <rect x="135" y="125" width="20" height="135" fill="#ccc"/>
        <text x="135" y="120">$492.1K</text>
        <text x="115" y="275">May</text>

        <!-- Jun 24 -->
        <rect x="170" y="190" width="20" height="70" fill="#4B87C5"/>
        <text x="170" y="185">$370.4K</text>
        <rect x="195" y="160" width="20" height="100" fill="#ccc"/>
        <text x="195" y="155">$428.0K</text>
        <text x="175" y="275">Jun</text>

        <!-- Jul 24 -->
        <rect x="230" y="150" width="20" height="110" fill="#4B87C5"/>
        <text x="230" y="145">$428.0K</text>
        <rect x="255" y="110" width="20" height="150" fill="#ccc"/>
        <text x="255" y="105">$548.0K</text>
        <text x="235" y="275">Jul</text>

        <!-- Aug 24 -->
        <rect x="290" y="60" width="20" height="200" fill="#4B87C5"/>
        <text x="290" y="55">$623.8K</text>
        <rect x="315" y="120" width="20" height="140" fill="#ccc"/>
        <text x="315" y="115">$470.8K</text>
        <text x="295" y="275">Aug</text>

        <!-- Sep 24 -->
        <rect x="350" y="130" width="20" height="130" fill="#4B87C5"/>
        <text x="350" y="125">$423.4K</text>
        <rect x="375" y="100" width="20" height="160" fill="#ccc"/>
        <text x="375" y="95">$507.4K</text>
        <text x="355" y="275">Sep</text>

        <!-- Oct 24 -->
        <rect x="410" y="90" width="20" height="170" fill="#4B87C5"/>
        <text x="410" y="85">$523.5K</text>
        <rect x="435" y="60" width="20" height="200" fill="#ccc"/>
        <text x="435" y="55">$573.0K</text>
        <text x="415" y="275">Oct</text>

        <!-- Nov 24 -->
        <rect x="470" y="150" width="20" height="110" fill="#4B87C5"/>
        <text x="470" y="145">$446.0K</text>
        <rect x="495" y="100" width="20" height="160" fill="#ccc"/>
        <text x="495" y="95">$502.1K</text>
        <text x="475" y="275">Nov</text>

        <!-- Dec 24 -->
        <rect x="530" y="160" width="20" height="100" fill="#4B87C5"/>
        <text x="530" y="155">$496.0K</text>
        <rect x="555" y="110" width="20" height="150" fill="#ccc"/>
        <text x="555" y="105">$496.0K</text>
        <text x="535" y="275">Dec</text>

        <!-- Jan 25 -->
        <rect x="590" y="50" width="20" height="210" fill="#4B87C5"/>
        <text x="590" y="45">$629.7K</text>
        <rect x="615" y="90" width="20" height="170" fill="#ccc"/>
        <text x="615" y="85">$541.7K</text>
        <text x="595" y="275">Jan</text>

        <!-- Feb 25 -->
        <rect x="650" y="120" width="20" height="140" fill="#4B87C5"/>
        <text x="650" y="115">$488.4K</text>
        <rect x="675" y="60" width="20" height="200" fill="#ccc"/>
        <text x="675" y="55">$597.4K</text>
        <text x="655" y="275">Feb</text>

        <!-- Mar 25 -->
        <rect x="710" y="140" width="20" height="120" fill="#4B87C5"/>
        <text x="710" y="135">$465.0K</text>
        <rect x="735" y="110" width="20" height="150" fill="#ccc"/>
        <text x="735" y="105">$532.0K</text>
        <text x="715" y="275">Mar</text>

        <!-- Legend -->
        <rect x="40" y="20" width="12" height="12" fill="#4B87C5"/>
        <text x="56" y="30">Revenue</text>
        <rect x="110" y="20" width="12" height="12" fill="#ccc"/>
        <text x="126" y="30">Last Year</text>
      </svg>
    </div>

  </body>
</html>
"""

HTML(string=html).write_pdf("svg_chart_output.pdf")
