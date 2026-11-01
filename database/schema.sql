-- Таблица стран с координатами границ (bounding box)
CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    min_lat FLOAT NOT NULL,
    max_lat FLOAT NOT NULL,
    min_lon FLOAT NOT NULL,
    max_lon FLOAT NOT NULL
);

-- Таблица самолетов
CREATE TABLE IF NOT EXISTS airplanes (
    id SERIAL PRIMARY KEY,
    icao24 VARCHAR(10) NOT NULL,
    callsign VARCHAR(20),
    origin_country VARCHAR(100),
    longitude FLOAT,
    latitude FLOAT,
    velocity FLOAT,
    country_id INT REFERENCES countries(id) ON DELETE SET NULL,
    last_contact BIGINT,
    UNIQUE(icao24, country_id)
);