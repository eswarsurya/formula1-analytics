# Formula 1 Race Analytics - Data Pipeline & Visualization

A complete ETL and analytics pipeline for Formula 1 race data using the **FastF1 API**, demonstrating **API integration**, **data pipeline design**, **ETL processes**, and **business intelligence** capabilities.

## What This Project Demonstrates

| Skill | Evidence |
|-------|----------|
| **API Integration** | FastF1 REST API for real-time race data extraction |
| **ETL Pipeline** | Extract → Transform → Load workflow with data cleaning |
| **Data Engineering** | Automated data extraction, schema handling, caching |
| **Python & Pandas** | Data manipulation, feature engineering, aggregation |
| **Data Visualization** | Matplotlib/Seaborn charts for race performance analysis |
| **Cloud Concepts** | Designed for Azure Data Factory integration (WIP) |
| **Continuous Learning** | Independently mastered FastF1 library in 2 weeks |

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  FastF1 API │────▶│   ETL Pipe  │────▶│  Analytics  │
│  (Extract)  │     │(Transform)  │     │ (Visualize) │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
  data/raw/           data/processed/      notebooks/
  - results_r1.csv    - results_r1_clean.csv - charts
  - laps_r1.csv       - laps_r1_clean.csv    - reports
  - schedule.csv
```

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/formula1-analytics.git
cd formula1-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run ETL Pipeline

```bash
# Extract and process first 3 races of 2024 season
python scripts/f1_data_pipeline.py
```

### Run Analysis

```bash
# Generate charts and reports
python scripts/f1_analysis.py
```

## Sample Output

### Data Pipeline
```
============================================================
F1 DATA PIPELINE - 2024 Season
============================================================
Extracting 2024 race schedule...
  ✓ Saved 24 races
Extracting Round 1: Bahrain Grand Prix...
  ✓ Saved 20 driver results
  ✓ Saved 1200 lap records
Extracting Round 2: Saudi Arabian Grand Prix...
  ✓ Saved 20 driver results
  ✓ Saved 1100 lap records
...

📊 DATA QUALITY SUMMARY
----------------------------------------
Raw data files: 6
Processed files: 6
Total raw records: 4600
Total processed records: 4580
Data retention rate: 99.6%
```

### Analysis Charts
- `qualifying_vs_race.png` - Grid position vs finish position scatter plot
- `positions_gained.png` - Best overtakers bar chart

## Key Features

### ETL Pipeline (`f1_data_pipeline.py`)
- ✅ **API Integration**: FastF1 library wraps Ergast F1 API
- ✅ **Data Extraction**: Race results, lap times, sector times
- ✅ **Data Transformation**: Cleaning, type conversion, feature engineering
- ✅ **Data Loading**: Structured CSV output for analysis
- ✅ **Error Handling**: Graceful handling of missing/late data
- ✅ **Caching**: FastF1 cache for faster subsequent loads

### Analytics (`f1_analysis.py`)
- ✅ **Driver Standings**: Championship points aggregation
- ✅ **Team Performance**: Constructor comparison
- ✅ **Qualifying vs Race**: Start vs finish position analysis
- ✅ **Positions Gained**: Overtaking performance metrics

## Cloud Integration Roadmap

### Phase 1: Azure Data Factory (Current WIP)
- [ ] Azure Data Factory pipeline for scheduled API extraction
- [ ] Azure Blob Storage for raw data lake
- [ ] Azure SQL Database for structured data warehouse
- [ ] Power BI connector for live dashboards

### Phase 2: Real-time Streaming
- [ ] Azure Event Hubs for live timing data
- [ ] Azure Stream Analytics for real-time metrics
- [ ] Power BI real-time dashboard

## Project Structure
```
formula1-analytics/
├── data/
│   ├── raw/              # Extracted API data
│   ├── processed/        # Cleaned analysis-ready data
│   └── cache/            # FastF1 cache
├── scripts/
│   ├── f1_data_pipeline.py   # ETL pipeline
│   └── f1_analysis.py        # Analytics & visualization
├── notebooks/
│   ├── qualifying_vs_race.png
│   └── positions_gained.png
├── requirements.txt
└── README.md
```

## Data Sources

- **FastF1 API**: Python wrapper for Ergast Formula 1 API (http://ergast.com/mrd/)
- **Coverage**: Race results, lap times, sector times, qualifying, practice
- **Historical Data**: 1950-present (limited by Ergast API availability)

## Author

**Eswar Surya Danaboina**  
MSc Data Analytics | Dublin Business School  
[Portfolio](https://eswarsurya.github.io/eswar-portfolio/) | [LinkedIn](https://linkedin.com/in/eswarsurya76)

## License

MIT License - Academic project for demonstration purposes.
