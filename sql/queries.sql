SELECT 
    category,
    COUNT(*)                    AS total_bookings,
    ROUND(SUM(price)::numeric, 2)  AS total_revenue,
    ROUND(AVG(price)::numeric, 2)  AS avg_price
FROM bookings
GROUP BY category
ORDER BY total_revenue DESC
LIMIT 10;

SELECT 
    DATE_TRUNC('month', booking_date)  AS month,
    COUNT(*)                           AS total_bookings,
    ROUND(SUM(price)::numeric, 2)      AS monthly_revenue
FROM bookings
WHERE booking_date IS NOT NULL
GROUP BY month
ORDER BY month;

SELECT 
    country,
    COUNT(*)                          AS total_bookings,
    ROUND(AVG(rating)::numeric, 2)    AS avg_rating,
    ROUND(AVG(price)::numeric, 2)     AS avg_price
FROM bookings
GROUP BY country
ORDER BY avg_rating DESC;

SELECT 
    payment_method,
    COUNT(*)                        AS total_bookings,
    ROUND(SUM(price)::numeric, 2)   AS total_revenue
FROM bookings
GROUP BY payment_method
ORDER BY total_bookings DESC;