# Location Data Schema
This cookbook covers how to accept any one of multiple possible schemas on a single topic.


### Use-case
> As a developer, I want to be able to accept all JSON messages that come from one of a number of different geographic regions, and reject everything outside of these.

The use-case here is that multiple MQTT clients publish messages that may contain coordinate information either from Europe or the USA on the `location` topic. It is useful to reject all instances of messages that are not from one of these regions, and log this rejection.

For this use-case, two schemas and one policy are needed.


### USA Location Schema

First, create the following JSON schema:

`usa-schema.json`:
```json
{
  "title": "USA Location Data",
  "description": "A schema that matches any objects with longitude and latitude coordinates near the USA",
  "required": [
    "latitude",
    "longitude"
  ],
  "type": "object",
  "properties": {
    "latitude": {
      "type": "number",
      "minimum": 20,
      "maximum": 50
    },
    "longitude": {
      "type": "number",
      "minimum": -130,
      "maximum": -60
    }
  }
}
```

It matches any JSON payloads which contain a `latitude` and  `longitude` property in a range that very approximately corresponds to the bounds of the contiguous United States.

Encode the schema as a Base64 string:

```bash
base64 -i usa-schema.json
```

The following request adds this schema to the broker, using the encoded Base64 string for the `schemaDefinition` field:

`usa-schema-request.json`:
```json
{
  "id": "usa-coordinates",
  "type": "JSON",
  "schemaDefinition": "ewogICJ0aXRsZSI6ICJVU0EgTG9jYXRpb24gRGF0YSIsCiAgImRlc2NyaXB0aW9uIjogIkEgc2NoZW1hIHRoYXQgbWF0Y2hlcyBhbnkgb2JqZWN0cyB3aXRoIGxvbmdpdHVkZSBhbmQgbGF0aXR1ZGUgY29vcmRpbmF0ZXMgbmVhciB0aGUgVVNBIiwKICAicmVxdWlyZWQiOiBbCiAgICAibGF0aXR1ZGUiLAogICAgImxvbmdpdHVkZSIKICBdLAogICJ0eXBlIjogIm9iamVjdCIsCiAgInByb3BlcnRpZXMiOiB7CiAgICAibGF0aXR1ZGUiOiB7CiAgICAgICJ0eXBlIjogIm51bWJlciIsCiAgICAgICJtaW5pbXVtIjogMjAsCiAgICAgICJtYXhpbXVtIjogNTAKICAgIH0sCiAgICAibG9uZ2l0dWRlIjogewogICAgICAidHlwZSI6ICJudW1iZXIiLAogICAgICAibWluaW11bSI6IC0xMzAsCiAgICAgICJtYXhpbXVtIjogLTYwCiAgICB9CiAgfQp9"
}
```

The identifier of this schema is `usa-coordinates`.

To upload `usa-schema-request.json` to the broker, run the following command:

```bash
curl -X POST --data @usa-schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas
```

suppose your HiveMQ REST API runs at `http://localhost:8888`.


### Europe Location Schema

Create the following JSON schema:

`europe-schema.json`:
```json
{
  "title": "Europe Location Data",
  "description": "A schema that matches any objects with longitude and latitude coordinates near Europe",
  "required": [
    "latitude",
    "longitude"
  ],
  "type": "object",
  "properties": {
    "latitude": {
      "type": "number",
      "minimum": 30,
      "maximum": 70
    },
    "longitude": {
      "type": "number",
      "minimum": -30,
      "maximum": 50
    }
  }
}
```

This is similar to the USA schema but matches European coordinates instead.

Encode the schema as a Base64 string and upload it to the broker in the same way as the USA schema:

```bash
base64 -i europe-schema.json
```

`europe-schema-request.json`:
```json
{
  "id": "europe-coordinates",
  "type": "JSON",
  "schemaDefinition": "ewogICJ0aXRsZSI6ICJFdXJvcGUgTG9jYXRpb24gRGF0YSIsCiAgImRlc2NyaXB0aW9uIjogIkEgc2NoZW1hIHRoYXQgbWF0Y2hlcyBhbnkgb2JqZWN0cyB3aXRoIGxvbmdpdHVkZSBhbmQgbGF0aXR1ZGUgY29vcmRpbmF0ZXMgbmVhciBFdXJvcGUiLAogICJyZXF1aXJlZCI6IFsKICAgICJsYXRpdHVkZSIsCiAgICAibG9uZ2l0dWRlIgogIF0sCiAgInR5cGUiOiAib2JqZWN0IiwKICAicHJvcGVydGllcyI6IHsKICAgICJsYXRpdHVkZSI6IHsKICAgICAgInR5cGUiOiAibnVtYmVyIiwKICAgICAgIm1pbmltdW0iOiAzMCwKICAgICAgIm1heGltdW0iOiA3MAogICAgfSwKICAgICJsb25naXR1ZGUiOiB7CiAgICAgICJ0eXBlIjogIm51bWJlciIsCiAgICAgICJtaW5pbXVtIjogLTMwLAogICAgICAibWF4aW11bSI6IDUwCiAgICB9CiAgfQp9Cg=="
}
```

```bash
curl -X POST --data @europe-schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas
```


### Policy

The next step is to create a policy using these two schemas for incoming MQTT messages matching the topic `location`.

The following policy tests if incoming messages match either the USA schema or the Europe schema:

`policy.json`:
```json
{
  "id": "location-policy",
  "matching": {
    "topicFilter": "location"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ANY_OF",
          "schemas": [
            {
              "schemaId": "europe-coordinates"
            },
            {
              "schemaId": "usa-coordinates"
            }
          ]
        }
      }
    ]
  },
  "onSuccess": {
    "pipeline": [
      {
        "id": "logSuccess",
        "functionId": "log",
        "arguments": {
          "level": "INFO",
          "message": "The client ${clientId} published coordinate data"
        }
      },
      {
        "id": "incrementGoodCoordinatesMetric",
        "functionId": "Metrics.Counter.increment",
        "arguments": {
          "metricName": "valid-coordinates",
          "incrementBy": 1
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
          "message": "The client ${clientId} attempted to publish invalid coordinate data: ${validationResult}"
        }
      },
      {
        "id": "incrementBadCoordinatesMetric",
        "functionId": "Metrics.Counter.increment",
        "arguments": {
          "metricName": "invalid-coordinates",
          "incrementBy": 1
        }
      }
    ]
  }
}
```

When validation succeeds it will be logged at the `INFO` level and include the client ID using the `${clientId}` string substitution. When validation fails it will be logged at the `WARN` level and also include the reason for failure using the `${validationResult}` string substitution. Moreover, for both cases custom metrics are created: `com.hivemq.data-governance-hub.data-validation.custom.counters.valid-coordinates` and `com.hivemq.data-governance-hub.data-validation.custom.counters.invalid-coordinates`.

The `ANY_OF` validation strategy ensures that only one of the schemas needs to be matched, not both.

To upload `policy.json` to the broker, run the following command:

```bash
curl -X POST --data @policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies
```

## Quality Metric
Check out the script `generate-random-data.sh` that continously generates random GPS coordinates according to the `usa-coordinates` schema.
However, some of them are invalid. Since we added a metric function to count invalid and valid messages a quality metric can be easily defined.

Suppose you have a Prometheus server running andPrometheus Extension installed available at [HiveMQ's website](https://www.hivemq.com/extension/prometheus-extension/) you can run a PromQL statement to derive a quality metric:

```
com_hivemq_data_governance_hub_data_validation_custom_counters_valid_coordinates / (com_hivemq_data_governance_hub_data_validation_custom_counters_invalid_coordinates + com_hivemq_data_governance_hub_data_validation_custom_counters_valid_coordinates)
```
Consequently, alerts can be defined to be notified for certain threshold violation.