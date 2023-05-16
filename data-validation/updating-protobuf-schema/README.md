# Updating a schema
This cookbook covers how to update a policy to use a different schema.


### Use-case 
> As a developer, I want to be able to modify the schema in an existing policy to use a more recent version.

For this use-case, an existing policy and schema must be deleted and new versions uploaded to the broker.


### Find policy and schema identifiers

List existing policies in the broker with the following command:

```bash
curl -X GET http://localhost:8888/api/v1/data-validation/policies
```

suppose your HiveMQ REST API runs at `http://localhost:8888`.

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
                  "schemaId": "simple-schema"
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
            "id": "logFailiure",
            "functionId": "log",
            "arguments": {
              "level": "WARN",
              "message": "The client with ID $clientId sent invalid data"
            }
          }
        ]
      }
    }
  ]
}
```

From this, take the `id` of the policy you wish to update and the `schemaId` of the schema it uses.


### Delete the old policy and schema

Because the existing policy references the existing schema, the policy first must be deleted before the schema can be deleted.

Delete the policy by running the following command:

```bash
curl -X DELETE -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/policies/simple-policy
```

Then delete the schema by running the following command:

```bash
curl -X DELETE -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas/simple-schema
```


### New schema

Now a new schema can be uploaded using the same `id`, `simple-schema`, as the previous one:

`new-schema-request.json`:
```json
{
  "id": "simple-schema",
  "type": "PROTOBUF",
  "schemaDefinition": "Co4BChBuZXctc2NoZW1hLnByb3RvEhFpby5oaXZlbXEuZXhhbXBsZSJfCg1TaW1wbGVNZXNzYWdlEiEKDHN0b3JhZ2VfdXNlZBgBIAEoA1ILc3RvcmFnZVVzZWQSKwoRc3RvcmFnZV9hdmFpbGFibGUYAiABKANSEHN0b3JhZ2VBdmFpbGFibGViBnByb3RvMw==",
  "arguments": {
    "messageType": "SimpleMessage",
    "allowUnknownFields": "false"
  }
}
```

To upload `new-schema-request.json` to the broker, run the following command:

```bash
curl -X POST --data @new-schema-request.json -H "Content-Type: application/json" http://localhost:8888/api/v1/data-validation/schemas
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
              "schemaId": "simple-schema"
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
        "functionId": "log",
        "arguments": {
          "level": "WARN",
          "message": "The client with ID $clientId sent invalid data"
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
