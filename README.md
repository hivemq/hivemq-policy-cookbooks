# hivemq-policy-cookbooks

Collection of user-stories and polices for data governance.

| Description                                                                       	 | Data Format 	      | Link 	                                                                       |
|-------------------------------------------------------------------------------------|--------------------|------------------------------------------------------------------------------|
| A policy and schema that enforces that all incoming data packets are valid JSON.    | JSON        	      | [simple-generic-json](/data-validation/simple-generic-json-schema)     	     |
| Multiple Protobuf schemas on different topics for incoming sensor data              | Protobuf            	 | [multi-topic-sensor-protobuf](/data-validation/multi-topic-sensor-protobuf)	 |
| Log all incoming packets that contain location coordinates from within a region     | JSON            	  | [log-all-with-field](/data-validation/log-all-with-field)	                   |
| Updating an existing policy to use a different schema                               | Protobuf       | [updating-protobuf-schema](/data-validation/updating-protobuf-schema)	                |
