--Rank zones by revenue using window functions

WITH zone_revenue AS (
    SELECT
        pickup_location_id,
        SUM(total_amount) AS total_revenue,
        COUNT(*) AS trip_count,
    FROM fact_trips
    GROUP BY pickup_location_id
)

SELECT
    pickup_location_id,
    total_revenue,
    trip_count,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM zone_revenue
QUALIFY revenue_rank <= 10;