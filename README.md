# Automated Weather ETL Data Pipeline

An end-to-end automated Data Engineering project that extracts real-time weather data from the Open-Meteo API, transforms and validates it using Python and Pandas, and loads it into PostgreSQL. The pipeline includes automated scheduling, SQL analytics, data-quality reporting, visualization, and API retry handling.

## Project Overview

This project demonstrates the development of an automated ETL pipeline that collects current weather observations for four major Indian cities:

- Mumbai
- Delhi
- Bengaluru
- Pune

The pipeline processes weather measurements, validates data quality, prevents duplicate database records, and generates analytical reports and visualizations.

## Architecture

```mermaid
flowchart TD
    A[Open-Meteo Weather API] --> B[Extract - Python Requests]
    B --> C[Transform - Pandas]
    C --> D[Data Quality Validation]
    D --> E[Quality Report and Charts]
    D --> F[Load - SQLAlchemy]
    F --> G[(PostgreSQL Database)]
    G --> H[SQL Analytics]
    I[Windows Task Scheduler] --> B
    B --> J[Logging and Error Handling]
    F --> J
```

## Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| API Integration | Open-Meteo API, Requests |
| Data Processing | Pandas |
| Database | PostgreSQL |
| Database Connectivity | SQLAlchemy, psycopg2 |
| Data Visualization | Matplotlib |
| Data Analysis | SQL, Window Functions, Aggregations |
| Automation | Windows Task Scheduler |
| Testing | Pytest |
| Logging | Python Logging |
| Version Control | Git, GitHub |

## Key Features

### 1. Automated Data Extraction
- Fetches current weather observations from the Open-Meteo API.
- Collects temperature, humidity, apparent temperature, precipitation, weather code, and wind speed.
- Supports multiple cities through a centralized configuration.

### 2. Data Transformation
- Processes raw API responses using Pandas.
- Handles missing and invalid values.
- Validates measurement ranges.
- Removes duplicate observations.

### 3. PostgreSQL Data Storage
- Stores cleaned weather records in PostgreSQL.
- Uses SQLAlchemy for database connectivity.
- Implements a unique constraint on city and observation timestamp.
- Uses `ON CONFLICT DO NOTHING` for idempotent loading.

### 4. SQL Analytics
Includes analytical queries for:
- Latest weather conditions by city.
- Average, minimum, and maximum temperature.
- Daily weather trends.
- City temperature rankings using window functions.
- Record counts and observation history.
- Unusually high temperature detection.
- Overall database summaries.

### 5. Data Quality Monitoring
Automatically generates quality reports containing:
- Extracted, cleaned, and rejected record counts.
- Missing values and duplicate records.
- Invalid measurement counts.
- Overall data-quality status.

### 6. Data Visualization
Generates charts for:
- Data-quality checks.
- ETL record processing summary.
- Average temperature comparison across cities.

### 7. API Retry Handling
- Automatically retries temporary API failures.
- Handles HTTP errors such as 429, 500, 502, 503, and 504.
- Uses exponential backoff to reduce repeated requests during temporary failures.

### 8. Automated Scheduling
Uses Windows Task Scheduler to execute the complete ETL pipeline automatically at scheduled intervals.

### 9. Logging and Testing
- Maintains timestamped execution logs.
- Records extraction, transformation, and loading activities.
- Includes Pytest tests for transformation logic and data validation.

## Project Structure

```text
automated-etl-pipeline/
│
├── config/
│   ├── __init__.py
│   └── cities.py
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── database.py
│   ├── logger.py
│   └── data_quality.py
│
├── sql/
│   ├── schema.sql
│   └── analytics.sql
│
├── tests/
│   └── test_transform.py
│
├── reports/
│   └── Generated quality reports and charts
│
├── logs/
│   └── ETL execution logs
│
├── pipeline.py
├── run_pipeline.bat
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.12 or newer
- PostgreSQL 14 or newer
- Git
- Windows operating system

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/automated-etl-pipeline.git
cd automated-etl-pipeline
```

### 2. Create a virtual environment

```powershell
py -3.14 -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```sql
CREATE DATABASE weather_db;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/weather_db
```

Replace `YOUR_PASSWORD` with your PostgreSQL password. URL-encode special characters in the password when necessary.

Never commit your actual `.env` file to GitHub.

### 6. Run the ETL pipeline

```bash
python pipeline.py
```

### 7. Run the tests

```bash
python -m pytest -v
```

### 8. Execute SQL analytics

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d weather_db -f "sql/analytics.sql"
```

Adjust the PostgreSQL executable path if your installation uses another version or location.

### 9. Automate execution

Run the batch file manually:

```powershell
.\run_pipeline.bat
```

For automatic execution, configure `run_pipeline.bat` in Windows Task Scheduler.

## Generated Outputs

The pipeline creates timestamped reports and charts in the `reports/` directory.

Example:

```text
reports/
├── quality_report_YYYYMMDD_HHMMSS.txt
├── quality_checks_YYYYMMDD_HHMMSS.png
├── record_summary_YYYYMMDD_HHMMSS.png
└── city_temperature_YYYYMMDD_HHMMSS.png
```

Execution logs are stored in:

```text
logs/
└── etl_YYYYMMDD.log
```

## Future Enhancements

- Historical weather data ingestion.
- Interactive dashboards using Power BI or Streamlit.
- Cloud deployment using AWS S3, Glue, and Redshift.
- Email notifications for pipeline failures.
- Incremental data processing and advanced monitoring.
- More comprehensive automated data-quality tests.

## Learning Outcomes

Through this project, I gained practical experience in:

- Building end-to-end ETL pipelines.
- Integrating REST APIs with Python.
- Data cleaning and transformation using Pandas.
- Relational database design and PostgreSQL integration.
- SQL analytical queries and window functions.
- Data-quality validation and visualization.
- Error handling, retry mechanisms, and logging.
- Automating scheduled data workflows.

---

**Project:** Automated Weather ETL Data Pipeline  
**Domain:** Data Engineering  
**Language:** Python  
**Database:** PostgreSQL