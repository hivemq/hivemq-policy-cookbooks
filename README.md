# HiveMQ Data Governance Hub

The HiveMQ Data Governance Hub provides mechanisms to define how MQTT data is handled in the HiveMQ broker.
The first feature of our new Data Governance Hub is *Data Validation*.

> NOTE: The HiveMQ Data Governance Hub data validation feature is currently available for testing in a closed beta version only. 
For more information or to request access to the closed beta, contact [datagovernancehub@hivemq.com](mailto:datagovernancehub@hivemq.com)

## Data Validation

In the HiveMQ Data Governance Hub, data validation implements a declarative
policy that checks whether your data sources are sending data in the data format
you expect. This process ensures that the value of the data is assessed at an
early stage in the data supply chain. To eliminate the need for subscribing
clients to perform resource-intensive validation, checks occur before your data
reaches downstream devices or upstream services.

## Features

* Validate MQTT messages with JSON Schema or Protobuf.
* Enforce policies across the entire MQTT topic tree structure.
* Reroute valid and invalid MQTT messages to different topics based on the data validation results.
* Increase the observability of client performance through additional metrics and log statements.

Our data validation functionality lets your development teams use the HiveMQ broker to automatically enforce a data validation strategy of their own design
(including fine-tuned control over how the broker handles incoming valid and invalid MQTT messages).

## Quick Start
For a quick start please conduct our HiveMQ Data Governance Hub documentation.

## Example Use-Cases
| Description                                                                       	                         | Data Format 	         | Link 	                                                                       |
|-------------------------------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------|
| A policy and schema that enforces that all incoming data packets are valid JSON.                            | JSON        	         | [simple-generic-json](/data-validation/simple-generic-json-schema)     	     |
| Multiple Protobuf policies on different topics for incoming sensor data                                     | Protobuf            	 | [multi-topic-sensor-protobuf](/data-validation/multi-topic-sensor-protobuf)	 |
| Accept multiple possible schemas on a single topic for location data                                        | JSON            	     | [multiple-coordinate-schemas](/data-validation/multiple-coordinate-schemas)	 |
| Ensure messages follow at least one version of a schema and redirect legacy versions to a different topic   | Protobuf            	 | [redirect-legacy-schema](/data-validation/redirect-legacy-schema)	           |
| Updating an existing policy to use a different schema                                                       | Protobuf              | [updating-protobuf-schema](/data-validation/updating-protobuf-schema)	       |
| A policy that enforces that incoming packets match multiple JSON schemas simultaneously                     | JSON                  | [multiple-required-json-schemas](/data-validation/multiple-required-json-schemas)	 |

## Versions
* since version 4.16: The release of HiveMQ Data Governance Hub 4.16 we will introduce some new features and breaking changes for string interpolation syntax. Moreover, we introduced namespacing for functions. For reference of the cookbooks for the 4.15 version please refer to the branch [4.15](https://github.com/hivemq/hivemq-policy-cookbooks/tree/4.15)