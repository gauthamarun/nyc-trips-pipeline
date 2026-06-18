import duckdb
import pytest

@pytest.fixture
def con():
    return duckdb.connect("warehouse.duckdb")

def test_no_negative_fares(con):
    result = con.execute(
        "SELECT COUNT(*) FROM fact_trips WHERE fare_amount < 0"
    ).fetchone()[0]
    assert result == 0, f"Found {result} negative fares"

def test_row_count(con):
    result = con.execute("SELECT COUNT(*) FROM fact_trips").fetchone()[0]
    assert result > 100_000, "Suspiciously low row count"

def test_kpis_not_empty(con):
    result = con.execute("SELECT COUNT(*) FROM daily_kpis").fetchone()[0]
    assert result > 0

def test_no_null_pickup_datetime(con):
    result = con.execute(
        "SELECT COUNT(*) FROM fact_trips WHERE pickup_datetime IS NULL"
    ).fetchone()[0]
    assert result == 0