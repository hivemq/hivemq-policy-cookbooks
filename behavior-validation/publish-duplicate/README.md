# Disconnect a client sending duplicate messages

This cookbook is about disconnecting a client when it sends a PUBLISH message identical to the previous one it sent.


### Use-case
> As a developer, I want to disconnect all clients that send duplicate messages.

For this use-case, a behavior policy is required.


### Policy

Consider the following behavior policy that disconnects a client if the received published message has an identical payload and topic to the previous one.

This policy uses `System.log` function to log explanatory messages on each state transition and `Mqtt.disconnect` function to disconnect a client if message count goest above 10.

`policy.json`:
```json
{
  "id": "duplicate-policeman",
  "matching": {
    "clientIdRegex": ".*"
  },
  "behavior": {
    "id": "Publish.duplicate",
    "arguments": {}
  },
  "onTransitions": [
    {
      "fromState": "Initial",
      "toState": "Connected",
      "Mqtt.OnInboundConnect": {
        "pipeline": [
          {
            "id": "logFunctionTransitionDebug",
            "functionId": "System.log",
            "arguments": {
              "level": "INFO",
              "message": "Behavior policy ${policyId}: ${clientId} transitioned from ${fromState} to ${toState} on ${triggerEvent} at ${timestamp}"
            }
          },
          {
            "id": "logFunctionExplanationMessage",
            "functionId": "System.log",
            "arguments": {
              "level": "INFO",
              "message": "Ok, we've got a client connected. Waiting for a first PUBLISH message to start detecting duplicates."
            }
          }
        ]
      }
    },
    {
      "fromState": "Connected",
      "toState": "NotDuplicated",
      "Mqtt.OnInboundPublish": {
        "pipeline": [
          {
            "id": "logFunctionTransitionDebug",
            "functionId": "System.log",
            "arguments": {
              "level": "INFO",
              "message": "Behavior policy ${policyId}: ${clientId} transitioned from ${fromState} to ${toState} on ${triggerEvent} at ${timestamp}"
            }
          },
          {
            "id": "logFunctionExplanationMessage",
            "functionId": "System.log",
            "arguments": {
              "level": "INFO",
              "message": "And here is the first PUBLISH message. From now on we are detecting duplicates."
            }
          }
        ]
      }
    },
    {
      "fromState": "NotDuplicated",
      "toState": "Duplicated",
      "Mqtt.OnInboundPublish": {
        "pipeline": [
          {
            "id": "logFunctionTransitionDebug",
            "functionId": "System.log",
            "arguments": {
              "level": "INFO",
              "message": "Behavior policy ${policyId}: ${clientId} transitioned from ${fromState} to ${toState} on ${triggerEvent} at ${timestamp}"
            }
          },
          {
            "id": "logFunctionExplanationMessage",
            "functionId": "System.log",
            "arguments": {
              "level": "WARN",
              "message": "Duplicate message detected! ${clientId} will be disconnected!"
            }
          },
          {
            "id": "disconnectFunction",
            "functionId": "Mqtt.disconnect",
            "arguments": {}
          }
        ]
      }
    }
  ]
}
```

To upload `policy.json` to the broker, run the following command:

```bash
mqtt hivemq behavior-policy create --file policy.json
```

The policy is now applied and all incoming MQTT messages are subject to validation.

To delete the policy, run the following command:

```bash
mqtt hivemq behavior-policy delete --id duplicate-policeman
```


### Policy output

The abundant use of `System.log` in the policy produces a log output that facilitates understanding of the policy's behavior.

```text
INFO  - Behavior policy duplicate-policeman: hmq_hqIfS_2_c1834f9bdabbe47be40935e059a3855a transitioned from Initial to Connected on MQTT - Inbound CONNECT at 1696975327144
INFO  - Ok, we've got a client connected. Waiting for a first PUBLISH message to start detecting duplicates.
INFO  - Behavior policy duplicate-policeman: hmq_hqIfS_2_c1834f9bdabbe47be40935e059a3855a transitioned from Connected to NotDuplicated on MQTT - Inbound PUBLISH at 1696975359963
INFO  - And here is the first PUBLISH message. From now on we are detecting duplicates.
INFO  - Behavior policy duplicate-policeman: hmq_hqIfS_2_c1834f9bdabbe47be40935e059a3855a transitioned from NotDuplicated to Duplicated on MQTT - Inbound PUBLISH at 1696975363526
INFO  - Duplicate message detected! hmq_hqIfS_2_c1834f9bdabbe47be40935e059a3855a will be disconnected!
```