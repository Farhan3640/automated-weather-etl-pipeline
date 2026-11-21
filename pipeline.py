
from src.extract import extract_weather_data
from src.transform import transform_weather_data
from src.load import load_weather_data
from src.data_quality import generate_data_quality_report
from src.logger import logger


def run_pipeline():
    try:
        logger.info("=" * 50)
        logger.info("WEATHER ETL PIPELINE STARTED")
        logger.info("=" * 50)

        # Step 1: Extract
        raw_data = extract_weather_data()

        # Step 2: Transform
        clean_data = transform_weather_data(raw_data)

        if clean_data.empty:
            raise ValueError("No valid records available for loading.")

        # Step 3: Data Quality Report
        generate_data_quality_report(raw_data, clean_data)

        # Step 4: Load
        load_weather_data(clean_data)

        logger.info("WEATHER ETL PIPELINE COMPLETED SUCCESSFULLY")

    except Exception:
        logger.exception("WEATHER ETL PIPELINE FAILED")
        raise


if __name__ == "__main__":
    run_pipeline()
