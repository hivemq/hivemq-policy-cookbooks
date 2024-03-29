# HiveMQ Data Hub

The HiveMQ Data Hub provides mechanisms to define how MQTT data is handled in the HiveMQ Enterprise Edition and HiveMQ Edge.

## Quick Start

For a quick start please consult our [HiveMQ Data Hub documentation](https://docs.hivemq.com/hivemq/latest/data-hub/quick-start).

## Setup

To follow along with the example use-cases, the `mqtt` command line utility is required.
See [here](https://hivemq.github.io/mqtt-cli/docs/installation/) for installation and usage instructions.

By default, this will connect to a HiveMQ broker REST API running at http://localhost:8888. To configure this URL, use
the `--url` command line option with any of the policy and schema commands.

## Data Validation

In the HiveMQ Data Hub, data validation implements a declarative
policy that checks whether your data sources are sending data in the data format
you expect. This process ensures that the value of the data is assessed at an
early stage in the data supply chain. To eliminate the need for subscribing
clients to perform resource-intensive validation, checks occur before your data
reaches downstream devices or upstream services.

### Features

* Validate MQTT messages with JSON Schema or Protobuf.
* Enforce policies across the entire MQTT topic tree structure.
* Reroute valid and invalid MQTT messages to different topics based on the data validation results.
* Increase the observability of client performance through additional metrics and log statements.

Our data validation functionality lets your development teams use the HiveMQ broker to automatically enforce a data
validation strategy of their own design (including fine-tuned control over how the broker handles incoming valid and
invalid MQTT messages).

### Example Use-Cases

| Description                                                                       	                       | Data Format 	         | Link 	                                                                             |
|-----------------------------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------------|
| A policy and schema that enforces that all incoming data packets are valid JSON.                          | JSON        	         | [simple-generic-json](/data-validation/simple-generic-json-schema)     	           |
| Multiple Protobuf policies on different topics for incoming sensor data                                   | Protobuf            	 | [multi-topic-sensor-protobuf](/data-validation/multi-topic-sensor-protobuf)	       |
| Accept multiple possible schemas on a single topic for location data                                      | JSON            	     | [multiple-coordinate-schemas](/data-validation/multiple-coordinate-schemas)	       |
| Ensure messages follow at least one version of a schema and redirect legacy versions to a different topic | Protobuf            	 | [redirect-legacy-schema](/data-validation/redirect-legacy-schema)	                 |
| Updating an existing policy to use a new schema version                                                   | Protobuf              | [updating-protobuf-policy](/data-validation/updating-protobuf-policy)	             |
| A policy that enforces that incoming packets match multiple JSON schemas simultaneously                   | JSON                  | [multiple-required-json-schemas](/data-validation/multiple-required-json-schemas)	 |
| Debug bad clients by dropping valid traffic | JSON |  [debug-bad-clients](data-validation/debug-bad-clients) |
| Disconnect client that sends bad data | JSON | [disconnect-client-for-invalid-data](data-validation/disconnect-client-for-invalid-data)
| Compute temperature range and adds state | JSON | [edge-temperature-values-via-arguments](edge-examples/value-via-arguments)

### Complete Demo Setups

| Description                                                                       	                                                                                                                                                                                                                                                               | Link 	                                                           |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| The demo showcases how to derive a quality metric from schema validations and visualize it in Grafana. The [Prometheus Monitoring Extension](https://www.hivemq.com/extension/prometheus-extension/) is used to gather metrics from the HiveMQ Broker                                                                                             | [quality-metric-example](/examples/quality-metric-example)     	 |
| The demo shows how to flag clients that sending invalid messages wrt. a schema (bad clients). Moreover, it also stores invalid messages using the [HiveMQ Enterprise Extension for PostgreSQL](https://www.hivemq.com/extension/postgresql-extension/) for further inspection. As a result a Grafana dashboard shows the top most 10 bad clients. | [flagging-bad-clients](/examples/flagging-bad-clients)     	     |

## Behavior Validation

In the HiveMQ Data Hub, behavior validation implements a declarative
policy that maintains a state between validation invocations. This allows to have counters, sliding windows, histories of past messages - all those validation scenarios that spans across multiple messages.

### Example Use-Cases
| Description                                                                       	    | Link 	                                                                 |
|----------------------------------------------------------------------------------------|------------------------------------------------------------------------|
| A policy that enforces a specified amount of PUSLISH messages within a client session. | [publish-quota](/behavior-validation/publish-quota)     	              |
| A policy that detects duplicated messages.                                             | [publish-duplicate](/behavior-validation/publish-duplicate)	 |

## Data Transformation

In the HiveMQ Data Hub, data transformation provides a way to transform MQTT messages to implement conversions, data
repairs, and other data transformations.

### Example Use-Cases

| Description                                                                       	 | Link 	                                                               |
|-------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| Fahrenheit to Celsius temperature readings conversion.                              | [fahrenheit-to-celsius](/transformation/fahrenheit-to-celsius)     	 |
| Voltage readings normalization.                                                     | [voltage-normalization](/transformation/voltage-normalization)	      |
| Sensitive personal data anonymization.                                              | [data-anonymization](/transformation/data-anonymization)	            |