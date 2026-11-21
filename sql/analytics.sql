
-- 1. Latest weather conditions for each city

SELECT DISTINCT ON (city)
    city,
    temperature,
    humidity,
    apparent_temperature,
    precipitation,
    wind_speed,
    observed_at
FROM weather_data
ORDER BY city, observed_at DESC;


-- 2. Average temperature by city

SELECT
    city,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(MIN(temperature), 2) AS min_temperature,
    ROUND(MAX(temperature), 2) AS max_temperature
FROM weather_data
GROUP BY city
ORDER BY avg_temperature DESC;


-- 3. Daily weather trends by city

SELECT
    city,
    DATE(observed_at) AS observation_date,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(MAX(temperature), 2) AS max_temperature,
    ROUND(MIN(temperature), 2) AS min_temperature
FROM weather_data
GROUP BY city, DATE(observed_at)
ORDER BY observation_date DESC, city;


-- 4. Rank cities by average temperature

SELECT
    city,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    RANK() OVER (
        ORDER BY AVG(temperature) DESC
    ) AS temperature_rank
FROM weather_data
GROUP BY city;


-- 5. Count records collected for each city

SELECT
    city,
    COUNT(*) AS total_records,
    MIN(observed_at) AS first_observation,
    MAX(observed_at) AS latest_observation
FROM weather_data
GROUP BY city
ORDER BY total_records DESC;


-- 6. Identify unusually high temperatures

SELECT
    city,
    temperature,
    observed_at
FROM weather_data
WHERE temperature > 35
ORDER BY temperature DESC;


-- 7. Overall pipeline data summary

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT city) AS total_cities,
    ROUND(AVG(temperature), 2) AS overall_avg_temperature,
    ROUND(AVG(humidity), 2) AS overall_avg_humidity,
    MAX(extracted_at) AS last_extraction_time
FROM weather_data;
