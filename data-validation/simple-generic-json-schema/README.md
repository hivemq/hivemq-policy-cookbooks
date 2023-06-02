# Simple JSON schema
This cookbook is about a very simple and generic use-case. 


### Use-case 
> As a developer, I want to enforce that all MQTT payloads are published in a JSON format, to unify data payloads. I do not care about the actual JSON schema.

For this use-case, a policy and a schema are required.


### Schema

To begin with, consider the following plain JSON schema (according to [JSON Schema](https://json-schema.org/)):

`schema.json`:
```json
{
  "description": "This is the most generic JSON schema, since it requires just a JSON object, nothing further specified",
  "type": "object"
}
```

which simply specifies that the payload should be in a JSON format without specifying the actual fields.

Convert `schema.json` to a Base64 string with the following command:

```bash
base64 -i schema.json
```

To get this schema into the broker, the following request has to be made:

`schema-request.json`:
```json
{
  "id": "simple-generic-json",
  "type": "JSON",
  "schemaDefinition": "ewogICJkZXNjcmlwdGlvbiI6ICJUaGlzIGlzIGEgdGhlIG1vc3QgZ2VuZXJpYyBKU09OIHNjaGVtYSwgc2luY2UgaXQgcmVxdWlyZXMganVzdCBhIEpTT04sIG5vdGhpbmcgZnVydGhlciBzcGVjaWZpZWQiLAogICJ0eXBlIjogIm9iamVjdCIKfQ=="
}
```

which embeds the schema definition, the type of schema (JSON) and the unique identifier, `simple-generic-json`, that can be used for reference in the policy.

To upload `schema-request.json` to the broker, run the following command: 

```bash
curl -X POST --data @schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas
```

suppose your HiveMQ REST API runs at `http://localhost:8888`.


### Policy
The next step is to apply the schema for all incoming MQTT messages by referencing the already defined schema `simple-generic-schema`.

The following policy specifies the validation step under the `topicFilter`: `#`. There are two outcomes of the validation `onSuccess` and `onFailure`:

* `onSuccess`: an MQTT User Property `"policy": "success"` is added the MQTT message
* `onFailure`: Logs a message with the `clientId` on level `WARN` and adds an MQTT User Property `"policy": "failed"`.

`policy.json`:
```json
{
  "id": "simple-basic-json-policy-for-every-topic",
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
              "schemaId": "simple-generic-json",
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
        "id": "flagSchemaChecked",
        "functionId": "UserProperties.add",
        "arguments": {
          "name": "policy",
          "value": "success"
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
          "message": "The client ${clientId} does not send JSON payloads. The message will be dropped."
        }
      },
      {
        "id": "flagSchemaChecked",
        "functionId": "UserProperties.add",
        "arguments": {
          "name": "policy",
          "value": "failed"
        }
      }
    ]
  }
}

```

To upload `policy.json` to the broker, run the following command:
```bash
curl -X POST --data @policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies
```

The policy is now applied and all incoming MQTT messages are subject to validation.

To delete the policy, run the following command:

```bash
curl -X DELETE -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies/simple-basic-json-policy-for-every-topic
```
