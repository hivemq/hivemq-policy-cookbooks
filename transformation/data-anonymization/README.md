# Anonymize Personal Data
This cookbook is about data anonymization.

### Use-case
> As an OT developer, I have devices sending personal data, but the downstream analytics service require anonymized data to conform to legal requirements.

For this use-case, a script, a policy, and a schema are required.

### Schema

To begin with, consider the following plain JSON schema (according to [JSON Schema](https://json-schema.org/)):

`schema.json`:
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "surname": {
      "type": "string"
    },
    "dateOfBirth": {
      "type": "string",
      "format": "date"
    },
    "address": {
      "type": "object",
      "properties": {
        "street": {
          "type": "string"
        },
        "city": {
          "type": "string"
        },
        "zipCode": {
          "type": "string"
        },
        "country": {
          "type": "string"
        }
      },
      "required": ["street", "city", "zipCode", "country"]
    }
  },
  "required": [
    "name",
    "surname",
    "dateOfBirth",
    "address"
  ]
}
```

To upload the schema to the broker, run the following command:

```bash
mqtt hivemq schema create --id schema-person --type json --file schema.json
```

### Transformation function
In HiveMQ Data Hub from version 4.23 we support JavaScript to transform incoming MQTT 
messages. 

The following scripts masks the middle of the surname, extracts the year from the date of birth, and replaces the street
and zip code with a placeholder:

```javascript
function maskString(inputString) {
    if (inputString.length <= 2) {
        return inputString;
    }

    const firstChar = inputString.charAt(0);
    const lastChar = inputString.charAt(inputString.length - 1);

    const maskedChars = '*'.repeat(inputString.length - 2);

    const maskedString = firstChar + maskedChars + lastChar;

    return maskedString;
}

function extractYearFromDate(dateString) {
    const year = dateString.split('-')[0];
    return `${year}-01-01`;
}

function transform(publish, context) {
    publish.payload = {
        "name": publish.payload.name,
        "surname": maskString(publish.payload.surname),
        "dateOfBirth": extractYearFromDate(publish.payload.dateOfBirth),
        "address": {
            "street": "[REDACTED]",
            "city": publish.payload.address.city,
            "zipCode": "[REDACTED]",
            "country": publish.payload.address.country
        }
    }

    return publish;
}
```
The function `transform` has two parameters, a publish-object and a context-publish. A new
publish-object is created with the sensitive fields masked or removed.

The function is uploaded to the broker with the following command:

```basH
mqtt hivemq script create --id=script-anonymize --file=script.js --type=transformation
```

### Policy
The next step is to create a policy that validates against the `schema-person` schema, 
anonymizes the data by executing the transformation script and publishes the payload to the original topic.

`policy.json`:
```json
{
  "id": "person-anonymization",
  "matching": {
    "topicFilter": "person/#"
  },
  "validation": {
    "validators": [
      {
        "type": "schema",
        "arguments": {
          "strategy": "ALL_OF",
          "schemas": [
            {
              "schemaId": "schema-person",
              "version": "latest"
            }
          ]
        }
      }
    ]
  },
  "onSuccess": {
    "pipeline": [
      {
        "id": "operation-2eng0",
        "functionId": "Serdes.deserialize",
        "arguments": {
          "schemaVersion": "latest",
          "schemaId": "schema-person"
        }
      },
      {
        "id": "operation-ek2Mx",
        "functionId": "fn:script-anonymize:latest",
        "arguments": {}
      },
      {
        "id": "operation-4DBF3",
        "functionId": "Serdes.serialize",
        "arguments": {
          "schemaVersion": "latest",
          "schemaId": "schema-person"
        }
      }
    ]
  },
  "onFailure": {
    "pipeline": [
      {
        "id": "operation-aMNNx",
        "functionId": "Mqtt.drop",
        "arguments": {
          "reasonString": "Your client ${clientId} sent invalid data according to the schema: ${validationResult}."
        }
      }
    ]
  }
}
```

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq data-policy create --file policy.json
```

The policy is now applied and all incoming MQTT messages matching the topic filter `person/#` are subject to validation.
When validation for an incoming message is successful, the transformation script to anonymize the data is executed and the
resulting payload is published to the original topic.

Below is an example of an incoming message and the resulting outgoing anonymized message.

Original data before anonymization:
```json
{
  "name": "Martin",
  "surname": "McFly",
  "dateOfBirth": "1986-05-02",
  "address": {
    "street": "9303 Lyon Drive",
    "city": "Hill Valley",
    "zipCode": "95420",
    "country": "USA"
  }
}
```

Anonymized data after transformation:
```json
{
  "name": "Martin",
  "surname": "M***y",
  "dateOfBirth": "1986-01-01",
  "address": {
    "zipCode": "[REDACTED]",
    "country": "USA",
    "city": "Hill Valley",
    "street": "[REDACTED]"
  }
}
```