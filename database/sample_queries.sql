USE public_transport_analytics;
SELECT SUM(passengers) AS recorded_passengers FROM transport_records;
SELECT route, SUM(passengers) AS passengers FROM transport_records GROUP BY route ORDER BY passengers DESC;
SELECT stop, SUM(passengers) AS passengers FROM transport_records GROUP BY stop ORDER BY passengers DESC;
SELECT hour_of_day, SUM(passengers) AS passengers FROM transport_records GROUP BY hour_of_day ORDER BY hour_of_day;
