
import duckdb

con = duckdb.connect("warehouse.duckdb")

for sql_file in ["transform/daily_kpis.sql", "transform/top_pickup_zones.sql"]:
    with open(sql_file) as f:
        query = f.read()
    result = con.execute(query).df()
    table_name = sql_file.split("/")[-1].replace(".sql", "")
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS {query}")
    print(f"✅ {table_name} built — {len(result)} rows")