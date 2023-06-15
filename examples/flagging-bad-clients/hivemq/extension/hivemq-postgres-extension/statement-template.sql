INSERT INTO bad_clients(topic, payload_base64, qos, retain, packet_id, payload_format_indicator, response_topic, correlation_data_base64, arrival_timestamp)
 VALUES(
    ${mqtt-topic},
    ${mqtt-payload-base64},
    ${mqtt-qos},
    ${mqtt-retain},
    ${mqtt-packet-id},
    ${mqtt-payload-format-indicator},
    ${mqtt-response-topic},
    ${mqtt-correlation-data-base64},
    ${timestamp}
);