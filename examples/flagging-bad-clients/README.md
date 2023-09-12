# Flagging Bad Clients
![](screenshot.png)


This repository showcases to flag clients that publishes bad data. 
The code exemplifies a scenario where clients publish data in a prescribed JSON format, but certain messages fail validation. 
The solution incorporates the [UserProperties.add](https://docs.hivemq.com/hivemq/latest/data-hub/policies.html#user-properties-add-function)
and [Delivery.redirectTo](https://docs.hivemq.com/hivemq/latest/data-hub/policies.html#delivery-redirect-to-function)
functions to add MQTT user properties and redirect invalid messages.
To each redirected message we add user properties to identify bad clients and to analyze the failure.

## Requirements
- [Docker](https://www.docker.com/) 
- [Docker compose](https://docs.docker.com/compose/) 
- A HiveMQ license with enabled Data Hub (contact [sales@hivemq.com](mailto:sales@hivemq.com))
- A [HiveMQ Enterprise Extension for PostgreSQL](https://www.hivemq.com/extension/postgresql-extension/) license. If no license is provided, a trial license is valid for 5 hours.
- Optional: 
  - (**License**): If you have a HiveMQ license with Data Hub copy the file into the container. Check the commented line in `docker-compose.yml` 
  - (**Non-License**): In case you don't have a license, the trial mode is activated which stays active for 5 hours. Check out the [documentation](https://docs.hivemq.com/hivemq/latest/data-hub/#activate-trial-mode) how to activate the trial mode.
 

## Quickstart

1. Execute `docker compose up`
2. Execute `mqtt sub -t 'invalid/#' -J` to see redirected MQTT messages from bad clients
3. Go to http://localhost:3000 and open the pre-defined Grafana Dashboard (credentials: admin, grafana)