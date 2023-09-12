# HiveMQ Data Hub

The HiveMQ Data Hub provides mechanisms to define how MQTT data is handled in the HiveMQ broker.
The first feature of our new Data Hub is *Data Validation*.

> NOTE: The HiveMQ Data Hub data validation feature is currently available as Early Access Preview (EAP)
> version only.
> For more information on the terms and conditions of the EAP offering,
> contact [sales@hivemq.com](mailto:sales@hivemq.com).

## Data Validation

In the HiveMQ Data Hub, data validation implements a declarative
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

Our data validation functionality lets your development teams use the HiveMQ broker to automatically enforce a data
validation strategy of their own design (including fine-tuned control over how the broker handles incoming valid and
invalid MQTT messages).

## Quick Start

For a quick start please consult our HiveMQ Data Hub documentation.

## Setup

To follow along with the example use-cases, the `mqtt` command line utility is required.
See [here](https://hivemq.github.io/mqtt-cli/docs/installation/) for installation and usage instructions.

By default, this will connect to a HiveMQ broker REST API running at http://localhost:8888. To configure this URL, use
the `--url` command line option with any of the policy and schema commands.

## Example Use-Cases

| Description                                                                       	                       | Data Format 	         | Link 	                                                                             |
|-----------------------------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------------|
| A policy and schema that enforces that all incoming data packets are valid JSON.                          | JSON        	         | [simple-generic-json](/data-validation/simple-generic-json-schema)     	           |
| Multiple Protobuf policies on different topics for incoming sensor data                                   | Protobuf            	 | [multi-topic-sensor-protobuf](/data-validation/multi-topic-sensor-protobuf)	       |
| Accept multiple possible schemas on a single topic for location data                                      | JSON            	     | [multiple-coordinate-schemas](/data-validation/multiple-coordinate-schemas)	       |
| Ensure messages follow at least one version of a schema and redirect legacy versions to a different topic | Protobuf            	 | [redirect-legacy-schema](/data-validation/redirect-legacy-schema)	                 |
| Updating an existing policy to use a new schema version                                                   | Protobuf              | [updating-protobuf-policy](/data-validation/updating-protobuf-policy)	             |
| A policy that enforces that incoming packets match multiple JSON schemas simultaneously                   | JSON                  | [multiple-required-json-schemas](/data-validation/multiple-required-json-schemas)	 |

## Complete Demo Setups

| Description                                                                       	                                                                                                                                                                                                                                                               | Link 	                                                           |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| The demo showcases how to derive a quality metric from schema validations and visualize it in Grafana. The [Prometheus Monitoring Extension](https://www.hivemq.com/extension/prometheus-extension/) is used to gather metrics from the HiveMQ Broker                                                                                             | [quality-metric-example](/examples/quality-metric-example)     	 |
| The demo shows how to flag clients that sending invalid messages wrt. a schema (bad clients). Moreover, it also stores invalid messages using the [HiveMQ Enterprise Extension for PostgreSQL](https://www.hivemq.com/extension/postgresql-extension/) for further inspection. As a result a Grafana dashboard shows the top most 10 bad clients. | [flagging-bad-clients](/examples/flagging-bad-clients)     	     |

## Versions

* since version 4.16: The release of HiveMQ Data Hub 4.16 will introduce some new features and breaking
  changes for string interpolation syntax. Moreover, we introduced namespacing for functions. For reference of the
  cookbooks for the 4.15 version please refer to the
  branch [4.15](https://github.com/hivemq/hivemq-policy-cookbooks/tree/4.15)