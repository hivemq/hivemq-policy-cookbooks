# hivemq-policy-cookbooks

Collection of user-stories and polices for data governance.

| Description                                                                       	                         | Data Format 	         | Link 	                                                                       |
|-------------------------------------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------|
| A policy and schema that enforces that all incoming data packets are valid JSON.                            | JSON        	         | [simple-generic-json](/data-validation/simple-generic-json-schema)     	     |
| Multiple Protobuf policies on different topics for incoming sensor data                                     | Protobuf            	 | [multi-topic-sensor-protobuf](/data-validation/multi-topic-sensor-protobuf)	 |
| Accept multiple possible schemas on a single topic for location data                                        | JSON            	     | [multiple-coordinate-schemas](/data-validation/multiple-coordinate-schemas)	 |
| Ensure messages follow at least one version of a schema and redirect legacy versions to a different topic   | Protobuf            	 | [redirect-legacy-schema](/data-validation/redirect-legacy-schema)	           |
| Updating an existing policy to use a different schema                                                       | Protobuf              | [updating-protobuf-schema](/data-validation/updating-protobuf-schema)	       |
| A policy that enforces that incoming packets match multiple JSON schemas simultaneously                     | JSON                  | [multiple-required-json-schemas](/data-validation/multiple-required-json-schemas)	 |
