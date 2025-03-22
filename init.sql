CREATE TABLE IF NOT EXISTS car_data (
    guid UUID PRIMARY KEY,
    price NUMERIC,
    make VARCHAR,
    model VARCHAR,
    mileage INTEGER,
    fuel_type VARCHAR,
    age DATE,
    transmission VARCHAR
);