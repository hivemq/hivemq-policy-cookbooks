function normalizeVoltage(originalVoltage, sensorType) {
    switch (sensorType) {
        case 1:
            return originalVoltage; // Volts
        case 2:
            return originalVoltage / 1000; // Millivolts
        case 3:
            return originalVoltage * 1000; // Kilovolts
        default:
            return originalVoltage; // Default to Volts if unknown sensor type
    }
}

function transform(publish, context) {
    const sensorType = publish.payload.sensor_type;

    publish.payload = {
        "voltage": normalizeVoltage(publish.payload.voltage, sensorType),
        "timestamp": publish.payload.timestamp
    }

    return publish;
}
