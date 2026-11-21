import pandas as pd
import pytest

from src.transform import transform_weather_data


def sample_data():
    return pd.DataFrame([
        {
            "city": "Mumbai",
            "temperature": 50,
            "humidity": 66,
            "apparent_temperature": 28.1,
            "precipitation": 0.0,
            "weather_code": 0,
            "wind_speed": 6.1,
            "observed_at": "2026-11-21T21:15:00",
            "extracted_at": "2026-11-21T15:51:43+00:00"
        },
        {
            "city": "Delhi",
            "temperature": 19.4,
            "humidity": 75,
            "apparent_temperature": 20.6,
            "precipitation": 0.0,
            "weather_code": 1,
            "wind_speed": 2.8,
            "observed_at": "2026-11-21T21:15:00",
            "extracted_at": "2026-11-21T15:51:43+00:00"
        }
    ])


def test_valid_data():
    df = sample_data()

    result = transform_weather_data(df)

    assert len(result) == 2
    assert result["city"].tolist() == ["Mumbai", "Delhi"]


def test_empty_dataframe():
    with pytest.raises(ValueError):
        transform_weather_data(pd.DataFrame())


def test_duplicate_records():
    df = sample_data()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    result = transform_weather_data(df)

    assert len(result) == 2


def test_invalid_humidity():
    df = sample_data()
    df.loc[0, "humidity"] = 150

    result = transform_weather_data(df)

    assert len(result) == 1
    assert result.iloc[0]["city"] == "Delhi"


def test_missing_column():
    df = sample_data()
    df = df.drop(columns=["temperature"])

    with pytest.raises(ValueError):
        transform_weather_data(df)
