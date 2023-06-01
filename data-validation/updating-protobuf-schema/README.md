# Updating a schema
This cookbook covers how to update a policy to use a different schema.


### Use-case 
> As a developer, I want to be able to modify the schema in an existing policy to use a more recent version.

For this use-case, an existing policy and schema must be deleted and new versions uploaded to the broker.


### Find policy and schema identifiers

List existing policies in the broker with the following command:

```bash
mqtt hivemq policies list
```

This returns a JSON response containing details of all existing policies in the broker:

`list-policies-response.json`:
```json
{
  "items": [
    {
      "id": "simple-policy",
      "createdAt": "2023-05-01T12:00:00.000Z",
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
                  "schemaId": "simple-schema",
                  "version" : "latest"
                }
              ]
            }
          }
        ]
      },
      "onSuccess": {
        "pipeline": []
      },
      "onFailure": {
        "pipeline": [
          {
            "id": "logFailure",
            "functionId": "System.log",
            "arguments": {
              "level": "WARN",
              "message": "The client with ID ${clientId} sent invalid data"
            }
          }
        ]
      }
    }
  ]
}
```

From this, take the `id` of the policy you wish to update and the `schemaId` of the schema it uses.  Here the policy id is `simple-policy` and the schema id is `simple-schema`.


### Delete the old policy and schema

Because the existing policy references the existing schema, the policy first must be deleted before the schema can be deleted.

Delete the policy by running the following command:

```bash
mqtt hivemq policies delete --id simple-policy
```

Then delete the schema by running the following command:

```bash
mqtt hivemq schemas delete --id simple-schema
```


### New schema

Now a new schema can be created using the same `id`, `simple-schema`, as the previous one:

```bash
mqtt hivemq schemas create --id simple-schema --type protobuf --message-type SimpleMessage --file new-schema.desc
```

### New policy

Next, re-upload the previously deleted policy to the broker as-is. The `schemaId` field for the schema it uses can remain the same because the new schema re-uses the old ID.

`policy.json`:
```json
{
  "id": "simple-policy",
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
              "schemaId": "simple-schema",
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
        "id": "logFailiure",
        "functionId": "System.log",
        "arguments": {
          "level": "WARN",
          "message": "The client with ID ${clientId} sent invalid data"
        }
      }
    ]
  }
}

```

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq policies create --file policy.json
```
