# Location Data Schema
This cookbook covers logging the client ID and topic of messages that match a specific JSON schema.

## Use-Case
> As a developer, I want to be notified of messages that contain erroneous data which should have been published to a different topic.

The use-case here is that multiple MQTT clients publish messages that may contain coordinate information either from Europe or the USA, on the `europe/` and `usa/` topics respectively. It is useful to log all instances of messages being published that seem to contain coordinates for the wrong region, so that they can be debugged.

For this use-case a policy which logs instances of US coordinate information being published on `europe/#` MQTT topics is needed. A schema is required for this:

### Schema

First, the following JSON schema is created:

`schema.json`:
```json
{
  "title": "Location Data",
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

The following request adds this schema to the broker:

`schema-request.json`:
```json
{
  "id": "usa-coordinates",
  "type": "JSON",
  "schemaDefinition": "{\"title\":\"Location Data\",\"description\":\"A schema that matches any objects with longitude and latitude coordinates near the USA\",\"required\":[\"latitude\",\"longitude\"],\"type\":\"object\",\"properties\":{\"latitude\":{\"type\":\"number\",\"minimum\":20,\"maximum\":50},\"longitude\":{\"type\":\"number\",\"minimum\":-130,\"maximum\":-60}}}"
}
```

The identifier of this schema is `usa-coordinates`.

To upload the `schema-request.json` to the broker, run the following command:
```bash
curl -X POST --data @schema-request.json -H "Content-Type: application/json` http://localhost:8888/api/v1/schemas
```
suppose your HiveMQ REST API runs at `http://localhost:8888`.


### Policy

The next step is to apply the schema for incoming MQTT messages matching the topic filter `europe/#` with a policy.

The following policy logs any messages matching the schema at the `INFO` level and includes the client ID and published topic using the `$clientID` and `$topic` string substitutions:

`policy.json`:
```json
{
  "name": "log-usa-coords-in-europe",
  "matching": {
    "topicFilter": "europe/#"
  },
  "validation": {
    "schemaId": "usa-coordinates"
  },
  "onSuccess": {
    "continue": true,
    "log": {
      "level": "INFO",
      "message": "The client $clientId published coordinate data near the US on topic $topic"
    }
  },
  "onFailure": {
    "continue": true
  }
}
```

To upload the `policy.json` to the broker, run the following command:
```bash
curl -X POST --data @policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/policies
```

To delete the policy, run the following command:
```bash
curl -X DELETE -H "Content-Type: application/json" http://localhost:8888/api/v1/policies/log-usa-coords-in-europe
```
