# Multiple Required JSON Schemas

This cookbook is about requiring multiple JSON schemas in a single policy.

### Use-case

> As a developer, I want to enforce that all MQTT payloads conform to multiple specified JSON Schemas, to ensure that
> all data structure requirements are met.

For this use-case, a policy and three schemas are required.

### Schemas

Consider the following three schemas defined according to the [JSON Schema](https://json-schema.org/) specification:

`metadata-schema.json`:
```json
{
  "description": "A schema that specifies fields for payload metadata",
  "required": [
    "publisherId",
    "timestamp"
  ],
  "type": "object",
  "properties": {
    "publisherId": {
      "type": "string"
    },
    "timestamp": {
      "type": "number"
    }
  }
}
```

`data-schema.json`:
```json
{
  "description": "A schema that specifies fields for payload data",
  "required": [
    "values"
  ],
  "type": "object",
  "properties": {
    "values": {
      "type": "array",
      "items": {
        "type": "number"
      }
    }
  }
}
```

`verification-schema.json`:
```json
{
  "description": "A schema that specifies fields required for data integrity checks",
  "required": [
    "checksum",
    "signature"
  ],
  "type": "object",
  "properties": {
    "checksum": {
      "type": "number"
    },
    "signature": {
      "type": "string"
    }
  }
}
```

Each of these schemas alone defines some fields that may be required in an MQTT JSON payload.

Upload the three schemas to the broker using the following commands:

```bash
mqtt hivemq schemas create --id metadata-schema --type json --file metadata-schema.json
```

```bash
mqtt hivemq schemas create --id data-schema --type json --file data-schema.json
```

```bash
mqtt hivemq schemas create --id verification-schema --type json --file verification-schema.json
```

### Policy

The next step is to create a policy to validate all incoming MQTT messages against all three schemas, requiring that the
fields from every schema are present in the message JSON payload.

The following policy uses a `topicFilter` of `#` which will match all messages on every topic:

`policy.json`:

```json
{
  "id": "multiple-json-schemas-policy",
  "matching": {
    "topicFilter": "#"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ALL_OF",
          "schemas": [
            {
              "schemaId": "metadata-schema",
              "version" : "latest"
            },
            {
              "schemaId": "data-schema",
              "version" : "latest"
            },
            {
              "schemaId": "verification-schema",
              "version" : "latest"
            }
          ]
        }
      }
    ]
  },
  "onFailure": {
    "pipeline": [
      {
        "id": "logFailure",
        "functionId": "System.log",
        "arguments": {
          "level": "WARN",
          "message": "The client ${clientId} does not send valid JSON payloads. The message will be dropped. Reason: ${validationResult}"
        }
      }
    ]
  }
}
```

The `validators` section in the policy definition uses the `ALL_OF` validation strategy to specify that MQTT messages
must successfully match all three referenced schemas to be published.

If a MQTT message fails to validate for any of the three schemas, a message is logged using the `System.log` function with the
client ID and the reason for validation failure.

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq policies create --file policy.json
```
