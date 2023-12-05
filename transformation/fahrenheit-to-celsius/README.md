# Convert Fahrenheit to Celsius
This cookbook is about transforming units.

<img alt="Transformation Demo: Fahrenheit to Celsius" style="filter: drop-shadow(2px 4px 6px black)" src="demo.gif">

### Use-case 
> As an OT developer, I have devices sending data in Fahrenheit, but the analytics services require temperature in Celsius.

For this use-case, a script, a policy, and a schema are required.

### Schema

To begin with, consider the following plain JSON schema (according to [JSON Schema](https://json-schema.org/)):

`schema-from-device.json`:
```json
{
  "properties":{
    "fahrenheit":{
      "type":"number"
    },
    "timestamp":{
      "type":"number"
    }
  },
  "required": [ "fahrenheit", "timestamp" ]
}
```
which contains two required fields `fahrenheit` and `timestamp` to be of type `number`.

After transformation, the field `fahrenheit` isn't available anymore. Rather, there is a new field `celsius`. The schema for transformed MQTT messages is define as follows:

`schema-for-fan.json`:
```json
{
  "properties":{
    "celsius":{
      "type":"number"
    },
    "timestamp":{
      "type":"number"
    }
  },
  "required": [ "celsius", "timestamp" ]
}
```

To upload the schemas to the broker, run the following command:

```bash
mqtt hivemq schema create --id schema-from-sensor --type json --file schema-from-sensor.json
mqtt hivemq schema create --id schema-for-fan --type json --file schema-for-fan.json
```

### Transformation function
In HiveMQ Data Hub from version 4.23 we support JavaScript to transform incoming MQTT 
messages. 

The following scripts converts Fahrenheit into Celsius:

```javascript
function convert(fahrenheit) {
    return Mah.floor((fahrenheit - 32) * 5/9);
}

function transform(publish, context) {
    publish.payload = {
        "celsius": convert(publish.payload.fahrenheit),
        "timestamp": publish.payload.timestamp
    }

    return publish;
}
```
The function `transform` has two parameters, a publish-object and a context-publish. A new
publish-object is create with the fields `celisus` convert from the field `fahrenheit` and the
original timestamp of the incoming publish.

The function is uploaded to the broker with the following command:

```basH
mqtt hivemq script create --id=fahrenheit-to-celsius --file=script.js --type=transformation
```

### Policy
The next step is to create a policy that validates against the `schema-from-sensor` schema, 
converts the unit by executing the transformation script and publishes the payload to the 
original topic.

`policy.json`:
```json
{
  "id" : "convert-fahrenheit-into-celsius",

  "matching" : {
    "topicFilter" : "factory/#"
  },
  "validation" : {
    "validators" : [ {
      "type" : "schema",
      "arguments" : {
        "strategy" : "ALL_OF",
        "schemas" : [ {
          "schemaId" : "schema-from-sensor",
          "version" : "latest"
        } ]
      }
    } ]
  },
  "onSuccess": {
    "pipeline": [
      {
        "id": "operation-2eng0",
        "functionId": "Serdes.deserialize",
        "arguments": {
          "schemaVersion": "latest",
          "schemaId": "schema-from-sensor"
        }
      },
      {
        "id": "operation-ek2Mx",
        "functionId": "fn:fahrenheit-to-celsius:latest",
        "arguments": {}
      },
      {
        "id": "operation-4DBF3",
        "functionId": "Serdes.serialize",
        "arguments": {
          "schemaVersion": "latest",
          "schemaId": "schema-for-fan"
        }
      }
    ]
  },
  "onFailure" : {
    "pipeline" : [ {
      "id" : "operation-aMNNx",
      "functionId" : "Mqtt.drop",
      "arguments" : {
        "reasonString" : "Your client ${clientId} sent invalid data according to the schema: ${validationResult}."
      }
    } ]
  }
}
```

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq data-policy create --file policy.json
```

The policy is now applied and all incoming MQTT messages are subject to validation. In case the
validation is successful the transformation script to convert the unit is executed such that 
consumer only read celsius.

