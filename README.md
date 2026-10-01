# Formula 1 Race Analytics — Data Pipeline & Visualization

An analytics and data-engineering project built around **FastF1**, demonstrating API integration, ETL design, data quality handling, feature engineering, and business-intelligence workflows.

## What this project demonstrates

| Capability | Evidence |
| --- | --- |
| **API integration** | FastF1-based extraction of Formula 1 race data |
| **ETL** | Extract → transform → load workflow with reusable scripts |
| **Data engineering** | Schema handling, caching, cleaning, structured outputs |
| **Python** | Pandas, feature engineering, analysis automation |
| **Analytics** | Driver standings, team performance, qualifying vs race, positions gained |
| **BI direction** | Structured outputs prepared for Power BI |
| **Cloud roadmap** | Planned Azure Data Factory, Blob Storage, Azure SQL integration |

## Architecture

~~~text
FastF1 API
    ↓
Extract
    ↓
Transform / Clean
    ↓
Processed CSVs
    ↓
Analytics + Visualisation
    ↓
Power BI / Reporting
~~~

## Quick start

Clone the repository:

~~~bash
git clone https://github.com/eswarsurya/formula1-analytics.git
cd formula1-analytics

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
~~~

Run the ETL workflow:

~~~bash
python scripts/f1_data_pipeline.py
~~~

Run the analysis:

~~~bash
python scripts/f1_analysis.py
~~~

## Current workflow

The pipeline covers:

- Race schedule and result extraction
- Driver and constructor performance data
- Lap and sector information
- Cleaning and type conversion
- Feature engineering
- CSV-based analytical outputs
- Cached API data for repeatable local runs
- Basic data-quality checks
- Visual analysis of qualifying, race finish, and positions gained

## Project structure

~~~
formula1-analytics/
├── data/
│   ├── raw/
│   ├── processed/
│   └── cache/
├── scripts/
│   ├── f1_data_pipeline.py
│   └── f1_analysis.py
├── notebooks/
├── requirements.txt
└── README.md
~~~

## Cloud integration roadmap

The next engineering layer is planned around:

**Phase 1:** Azure Data Factory → Azure Blob Storage → Azure SQL → Power BI

**Phase 2:** Event streaming → real-time processing → live dashboarding

These are roadmap items rather than claimed production deployments.

## Author

**Eswar Surya Danaboina**  
MSc Data Analytics · Dublin, Ireland

Portfolio: https://eswardanaboina.vercel.app/  
LinkedIn: https://www.linkedin.com/in/eswarsurya76/  
GitHub: https://github.com/eswarsurya

## License

MIT
