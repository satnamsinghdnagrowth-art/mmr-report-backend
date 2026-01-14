# MMR Report Generation Backend

## Overview
This is the backend repository for the MMR Report Generation project. It provides a comprehensive API for:
- Ingesting financial data from Excel files.
- Performing complex financial calculations (Revenue, Expenses, Ratios, etc.).
- Managing and processing Custom KPIs.
- Generating detailed PDF reports with charts and tables.

## Tech Stack
- **Language:** Python 3.x
- **Framework:** FastAPI
- **Data Processing:** Pandas, NumPy
- **Report Generation:** WeasyPrint
- **Server:** Uvicorn

## Installation & Setup

1.  **Clone the repository** (if not already done).
2.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To start the backed server, run:

```bash
python main.py
```

The server will start at `http://0.0.0.0:8081`.

## Project Structure

```
backend/
├── config/                 # Configuration files (paths, variable mappings)
├── core/                   # Core models and base classes
├── database/               # JSON storage for reports and source metadata
├── helper/                 # Utility functions (Excel reading, JSON loading)
├── routes/                 # API Routes definitions
├── services/               # Business Logic
│   ├── calculations/       # Financial calculation modules
│   ├── customKPIs/         # Custom KPI processing and management
│   ├── reportSection/      # Logic for specific report sections
│   ├── reports/            # Report generation orchestration
│   └── visuals/            # Chart and table generation utilities
├── main.py                 # Entry point
├── RESTClient.py           # FastAPI app initialization
└── requirements.txt        # Project dependencies
```

## Key Features

### 1. Financial Calculations
Located in `services/calculations/`, this module handles all core financial metrics including:
- **Revenue & Growth:** Month-over-Month and Quarter-over-Quarter calculations.
- **Profitability:** Gross Profit, Net Income, EBITDA.
- **Ratios:** Liquidity ratios, Working Capital, etc.
- **Expenses:** Deep dive into various expense categories.

See `calculation.md` for a detailed breakdown of all logic and formulas.

### 2. Custom KPIs
The system supports user-defined KPIs via Excel uploads.
- **Ingestion:** Parses custom Excel files using `services/customKPIs/FormatData.py`.
- **Management:** Adds custom items to reports via `CreateCustomKPIsList.py`.
- **Visualization:** Generates custom charts and tables (`CustomChartCreation.py`, `CustomTableCreation.py`).

### 3. Report Generation
Generates PDF reports by consolidating data from:
- **Financial Data:** Processed from raw Excel inputs.
- **Custom KPIs:** Integrated dynamically.
- **Sections:** Modulas sections (Executive Summary, P&L, Balance Sheet) managed in `services/reportSection/`.

## API Endpoints
The application exposes RESTful endpoints for:
- File Uploads (Financial Data, Custom KPIs).
- Report Management (Create, List, Update).
- Data Retrieval (Specific financial metrics, Progress stats).
- PDF Export.

*(Refer to `RESTClient.py` and `routes/` for specific endpoint definitions.)*
