
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.logger import logger


def generate_charts(
    raw_df,
    clean_df,
    report_dir,
    timestamp,
    quality_metrics
):
    """
    Generate visualizations for the data quality report.
    """

    # Chart 1: Data Quality Checks
    metrics = list(quality_metrics.keys())
    values = list(quality_metrics.values())

    plt.figure(figsize=(10, 5))

    bars = plt.bar(metrics, values)

    plt.title("Weather ETL - Data Quality Checks")
    plt.xlabel("Quality Metrics")
    plt.ylabel("Number of Issues")
    plt.xticks(rotation=20, ha="right")

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    chart1 = report_dir / f"quality_checks_{timestamp}.png"
    plt.savefig(chart1, dpi=150)
    plt.close()

    # Chart 2: Record Summary
    record_labels = ["Extracted", "Cleaned", "Rejected"]

    record_values = [
        len(raw_df),
        len(clean_df),
        len(raw_df) - len(clean_df)
    ]

    plt.figure(figsize=(8, 5))

    bars = plt.bar(record_labels, record_values)

    plt.title("ETL Pipeline - Record Summary")
    plt.xlabel("Processing Stage")
    plt.ylabel("Number of Records")

    for bar, value in zip(bars, record_values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    chart2 = report_dir / f"record_summary_{timestamp}.png"
    plt.savefig(chart2, dpi=150)
    plt.close()

    # Chart 3: Average Temperature by City
    if not clean_df.empty and {"city", "temperature"}.issubset(clean_df.columns):

        city_temperature = (
            clean_df.groupby("city")["temperature"]
            .mean()
            .sort_values(ascending=False)
        )

        plt.figure(figsize=(8, 5))

        bars = plt.bar(
            city_temperature.index,
            city_temperature.values
        )

        plt.title("Average Temperature by City")
        plt.xlabel("City")
        plt.ylabel("Temperature (°C)")

        for bar, value in zip(bars, city_temperature.values):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.2f}°C",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()

        chart3 = report_dir / f"city_temperature_{timestamp}.png"
        plt.savefig(chart3, dpi=150)
        plt.close()

        return [chart1, chart2, chart3]

    return [chart1, chart2]


def generate_data_quality_report(raw_df, clean_df):

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    required_columns = [
        "city",
        "temperature",
        "humidity",
        "apparent_temperature",
        "precipitation",
        "weather_code",
        "wind_speed",
        "observed_at",
        "extracted_at"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in raw_df.columns
    ]

    missing_values = int(raw_df.isna().sum().sum())

    if {"city", "observed_at"}.issubset(raw_df.columns):
        duplicate_count = int(
            raw_df.duplicated(
                subset=["city", "observed_at"]
            ).sum()
        )
    else:
        duplicate_count = 0

    def numeric_column(name):
        if name not in raw_df.columns:
            return pd.Series(
                float("nan"),
                index=raw_df.index
            )

        return pd.to_numeric(
            raw_df[name],
            errors="coerce"
        )

    humidity = numeric_column("humidity")
    precipitation = numeric_column("precipitation")
    wind_speed = numeric_column("wind_speed")
    weather_code = numeric_column("weather_code")

    invalid_humidity = int(
        (humidity.notna() & ~humidity.between(0, 100)).sum()
    )

    invalid_precipitation = int(
        (precipitation.notna() & (precipitation < 0)).sum()
    )

    invalid_wind_speed = int(
        (wind_speed.notna() & (wind_speed < 0)).sum()
    )

    invalid_weather_code = int(
        (
            weather_code.notna()
            & (
                (weather_code < 0)
                | (weather_code > 99)
                | (weather_code % 1 != 0)
            )
        ).sum()
    )

    rejected_records = len(raw_df) - len(clean_df)

    clean_missing_values = int(
        clean_df.isna().sum().sum()
    )

    invalid_measurements = (
        invalid_humidity
        + invalid_precipitation
        + invalid_wind_speed
        + invalid_weather_code
    )

    quality_passed = (
        not missing_columns
        and clean_missing_values == 0
        and invalid_measurements == 0
    )

    status = "PASSED" if quality_passed else "WARNING"

    # Metrics for visualization
    quality_metrics = {
        "Missing Values": missing_values,
        "Duplicates": duplicate_count,
        "Invalid Humidity": invalid_humidity,
        "Invalid Precipitation": invalid_precipitation,
        "Invalid Wind": invalid_wind_speed,
        "Invalid Weather Codes": invalid_weather_code
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate charts
    chart_paths = generate_charts(
        raw_df,
        clean_df,
        report_dir,
        timestamp,
        quality_metrics
    )

    chart_names = "\n".join(
        str(path) for path in chart_paths
    )

    report = f"""
========================================
       WEATHER DATA QUALITY REPORT
========================================

Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

RECORD SUMMARY
--------------
Records Extracted       : {len(raw_df)}
Records After Cleaning  : {len(clean_df)}
Records Rejected        : {rejected_records}

DATA QUALITY CHECKS
-------------------
Missing Values          : {missing_values}
Duplicate Records       : {duplicate_count}
Invalid Humidity        : {invalid_humidity}
Invalid Precipitation   : {invalid_precipitation}
Invalid Wind Speed      : {invalid_wind_speed}
Invalid Weather Codes   : {invalid_weather_code}

Missing Required Columns: {missing_columns or 'None'}
Missing Values After Cleaning: {clean_missing_values}

GENERATED VISUALIZATIONS
------------------------
{chart_names}

========================================
OVERALL DATA QUALITY STATUS: {status}
========================================
"""

    report_path = (
        report_dir / f"quality_report_{timestamp}.txt"
    )

    report_path.write_text(
        report,
        encoding="utf-8"
    )

    logger.info(
        f"Data quality report generated: {report_path}"
    )

    logger.info(
        f"Generated {len(chart_paths)} visualization charts"
    )

    logger.info(
        f"Data quality status: {status}"
    )

    print(report)

    return report_path


if __name__ == "__main__":
    from src.extract import extract_weather_data
    from src.transform import transform_weather_data

    raw_data = extract_weather_data()
    clean_data = transform_weather_data(raw_data)

    generate_data_quality_report(
        raw_data,
        clean_data
    )
