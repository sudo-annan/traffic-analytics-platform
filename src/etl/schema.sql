-- -- Track ETL runs
-- CREATE TABLE IF NOT EXISTS etl_runs (
--     id SERIAL PRIMARY KEY,
--     run_timestamp TIMESTAMPTZ DEFAULT NOW(),
--     total_disruptions INT,
--     total_status INT
-- );

-- -- Traffic disruptions (roadworks, closures)
-- CREATE TABLE IF NOT EXISTS traffic_disruptions (
--     id TEXT PRIMARY KEY,
--     run_id INT REFERENCES etl_runs(id) ON DELETE CASCADE,
--     category TEXT,
--     sub_category TEXT,
--     severity TEXT,
--     current_update TEXT,
--     comments TEXT,
--     status TEXT,
--     level_of_interest TEXT,
--     start_time TIMESTAMPTZ,
--     end_time TIMESTAMPTZ,
--     location TEXT,
--     lat DOUBLE PRECISION,
--     lon DOUBLE PRECISION,
--     has_closures BOOLEAN,
--     road_ids TEXT[],
--     corridor_ids TEXT[],
--     source TEXT,
--     inserted_at TIMESTAMPTZ DEFAULT NOW()
-- );

-- -- High-level road status
-- CREATE TABLE IF NOT EXISTS traffic_status (
--     id TEXT PRIMARY KEY,
--     run_id INT REFERENCES etl_runs(id) ON DELETE CASCADE,
--     display_name TEXT,
--     status_severity TEXT,
--     status_description TEXT,
--     bounds TEXT,
--     envelope TEXT,
--     source TEXT,
--     inserted_at TIMESTAMPTZ DEFAULT NOW()
-- );

ALTER TABLE etl_runs
ADD COLUMN IF NOT EXISTS congestion_percentage NUMERIC,
ADD COLUMN IF NOT EXISTS average_delay_minutes NUMERIC,
ADD COLUMN IF NOT EXISTS journey_time_with_traffic NUMERIC,
ADD COLUMN IF NOT EXISTS journey_time_without_traffic NUMERIC,
ADD COLUMN IF NOT EXISTS incidents_detected INT,
ADD COLUMN IF NOT EXISTS traffic_speed_kmh NUMERIC;
