CREATE DATABASE IF NOT EXISTS public_transport_analytics;
USE public_transport_analytics;
CREATE TABLE IF NOT EXISTS transport_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    route VARCHAR(50) NOT NULL,
    stop VARCHAR(100) NOT NULL,
    service_date DATE NOT NULL,
    hour_of_day TINYINT NOT NULL,
    passengers INT NOT NULL DEFAULT 0,
    vehicle_capacity INT NULL,
    CHECK (hour_of_day BETWEEN 0 AND 23),
    CHECK (passengers >= 0)
);
-- Import data/public_transport_data.csv and map date -> service_date, hour -> hour_of_day.
