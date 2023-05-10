# HiveMQ Data Governance Hub Cookbooks

The HiveMQ Data Governance Hub provides mechanisms to define how MQTT data is handled in the HiveMQ broker. The first feature of our new Data Governance Hub is Data Validation.

> The HiveMQ Data Governance Hub data validation feature is currently available for testing in a closed beta version only. For more information or to request access to the closed beta, contact datagovernancehub@hivemq.com


In the HiveMQ Data Governance Hub, data validation implements a declarative policy that checks whether your data sources are sending data in the data format you expect.
This process ensures that the value of the data is assessed as early as possible in the data supply chain. Checks occur before your data reaches downstream devices or upstream services where costly validation must be handled by each subscribing client.

## Features
* Validate MQTT messages for JSON Schema or Protobuf
* Enforce policies along the entire MQTT topic tree structure
* Reroute valid and invalid MQTT messages to different topics based on the result of the data validation
* Increase the observability of bad clients with additional metrics and log statements

## Example Use-Cases
| Description                                                                       	                         | Data Format 	         | Link 	                                                                       |
|-------------------------------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------|
| A policy and schema that enforces that all incoming data packets are valid JSON.                            | JSON        	         | [simple-generic-json](/data-validation/simple-generic-json-schema)     	     |
| Multiple Protobuf policies on different topics for incoming sensor data                                     | Protobuf            	 | [multi-topic-sensor-protobuf](/data-validation/multi-topic-sensor-protobuf)	 |
| Accept multiple possible schemas on a single topic for location data                                        | JSON            	     | [multiple-coordinate-schemas](/data-validation/multiple-coordinate-schemas)	 |
| Ensure messages follow at least one version of a schema and redirect legacy versions to a different topic   | Protobuf            	 | [redirect-legacy-schema](/data-validation/redirect-legacy-schema)	           |
| Updating an existing policy to use a different schema                                                       | Protobuf              | [updating-protobuf-schema](/data-validation/updating-protobuf-schema)	       |
| A policy that enforces that incoming packets match multiple JSON schemas simultaneously                     | JSON                  | [multiple-required-json-schemas](/data-validation/multiple-required-json-schemas)	 |
