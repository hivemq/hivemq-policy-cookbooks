# Location Data Schema

This cookbook covers how to accept any one of multiple possible schemas on a single topic.

### Use-case

> As a developer, I want to be able to accept all JSON messages that come from one of a number of different geographic
> regions, and reject everything outside of these.

The use-case here is that multiple MQTT clients publish messages that may contain coordinate information either from
Europe or the USA on the `location` topic. It is useful to reject all instances of messages that are not from one of
these regions, and log this rejection.

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

It matches any JSON payloads which contain a `latitude` and  `longitude` property in a range that very approximately
corresponds to the bounds of the contiguous United States.

To upload the schema to the broker, run the following command:

```bash
mqtt hivemq schemas create --id usa-coordinates --type json --file usa-schema.json
```

This uses the identifier `usa-coordinates` for the schema.

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

Upload the schema to the broker with the id `europe-schema` in the same way as the USA schema:

```bash
mqtt hivemq schemas create --id europe-schema --type json --file europe-schema.json
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
              "schemaId": "europe-coordinates",
              "version" : "latest"
            },
            {
              "schemaId": "usa-coordinates",
              "version" : "latest"
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
        "functionId": "System.log",
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
        "functionId": "System.log",
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

When validation succeeds it will be logged at the `INFO` level and include the client ID using the `${clientId}` string
substitution. When validation fails it will be logged at the `WARN` level and also include the reason for failure using
the `${validationResult}` string substitution. Moreover, for both cases custom metrics are
created: `com.hivemq.data-governance-hub.data-validation.custom.counters.valid-coordinates`
and `com.hivemq.data-governance-hub.data-validation.custom.counters.invalid-coordinates`.

The `ANY_OF` validation strategy ensures that only one of the schemas needs to be matched, not both.

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq policies create --file policy.json
```

### Quality Metric

Check out the script `generate-random-data.sh` that continuously generates random GPS coordinates according to
the `usa-coordinates` schema. However, some of them are invalid. Since we added a metric function to count invalid and
valid messages, a quality metric can be easily defined.

Suppose you have a Prometheus server running and the Prometheus Extension installed (available
at [HiveMQ's website](https://www.hivemq.com/extension/prometheus-extension/)). You can run a PromQL statement to derive
a quality metric:

```
com_hivemq_data_governance_hub_data_validation_custom_counters_valid_coordinates / (com_hivemq_data_governance_hub_data_validation_custom_counters_invalid_coordinates + com_hivemq_data_governance_hub_data_validation_custom_counters_valid_coordinates)
```

With this, the metric function makes it possible to define alerts to notify when a certain threshold is reached. 