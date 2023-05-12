# Multiple Required JSON Schemas
This cookbook is about requiring multiple JSON schemas in a single policy.


### Use-Case
> As a developer, I want to enforce that all MQTT payloads conform to multiple specified JSON Schemas, to ensure that all data structure requirements are met.

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

Convert each of these three files to a Base64 string with the following command:

```bash
base64 -i filename.json
```

replacing `filename.json` with the name of the schema file being converted.

A separate request has to be made for each schema to upload it to the broker:

`metadata-schema-request.json`:
```json
{
  "id": "metadata-schema",
  "type": "JSON",
  "schemaDefinition": "ewogICJkZXNjcmlwdGlvbiI6ICJBIHNjaGVtYSB0aGF0IHNwZWNpZmllcyBmaWVsZHMgZm9yIHBheWxvYWQgbWV0YWRhdGEiLAogICJyZXF1aXJlZCI6IFsKICAgICJwdWJsaXNoZXJJZCIsCiAgICAidGltZXN0YW1wIgogIF0sCiAgInR5cGUiOiAib2JqZWN0IiwKICAicHJvcGVydGllcyI6IHsKICAgICJwdWJsaXNoZXJJZCI6IHsKICAgICAgInR5cGUiOiAic3RyaW5nIgogICAgfSwKICAgICJ0aW1lc3RhbXAiOiB7CiAgICAgICJ0eXBlIjogIm51bWJlciIKICAgIH0KICB9Cn0K"
}
```

`data-schema-request.json`:
```json
{
  "id": "data-schema",
  "type": "JSON",
  "schemaDefinition": "ewogICJkZXNjcmlwdGlvbiI6ICJBIHNjaGVtYSB0aGF0IHNwZWNpZmllcyBmaWVsZHMgZm9yIHBheWxvYWQgZGF0YSIsCiAgInJlcXVpcmVkIjogWwogICAgInZhbHVlcyIKICBdLAogICJ0eXBlIjogIm9iamVjdCIsCiAgInByb3BlcnRpZXMiOiB7CiAgICAidmFsdWVzIjogewogICAgICAidHlwZSI6ICJhcnJheSIsCiAgICAgICJpdGVtcyI6IHsKICAgICAgICAidHlwZSI6ICJudW1iZXIiCiAgICAgIH0KICAgIH0KICB9Cn0K"
}
```

`verification-schema-request.json`:
```json
{
  "id": "verification-schema",
  "type": "JSON",
  "schemaDefinition": "ewogICJkZXNjcmlwdGlvbiI6ICJBIHNjaGVtYSB0aGF0IHNwZWNpZmllcyBmaWVsZHMgcmVxdWlyZWQgZm9yIGRhdGEgaW50ZWdyaXR5IGNoZWNrcyIsCiAgInJlcXVpcmVkIjogWwogICAgImNoZWNrc3VtIiwKICAgICJzaWduYXR1cmUiCiAgXSwKICAidHlwZSI6ICJvYmplY3QiLAogICJwcm9wZXJ0aWVzIjogewogICAgImNoZWNrc3VtIjogewogICAgICAidHlwZSI6ICJudW1iZXIiCiAgICB9LAogICAgInNpZ25hdHVyZSI6IHsKICAgICAgInR5cGUiOiAic3RyaW5nIgogICAgfQogIH0KfQo="
}
```

where `id` corresponds to the `schemaId`, and `schemaDefinition` holds the generated Base64 string.

For each of these schema requests, use the following command to upload them to the broker, replacing `filename.json` with the corresponding request filenames: `metadata-schema-request.json`, `data-schema-request.json`, and `verification-schema-request.json`:

```bash
curl -X POST --data @filename.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas
```

suppose your HiveMQ REST API runs at `http://localhost:8888`.


### Policy
The next step is to create a policy to validate all incoming MQTT messages against all three schemas, required that the fields from every schema are present in the message JSON payload.

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
              "schemaId": "metadata-schema"
            },
            {
              "schemaId": "data-schema"
            },
            {
              "schemaId": "verification-schema"
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
        "functionId": "log",
        "arguments": {
          "level": "WARN",
          "message": "The client $clientId does not send valid JSON payloads. The message will be dropped. Reason: $validationResult"
        }
      }
    ]
  }
}
```

The `validators` section in the policy definition uses the `ALL_OF` validation strategy to specify that MQTT messages must successfully match all three referenced schemas to be published.

If a MQTT message fails to validate for any of the three schemas, a message is logged using the `log` function with the client ID and the reason for validation failure.

To upload `policy.json` to the broker, run the following command:
```bash
curl -X POST --data @policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies
```
