function normalizeVoltage(originalVoltage, sensorType) {
    switch (sensorType) {
        case 1:
            return originalVoltage; // volts
        case 2:
            return originalVoltage / 1000; // millivolts
        case 3:
            return originalVoltage * 1000; // kilovolts
        default:
            return originalVoltage; // Default to volts if unknown sensor type
    }
}

function transform(publish, context) {
    const type = publish.payload.sensorType;

    publish.payload = {
        "voltage": normalizeVoltage(publish.payload.voltage, type),
        "timestamp": publish.payload.timestamp,
    };

    return publish;
}
