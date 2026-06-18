--Daily Revenue with 7-day rolling average 

SELECT
    DATE_TRUNC('day', pickup_datetime) AS trip_date,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount),2) AS daily_revenue,
    ROUND(AVG(trip_distance),2) AS avg_distance,
    ROUND(
        AVG(SUM(total_amount)) OVER (
            ORDER BY DATE_TRUNC('day', pickup_datetime)
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS revenue_7_day_rolling_avg
FROM fact_trips
GROUP BY 1
ORDER BY 1 DESC;