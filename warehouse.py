import duckdb
import pandas as pd

con = duckdb.connect("warehouse.db")

con.execute("""
CREATE TABLE IF NOT EXISTS raw_trips AS
SELECT * FROM read_parquet('data/raw/*.parquet')
""")

con.execute("""
CREATE TABLE IF NOT EXISTS dim_location AS
SELECT DISTINCT 
    PULocationID as location_id,
    'Unknown' as borough,
    'Unknown' as zone
    FROM raw_trips
""")

con.execute("""
CREATE TABLE IF NOT EXISTS fact_trips AS
SELECT
    ROW_NUMBER() OVER () AS trip_id,
    tpep_pickup_datetime AS pickup_datetime,
    tpep_dropoff_datetime AS dropoff_datetime,
    passenger_count,
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount,
    VendorID as vendor_id,
    PULocationID as pickup_location_id,
    DOLocationID as dropoff_location_id,
FROM raw_trips
WHERE fare_amount > 0
AND trip_distance > 0
AND passenger_count>0
""")

print("Warehouse loaded.")