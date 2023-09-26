# Disconnect a client not sending general JSON data
This cookbook is about to disconnect a client when the message is published
is not JSON data at all.


<img alt="demo shell with MQTT CLI" style="filter: drop-shadow(2px 4px 6px black)" src="demo.gif">


### Use-case 
> As a developer, I want to disconnect all clients not sending correct JSON data, to have a clean data pipeline.

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

To upload this schema to the broker, run the following command:

```bash
mqtt hivemq schema create --id simple-generic-json --type json --file schema.json
```

This specifies the schema type (JSON) and assigns the unique identifier `simple-generic-json` to the schema.


### Policy

The next step is to apply the schema for all incoming MQTT messages by referencing the already defined schema `simple-generic-schema`.

The following policy specifies the validation step under the `topicFilter`: `#`. 
There are two outcomes of the validation `onSuccess` and `onFailure`:

* `onSuccess`: An MQTT User Property `"policy": "success"` is added to the MQTT message.
* `onFailure`: Logs a message with the `clientId` on level `WARN` and adds an MQTT User Property `"policy": "failed"`.

`policy.json`:
```json
{
  "id": "disconnect-clients-for-bad-data",
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
              "version": "latest"
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
          "level": "WARN",
          "message": "The client ${clientId} does not send JSON payloads to ${topic}. The client will be disconnected."
        }
      },
      {
        "id": "disconnectClient",
        "functionId": "Mqtt.disconnect",
        "arguments": {}
      }
    ]
  }
}
```

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq data-policy create --file policy.json
```

The policy is now applied and all incoming MQTT messages are subject to validation.

To delete the policy, run the following command:

```bash
mqtt hivemq data-policy delete --id disconnect-clients-for-bad-data
```
