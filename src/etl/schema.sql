-- schema.sql : create tables for google traffic, weather, and etl_runs

CREATE TABLE IF NOT EXISTS etl_runs (
    id SERIAL PRIMARY KEY,
    run_timestamp TIMESTAMPTZ DEFAULT NOW(),
    source TEXT,
    city TEXT,
    total_routes INT,
    congestion_percentage NUMERIC,
    average_delay_minutes NUMERIC
);

CREATE TABLE IF NOT EXISTS google_traffic_data (
    id SERIAL PRIMARY KEY,
    run_id INT REFERENCES etl_runs(id) ON DELETE CASCADE,
    city TEXT,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    route_name TEXT,
    timestamp TIMESTAMPTZ,
    congestion_percentage NUMERIC,
    average_delay_minutes NUMERIC,
    traffic_level TEXT,
    red_percentage NUMERIC,
    yellow_percentage NUMERIC,
    green_percentage NUMERIC,
    screenshot_path TEXT,
    extraction_method TEXT,
    extraction_timestamp TIMESTAMPTZ
);


CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    run_id INT REFERENCES etl_runs(id) ON DELETE CASCADE,
    city TEXT,
    region TEXT,
    country TEXT,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    timestamp TIMESTAMPTZ,
    temp_c NUMERIC,
    condition TEXT,
    wind_kph NUMERIC,
    humidity NUMERIC,
    cloud NUMERIC,
    pressure_mb NUMERIC,
    feelslike_c NUMERIC,
    precip_mm NUMERIC,
    uv NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_weather_city_time ON weather_data(city, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_google_city_time ON google_traffic_data(city, timestamp DESC);