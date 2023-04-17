# Simple JSON schema
This cookbook is about a very simple and generic use-case. 

## Use-Case 
> As a developer, I want to enforce that all MQTT payloads are published in a JSON format, to unify data payloads. I do not care about the actual JSON schema.

For this use-case, a `policy` and a `schema` is required. To begin with, consider the following plain JSON schema (according to [JSON Schema](https://json-schema.org/))

### Schema

`schema.json`:
```json
{
  "description": "This is the most generic JSON schema, since it requires just a JSON object, nothing further specified",
  "type": "object"
}
```
which simply specifies that the payload should be in a JSON format without specifying the actual fields.

To get this schema into the broker, the following request has to be made:

`schema-request.json`:
```json
{
  "id": "simple-generic-json",
  "type": "JSON",
  "schemaDefinition": "{\n  \"description\": \"This is the most generic JSON schema, since it requires just a JSON object, nothing further specified\",\n  \"type\": \"object\"\n}"
}
```
which embeds the schema definition, the type of schema (JSON) and the unique identifier `simple-generic-json`, that can be used for reference in the policy.

To upload the `schema-request.json` to the broker, run the following command: 
```bash
curl -X POST --data @schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/schemas
```
suppose your HiveMQ REST API runs at `http://localhost:8888`.

### Policy
The next step is to apply the schema for all incoming MQTT messages by referencing the already defined schema `simple-generic-schema`.

The following policy specifies the validation step under the `topicFilter`: `#`.  In case a MQTT message does not contain a valid JSON payload, a log message with level 'WARN' is printed with the `clientId`. 
`policy.json`:
```json
{
  "name": "simple-basic-json-policy-for-every-topic",
  "matching": {
    "topicFilter": "#"
  },
  "validation": {
    "schemaId": "simple-generic-json"
  },
  "onSuccess": {
    "continue": true
  },
  "onFailure": {
    "continue": false,
    "log": {
      "level": "WARN",
      "message": "The client with id $clientId does not send JSON payloads. The message will be dropped."
    }
  }
}
```

To upload the `policy.json` to the broker, run the following command:
```bash
curl -X POST --data @policy.json -H "Content-Type: application/json" http://localhost:8888/api/v1/policies
```

The policy is now applied and all incoming MQTT messages are subject to validation.

To delete the policy, run the following command:
```bash
curl -X DELETE -H "Content-Type: application/json" http://localhost:8888/api/v1/policies/simple-basic-json-policy-for-every-topic
```
