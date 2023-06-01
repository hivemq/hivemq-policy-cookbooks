# Redirect Messages with Legacy Schemas
This cookbook covers how to accept multiple versions of a schema and redirect messages that follow the older schema version to the correct topic.


### Use-case
> As a developer, I want to be able to update my schema to a newer version. Messages from devices using the previous version should still be accepted but should be rerouted to a separate topic.

The use-case here involves accepting device status Protobuf messages on the `devices/v2/{clientId}/status` topic.

Messages may conform to either version 1 or version 2 of a schema. Version 1 messages should be published to `devices/v1/{clientId}/status`. Any version 1 messages incorrectly published to `devices/v2/{clientId}/status` should be redirected to the `v1` topic and published there instead.

For this use-case, two schemas and two policies are needed.


### Schemas

The following `.proto` file describes the older version of the device status schema:

`v1-status-schema.proto`:
```proto
syntax = "proto3";
package io.hivemq.example;

message DeviceStatus {
  bool  powered = 1;
  float temperature = 2;
}
```

To use this schema, it must first be compiled with the Protobuf compiler, and then the result encoded as Base64:

```bash
protoc v1-status-schema.proto -o /dev/stdout | base64
```

See [here](https://grpc.io/docs/protoc-installation/) for information on installing the `protoc` command.

Place the resulting Base64 string into the `schemaDefinition` field of the request and use the identifier `v1-status-schema`:

`v1-schema-request.json`:
```json
{
  "id": "v1-status-schema",
  "type": "PROTOBUF",
  "schemaDefinition": "Cn8KFnYxLXN0YXR1cy1zY2hlbWEucHJvdG8SEWlvLmhpdmVtcS5leGFtcGxlIkoKDERldmljZVN0YXR1cxIYCgdwb3dlcmVkGAEgASgIUgdwb3dlcmVkEiAKC3RlbXBlcmF0dXJlGAIgASgCUgt0ZW1wZXJhdHVyZWIGcHJvdG8z",
  "arguments": {
    "messageType": "DeviceStatus",
    "allowUnknownFields": "false"
  }
}
```

The `arguments` field specifies that the `DeviceStatus` message type from the Protobuf definition should be used, and that additional unknown fields in incoming data are not allowed.

To upload `v1-schema-request.json` to the broker, run the following command:

```bash
curl -X POST --data @v1-schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas
```

suppose your HiveMQ REST API runs at `http://localhost:8888`.

Suppose version 2 of the schema includes an additional `speed` field:

`v2-status-schema.proto`:
```proto
syntax = "proto3";
package io.hivemq.example;

message DeviceStatus {
  bool  powered = 1;
  float temperature = 2;
  float speed = 3;
}
```

As with version 1, upload this version 2 schema to the broker with the identifier `v2-status-schema`:

```bash
protoc v2-status-schema.proto -o /dev/stdout | base64
```

`v2-schema-request.json`:
```json
{
  "id": "v2-status-schema",
  "type": "PROTOBUF",
  "schemaDefinition": "CrEBCjJyZXBvL3JlZGlyZWN0LWxlZ2FjeS1zY2hlbWEvdjItc3RhdHVzLXNjaGVtYS5wcm90bxIRaW8uaGl2ZW1xLmV4YW1wbGUiYAoMRGV2aWNlU3RhdHVzEhgKB3Bvd2VyZWQYASABKAhSB3Bvd2VyZWQSIAoLdGVtcGVyYXR1cmUYAiABKAJSC3RlbXBlcmF0dXJlEhQKBXNwZWVkGAMgASgCUgVzcGVlZGIGcHJvdG8z",
  "arguments": {
    "messageType": "DeviceStatus",
    "allowUnknownFields": "false"
  }
}
```

```bash
curl -X POST --data @v2-schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas
```


### All Versions Policy

Next, a policy must be created to ensure that all published messages follow one of these schemas.

Because messages may be published to either `devices/v1/{clientId}/status` or `devices/v2/{clientId}/status`, the topic filter `devices/+/+/status` is used to cover both possibilities:

`all-versions-policy.json`:
```json
{
  "id": "all-device-statuses",
  "matching": {
    "topicFilter": "devices/+/+/status"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ANY_OF",
          "schemas": [
            {
              "schemaId": "v1-status-schema",
              "version" : "latest"
            },
            {
              "schemaId": "v2-status-schema",
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
        "functionId": "log",
        "arguments": {
          "level": "WARN",
          "message": "The client ${clientId} sent invalid status data to ${topic}"
        }
      }
    ]
  }
}
```

The `ANY_OF` validation strategy allows incoming messages to match either of the two specified schemas.

If a message does not follow either schema, a warning will be logged with the client ID and topic and the message will not be published.

To upload `all-versions-policy.json` to the broker, run the following command:
```bash
curl -X POST --data @all-versions-policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies
```


### Redirecting Policy

Next, a policy for `v2` topics specifically is needed. It should only accept messages that conform to the version 2 schema and redirect others to the `v1` topic.

Use the topic filter `devices/v2/+/status`:

`v2-status-policy.json`:
```json
{
  "id": "v2-device-statuses",
  "matching": {
    "topicFilter": "devices/v2/+/status"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ALL_OF",
          "schemas": [
            {
              "schemaId": "v2-status-schema",
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
        "id": "logRedirect",
        "functionId": "log",
        "arguments": {
          "level": "WARN",
          "message": "The client ${clientId} sent status data with a legacy format to topic ${topic}, the message will be redirected to devices/v1/${clientId}/status"
        }
      },
      {
        "id": "redirect",
        "functionId": "to",
        "arguments": {
          "topic": "devices/v1/${clientId}/status",
          "applyPolicies": true
        }
      }
    ]
  }
}
```

The `onFailure` pipeline specifies the sequence of actions that is taken if a message does not conform to the `v2-status-schema` schema.

First, a warning is logged using the `log` function. This contains the client ID and topic using the `${clientId}` and `${topic}` string substitutions.

Then, the message is redirected using the `to` function to the topic `devices/v1/${clientId}/status`. The `applyPolicies` field specifies whether policies matching this new topic should be applied to the message after redirection.

When multiple policies match a given topic, they are executed in the order of least specific to most specific. The topic filter `devices/+/+/status` is less specific than `devices/v2/+/status`, so the `all-device-statuses` policy will always execute before this `v2-device-statuses` policy. `all-device-statuses` only allows `v1-status-schema` and `v2-status-schema` schemas and filters out any other invalid messages before they can reach the next policy, so messages received for validation by `v2-device-statuses` will always be one of these two schemas. Because of this, if `v2-device-statuses` fails its validation, it must mean that the message conforms to `v1-status-schema` and so it can safely be redirected to `devices/v1/${clientId}/status`.

To upload the policy, run the following command:

```bash
curl -X POST --data @v2-status-policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies
```


### Listing policies

To see a list of the two policies that have been uploaded, run the following command:

```bash
curl -X GET http://localhost:8888/api/v1/data-validation/policies
```
