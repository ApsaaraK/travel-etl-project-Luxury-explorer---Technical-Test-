DROP TABLE IF EXISTS bookings;

CREATE TABLE bookings (
    id                SERIAL PRIMARY KEY,
    hotel_name        VARCHAR(100)   NOT NULL DEFAULT 'Unknown',
    category          VARCHAR(50)    NOT NULL DEFAULT 'Uncategorized',
    country           VARCHAR(50)    NOT NULL DEFAULT 'Unknown',
    price             NUMERIC(10,2)  CHECK (price > 0),
    rating            NUMERIC(3,1)   CHECK (rating >= 1 AND rating <= 5),
    customer_name     VARCHAR(100),
    booking_date      DATE,
    payment_method    VARCHAR(50)
);

CREATE INDEX idx_bookings_country   ON bookings(country);
CREATE INDEX idx_bookings_category  ON bookings(category);
CREATE INDEX idx_bookings_date      ON bookings(booking_date);
CREATE INDEX idx_bookings_price     ON bookings(price);