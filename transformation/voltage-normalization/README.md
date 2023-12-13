# Normalize Voltage Levels
This cookbook is about normalizing voltage levels for energy monitoring.

### Use-case
> In an energy monitoring system, voltage readings are collected from various sensors and devices. These sensors may use different voltage scales. The analytics services require voltage data normalized to a standardized scale for consistent analysis.

For this use-case, a script, a policy, and a schema are required.

### Schema

To begin with, consider the following plain JSON schema (according to [JSON Schema](https://json-schema.org/)):

`schema-from-sensor.json`:
```json
{
  "type": "object",
  "properties": {
    "voltage": {
      "type": "number"
    },
    "sensor_type": {
      "type": "integer",
      "enum": [1, 2, 3]
    },
    "timestamp": {
      "type": "number"
    }
  },
  "required": [
    "voltage",
    "sensor_type",
    "timestamp"
  ]
}
```
which contains two required fields `voltage` and `timestamp` to be of type `number`. The `sensor_type` field of type `integer` can have values 1, 2, or 3, representing different types of sensors reporting in Volts, Millivolts, or Kilovolts, respectively.

After transformation, the field `voltage` is reported in volts. The schema for transformed MQTT messages is defined as follows:

`schema-for-analytics.json`:
```json
{
  "type": "object",
  "properties": {
    "voltage": {
      "type": "number"
    },
    "timestamp": {
      "type": "number"
    }
  },
  "required": [
    "voltage",
    "timestamp"
  ]
}
```

To upload the schemas to the broker, run the following commands:

```bash
mqtt hivemq schema create --id schema-from-sensor --type json --file schema-from-sensor.json
mqtt hivemq schema create --id schema-for-analytics --type json --file schema-for-analytics.json
```

### Transformation function
In HiveMQ Data Hub version 4.23 and later, we support JavaScript for the transformation of incoming MQTT
messages.

The following script normalizes voltage readings from volts, millivolts, and kilovolts to volts:

```javascript
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
    const sensorType = publish.payload.sensor_type;

    publish.payload = {
        "voltage": normalizeVoltage(publish.payload.voltage, sensorType),
        "timestamp": publish.payload.timestamp
    }

    return publish;
}
```
The function `transform` has two parameters, a publish-object and a context-publish. A new publish-object is created
with the field `voltage` normalized from the field `voltage` and the original timestamp of the incoming publish.

The function is uploaded to the broker with the following command:

```basH
mqtt hivemq script create --id voltage-normalization --type transformation --file script.js
```

### Policy
The next step is to create a policy that validates against the `schema-from-sensor` schema, normalizes voltage values by executing
the transformation script, and publishes the payload to the original topic.

`policy.json`:
```json
{
  "id": "voltage-level-normalization",
  "matching": {
    "topicFilter": "energy/#"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ALL_OF",
          "schemas": [
            {
              "schemaId": "schema-from-sensor",
              "version": "latest"
            }
          ]
        }
      }
    ]
  },
  "onSuccess": {
    "pipeline": [
      {
        "id": "deserialize",
        "functionId": "Serdes.deserialize",
        "arguments": {
          "schemaVersion": "latest",
          "schemaId": "schema-from-sensor"
        }
      },
      {
        "id": "voltage-normalization",
        "functionId": "fn:voltage-normalization:latest",
        "arguments": {}
      },
      {
        "id": "serialize",
        "functionId": "Serdes.serialize",
        "arguments": {
          "schemaVersion": "latest",
          "schemaId": "schema-for-analytics"
        }
      }
    ]
  },
  "onFailure": {
    "pipeline": [
      {
        "id": "drop-invalid-message",
        "functionId": "Mqtt.drop",
        "arguments": {
          "reasonString": "Your client ${clientId} sent invalid data according to the schema: ${validationResult}."
        }
      }
    ]
  }
}
```

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq data-policy create --file policy.json
```

The policy is now applied, and all incoming MQTT messages matching the topic filter `energy/#` are subject to validation. When validation for an incoming message is successful, the transformation script to normalize the voltage levels is executed so that the consumer only reads standardized voltage values.


### Examples of Original and Transformed Data
Original data before normalization:
```json
{
  "voltage": 220,
  "sensor_type": 1,
  "timestamp": 1702424452
}
```
```json
{
  "voltage": 700,
  "sensor_type": 2,
  "timestamp": 1702424452
}
```
```json
{
  "voltage": 66,
  "sensor_type": 3,
  "timestamp": 1702424452
}
```

Transformed data after normalization:
```json
{
  "voltage": 220,
  "timestamp": 1702424452
}
```
```json
{
  "voltage": 0.7,
  "timestamp": 1702424452
}
```
```json
{
  "voltage": 66000,
  "timestamp": 1702424452
}
```
In these examples, the original data represents voltage readings from three different sensors with `sensor_type` values of `1`, `2`, and `3`, respectively. The transformed data shows the normalized voltage values in volts for consistent analysis in an energy monitoring system.