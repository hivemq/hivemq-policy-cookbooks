
CREATE TABLE IF NOT EXISTS bad_clients (
    id SERIAL,
    topic TEXT,
    payload_base64 TEXT,
    qos TEXT,
    retain BOOLEAN,
    packet_id INT,
    payload_format_indicator TEXT,
    response_topic TEXT,
    correlation_data_base64 TEXT,
    arrival_timestamp NUMERIC,
    PRIMARY KEY(id)
);