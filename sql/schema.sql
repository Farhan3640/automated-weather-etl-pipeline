
CREATE TABLE IF NOT EXISTS weather_data (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature NUMERIC(5,2),
    humidity SMALLINT,
    apparent_temperature NUMERIC(5,2),
    precipitation NUMERIC(8,2),
    weather_code SMALLINT,
    wind_speed NUMERIC(7,2),
    observed_at TIMESTAMPTZ NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_city_observation
    UNIQUE (city, observed_at)
);
