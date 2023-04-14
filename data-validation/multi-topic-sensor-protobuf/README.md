# Multi-topic Protobuf schemas
This cookbook covers the use-case of validating multiple topics with different Protobuf schemas.

## Use-Case 
> As a developer, I want to enforce that incoming sensor data over MQTT has the correct Protobuf data format for the topic it was published on.

Consider if there are two MQTT topics to which clients publish sensor data, `/temperature/{clientId}`, and `/air/{clientId}`. Clients send different types of payloads to each topic, all serialized with Protobuf.

For this use-case, two schemas and two policies are needed.

### Temperature schema

The following `.proto` file describes the structure of incoming temperature data.

`temperature.proto`:
```proto
syntax = "proto3";
package com.example;

message Temperature {
  float component_a_temperature = 1;
  float component_b_temperature = 2;
}

```

To use this schema, it must first be compiled with the Protobuf compiler, and then the result encoded as Base64:

```bash
protoc temperature.proto -o /dev/stdout | base64
```

Place the resulting Base64 string into the `schemaDefinition` field of the request:

`temperature-schema-request.json`:
```json
{
  "id": "temperature-schema",
  "type": "PROTOBUF",
  "schemaDefinition": "CqcBChF0ZW1wZXJhdHVyZS5wcm90bxILY29tLmV4YW1wbGUifQoLVGVtcGVyYXR1cmUSNgoXY29tcG9uZW50X2FfdGVtcGVyYXR1cmUYASABKAJSFWNvbXBvbmVudEFUZW1wZXJhdHVyZRI2Chdjb21wb25lbnRfYl90ZW1wZXJhdHVyZRgCIAEoAlIVY29tcG9uZW50QlRlbXBlcmF0dXJlYgZwcm90bzM",
  "arguments": {
    "messageType": "Temperature",
    "allowUnknownFields": "false"
  }
}
```

The `arguments` field specifies that the `Temperature` message type from the Protobuf definition should be used, and that additional unknown fields in incoming data are not allowed.

To upload the `temperature-schema-request` to the broker, run the following command:

```bash
curl -X POST --data @temperature-schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/schemas
```
suppose your HiveMQ REST API runs at `http://localhost:8888`.


### Temperature policy

The next step is to apply the schema for all incoming MQTT messages that are published under the topic `temperature/`.

The following policy applies to all messages that match the topic filter `temperature/#`.

`temperature-policy.json`:
```json
{
  "name": "temperature-policy",
  "matching": {
    "topicFilter": "temperature/#"
  },
  "validation": {
    "schemaId": "temperature-schema"
  },
  "onSuccess": {
    "continue": true
  },
  "onFailure": {
    "continue": false,
    "log": {
      "level": "DEBUG",
      "message": "The client with ID $clientId sent invalid temperature data: $validationResult"
    }
  }
}
```

This ensures that all messages published to a topic under `temperature/` must conform to the Protobuf specification.

The `$validationResult` substitution in the log message means that the exact cause of the failure will be logged. 

To upload the `temperature-policy.json` to the broker, run the following command:
```bash
curl -X POST --data @temperature-policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/policies
```


### Air schema

The following `.proto` file describes the structure of incoming sensor data for air.

`air.proto`:
```proto
syntax = "proto3";
package com.example;

message Air {
  float pressure = 1;
  float humidity = 2;
  float wind     = 3;
}
```

To compile it and upload it to the broker like with the temperature schema, run the following:

```bash
protoc air.proto -o /dev/stdout | base64
```

Place the resulting Base64 string into the `schemaDefinition` field:

`air-schema-request.json`:
```json
{
  "id": "air-schema",
  "type": "PROTOBUF",
  "schemaDefinition": "CnMKCWFpci5wcm90bxILY29tLmV4YW1wbGUiUQoDQWlyEhoKCHByZXNzdXJlGAEgASgCUghwcmVzc3VyZRIaCghodW1pZGl0eRgCIAEoAlIIaHVtaWRpdHkSEgoEd2luZBgDIAEoAlIEd2luZGIGcHJvdG8z",
  "arguments": {
    "messageType": "Air",
    "allowUnknownFields": "false"
  }
}
```

To upload the schema, run the following command:

```bash
curl -X POST --data @air-schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/schemas
```


### Air policy

A similar policy to the temperature policy can now be created and uploaded for the `air/` topic.

`air-policy.json`:
```json
{
  "name": "air-policy",
  "matching": {
    "topicFilter": "air/#"
  },
  "validation": {
    "schemaId": "air-schema"
  },
  "onSuccess": {
    "continue": true
  },
  "onFailure": {
    "continue": false,
    "log": {
      "level": "DEBUG",
      "message": "The client with ID $clientId sent invalid air data: $validationResult"
    }
  }
}
```

To upload the air policy, run the following command:

```bash
curl -X POST --data @air-policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/policies
```

### Listing policies

To see a list of the two policies that have been uploaded, run the following command:

```bash
curl -X GET http://localhost:8888/api/v1/policies
```
