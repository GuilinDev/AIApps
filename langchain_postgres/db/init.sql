CREATE TABLE alert (
    alert_id SERIAL PRIMARY KEY,
    alert_name VARCHAR(255) NOT NULL,
    component_path VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

INSERT INTO alert (alert_name, component_path, status, start_time, end_time) VALUES
('Alert1', 'jd1.prod.health_type1', 'degraded', '2024-06-01 12:00:00', '2024-06-01 13:00:00'),
('Alert2', 'jd3.impl.health_type2', 'disrupted', '2024-06-02 14:00:00', '2024-06-02 15:00:00'),
('Alert3', 'jd10.prod.health_type3', 'available', '2024-06-03 16:00:00', '2024-06-03 17:00:00');
