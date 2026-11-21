
import requests
import pandas as pd

from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.cities import CITIES
from src.logger import logger


API_URL = "https://api.open-meteo.com/v1/forecast"


def create_session():

    retry_strategy = Retry(
        total=4,
        connect=4,
        read=4,
        status=4,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


def fetch_city_weather(city, coordinates):

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m"
        ],
        "timezone": "Asia/Kolkata"
    }

    session = create_session()

    try:
        logger.info(f"Fetching weather data for {city}")

        response = session.get(
            API_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        current = data["current"]

        return {
            "city": city,
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "apparent_temperature": current["apparent_temperature"],
            "precipitation": current["precipitation"],
            "weather_code": current["weather_code"],
            "wind_speed": current["wind_speed_10m"],
            "observed_at": current["time"],
            "extracted_at": datetime.now(timezone.utc)
        }

    except (
        requests.RequestException,
        KeyError,
        ValueError
    ):
        logger.exception(
            f"Failed to fetch weather data for {city} after retries"
        )

        return None

    finally:
        session.close()


def extract_weather_data():

    records = []

    for city, coordinates in CITIES.items():

        weather = fetch_city_weather(
            city,
            coordinates
        )

        if weather:
            records.append(weather)

    if not records:
        logger.error("No weather data could be extracted")

        raise RuntimeError(
            "Weather extraction failed for all cities."
        )

    df = pd.DataFrame(records)

    logger.info("Extraction completed successfully")
    logger.info(f"Extracted {len(df)} records")

    return df


if __name__ == "__main__":

    weather_df = extract_weather_data()

    logger.info(
        f"Total records extracted: {len(weather_df)}"
    )
