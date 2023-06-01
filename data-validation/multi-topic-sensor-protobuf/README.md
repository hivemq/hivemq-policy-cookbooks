# Multi-topic Protobuf schemas

This cookbook covers the use-case of validating multiple topics each with a different Protobuf schema.

### Use-case

> As a developer, I want to enforce that incoming sensor data over MQTT has the correct Protobuf data format for the
> topic it was published on.

Consider if there are two MQTT topics to which clients publish sensor data, `/temperature/{clientId}`,
and `/air/{clientId}`. Clients send different types of payloads to each topic, all serialized with Protobuf.

For this use-case, two schemas and two policies are needed.

### Temperature schema

The following `.proto` file describes the structure of incoming temperature data.

`temperature.proto`:

```proto
syntax = "proto3";
package io.hivemq.example;

message Temperature {
  float component_a_temperature = 1;
  float component_b_temperature = 2;
}
```

To use this schema, it must first be compiled with the Protobuf compiler:

```bash
protoc temperature.proto -o temperature.desc
```

See [here](https://grpc.io/docs/protoc-installation/) for information on installing the `protoc` command.

To create the schema in the broker, run the following command:

```bash
mqtt hivemq schemas create --id temperature-schema --type protobuf --file temperature.desc --message-type Temperature --allow-unknown false
```

The `--message-type` argument specifies that the `Temperature` message type from the Protobuf definition should be
used. The `--allow-unknown` argument specifies that additional unknown fields in incoming data are not
allowed according to [Protobuf Unknown Fields](https://protobuf.dev/programming-guides/proto3/#unknowns]).


### Temperature policy

The next step is to apply the schema for all incoming MQTT messages that are published under the topic `temperature/`.

The following policy applies to all messages that match the topic filter `temperature/#`.

`temperature-policy.json`:

```json
{
  "id": "temperature-policy",
  "matching": {
    "topicFilter": "temperature/#"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ALL_OF",
          "schemas": [
            {
              "schemaId": "temperature-schema",
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
          "level": "ERROR",
          "message": "The client with ID ${clientId} sent invalid temperature data: ${validationResult}"
        }
      }
    ]
  }
}
```

This ensures that all messages published to a topic under `temperature/` must conform to the provided Protobuf
specification for temperature data.

The `${validationResult}` string substitution in the log message means that the exact cause of the failure will be
logged.

To upload `temperature-policy.json` to the broker, run the following command:

```bash
mqtt hivemq policies create --file temperature-policy.json
```

### Air schema

The following `.proto` file describes the structure of incoming sensor data for air.

`air.proto`:

```proto
syntax = "proto3";
package io.hivemq.example;

message Air {
  float pressure = 1;
  float humidity = 2;
  float wind     = 3;
}
```

To compile it and upload it to the broker like with the temperature schema, run the following commands:

```bash
protoc air.proto -o air.desc
```

```bash
mqtt hivemq schemas create --id air-schema --type protobuf --file air.desc --message-type Air --allow-unknown false
```

### Air policy

A similar policy to the temperature policy can now be created and uploaded for the `air/` topic.

`air-policy.json`:

```json
{
  "id": "air-policy",
  "matching": {
    "topicFilter": "air/#"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ALL_OF",
          "schemas": [
            {
              "schemaId": "air-schema",
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
          "level": "ERROR",
          "message": "The client with ID ${clientId} sent invalid air data: ${validationResult}"
        }
      }
    ]
  }
}

```

To upload the air policy, run the following command:

```bash
mqtt hivemq policies create --file air-policy.json
```

### Listing policies

To see a list of the two policies that have been uploaded, run the following command:

```bash
mqtt hivemq policies list
```
