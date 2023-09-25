# Updating a schema

This cookbook covers how to update a policy to use a newer version of a schema and different log messages.

### Use-case

> As a developer, I want to be able to update my Protobuf schema to a newer version and apply it to an existing policy
> in-place.

For this use-case, a policy and a schema which has been modified from its original form are needed.

### Find policy and schema identifiers

List existing policies in the broker with the following command:

```bash
mqtt hivemq data-policy list
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
                  "version": "1"
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
              "message": "The client with ID ${clientId} sent invalid data for schema version 1"
            }
          }
        ]
      }
    }
  ]
}
```

From this, note the `id` of the policy you wish to update and the `schemaId` of the schema it uses. Here the policy id
is `simple-policy` and the schema id is `simple-schema`.

### New schema

Create a new version of the schema by using the same `id`, `simple-schema`, as the current one. Use
the `--print-version` flag to see the version assigned to this new schema definition after creation:

```bash
mqtt hivemq schema create --id simple-schema --type protobuf --message-type SimpleMessage --file new-schema.proto --print-version
```

This returns a JSON response containing the version assigned to the newly uploaded schema, `2`:

```json
{
  "version": 2
}
```

### New policy

Next, update the policy, referencing the new version of the schema by setting the `version` field to `2`. Ensure that
the `message` field of the log operation also reflects the new schema version.

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
              "version": "2"
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
          "message": "The client with ID ${clientId} sent invalid data for schema version 2"
        }
      }
    ]
  }
}

```

To upload the new `policy.json` to the broker, run the following command:

```bash
mqtt hivemq data-policy update --id simple-policy --file policy.json
```
