import pandas as pd
from src.logger import logger

REQUIRED_COLUMNS = [
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

NUMERIC_COLUMNS = [
    "temperature",
    "humidity",
    "apparent_temperature",
    "precipitation",
    "weather_code",
    "wind_speed"
]


def transform_weather_data(df):

    logger.info("Starting data transformation")

    # 1. Check for empty input
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    # 2. Work on a copy
    df = df.copy()

    # 3. Validate required columns
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # 4. Clean city names
    df["city"] = df["city"].astype("string").str.strip()

    # 5. Convert numeric columns
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    # 6. Convert timestamps
    # API timestamps represent local Indian time.
    df["observed_at"] = pd.to_datetime(
        df["observed_at"], errors="coerce"
    ).dt.tz_localize("Asia/Kolkata")

    df["extracted_at"] = pd.to_datetime(
        df["extracted_at"], errors="coerce", utc=True
    )

    # 7. Remove records with missing essential values
    initial_count = len(df)

    df = df.dropna(subset=REQUIRED_COLUMNS)

    logger.info(f"Invalid or missing records removed: {initial_count - len(df)}")
    # 8. Validate measurement ranges
    valid_records = (
        df["temperature"].between(-90, 60)
        & df["apparent_temperature"].between(-100, 70)
        & df["humidity"].between(0, 100)
        & df["precipitation"].ge(0)
        & df["weather_code"].between(0, 99)
        & df["weather_code"].mod(1).eq(0)
        & df["wind_speed"].ge(0)
        & df["city"].ne("")
    )

    invalid_count = (~valid_records).sum()

    df = df.loc[valid_records].copy()

    logger.info(f"Invalid measurement records removed: {invalid_count}")

    # 9. Remove duplicate observations
    before_deduplication = len(df)

    df = df.drop_duplicates(
        subset=["city", "observed_at"],
        keep="last"
    )

    logger.info(f"Duplicate records removed: {before_deduplication - len(df)}")

    # 10. Reset index
    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid records remain after transformation.")

    logger.info(f"Transformation completed. Final records: {len(df)}")

    print("\nCleaned DataFrame:")
    print(df)

    return df
