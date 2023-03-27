# Simple JSON schema
This cookbook is about a very simple and generic use-case. 

## Use-Case 
> As a developer, I want to enforce that all MQTT payloads are published in a JSON format, to unify data payloads. I actually, do not care about the actually JSON schema.

For this use-case, a `policy` and a `schema` is required. To begin with, consider the following plain JSON schema (according to [JSON Schema](https://json-schema.org/))

### Schema

`schema.json`:
```json
{
  "description": "This is a the most generic JSON schema, since it requires just a JSON, nothing further specified",
  "type": "object"
}
```
which simply specify that the payload should be in a JSON format without specify the actual fields.

To get this schema into the broker, the following request has to made:

`schema-request.json`:
```json
{
  "id": "simple-generic-json",
  "type": "JSON",
  "schemaDefinition": "{\n  \"description\": \"This is a the most generic JSON schema, since it requires just a JSON, nothing further specified\",\n  \"type\": \"object\"\n}"
}
```
which embeds the schema definition, the type of schema (JSON) and the unique identifier `simple-generic-json`, that can be used for reference in the policy.

To upload the `schema-request.json` to the broker, run the following command: 
```bash
curl -X POST --data @schema-request.json -H "Content-Type: application/json` http://localhost:8888/api/v1/schemas
```
suppose your HiveMQ REST API runs at `http://localhost:8888`.

### Policy
The next step is to apply the schema for all incoming MQTT messages by referencing the already defined schema `simple-generic-schema`.

The following policy, specifies the validation step under the `topicFilter`: `#`.  In case a MQTT message isn't a valid JSON payload, a log message with level 'WARN' is printed with the `clientId`. 
```json
{
  "name": "simple-basic-json-schema-for-every-topic",
  "matching":{
    "topicFilter": "#"
  },
  "validation": {
    "schemaId": "simple-generic-json"
  },
  "onFailure": {
    "log": {
      "level": "WARN",
      "message": "The client with $clientid does no send JSON payloads. Skipping..."
    }
  }
}
```


