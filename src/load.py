from pathlib import Path
from sqlalchemy import text
from src.database import engine
from src.logger import logger


def load_weather_data(df):

    if df.empty:
        raise ValueError("Cannot load an empty DataFrame.")

    schema_path = Path("sql/schema.sql")
    schema = schema_path.read_text(encoding="utf-8")

    with engine.begin() as connection:

        # Create the table if it does not exist
        connection.execute(text(schema))

        records = df.to_dict(orient="records")

        insert_query = text("""
            INSERT INTO weather_data (
                city, temperature, humidity,
                apparent_temperature, precipitation,
                weather_code, wind_speed,
                observed_at, extracted_at
            )
            VALUES (
                :city, :temperature, :humidity,
                :apparent_temperature, :precipitation,
                :weather_code, :wind_speed,
                :observed_at, :extracted_at
            )
            ON CONFLICT (city, observed_at)
            DO NOTHING
        """)

        result = connection.execute(insert_query, records)
        logger.info("Starting data loading")
        logger.info("Data loading completed successfully")
        logger.info(f"New records inserted: {result.rowcount}")
        logger.info(f"Records processed: {len(records)}")


if __name__ == "__main__":

    from src.extract import extract_weather_data
    from src.transform import transform_weather_data

    raw_data = extract_weather_data()
    clean_data = transform_weather_data(raw_data)

    load_weather_data(clean_data)
