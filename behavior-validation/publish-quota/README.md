# Disconnect a client sending amount of messages outside of the specified range
This cookbook is about to disconnect a client when the amount of published messages is outside the specified range.


### Use-case
> As a developer, I want to disconnect all clients not sending correct amount of messages.

For this use-case, a behavior policy is required.


### Policy

Consider the following behavior policy that disconnects a client when the amount of published messages is more than 10.

This policy uses `System.log` function to log explanatory messages on each state transition and `Mqtt.disconnect` function to disconnect a client if message count goest above 10.

`policy.json`:
```json
{
  "id": "max10",
  "matching": {
    "clientIdRegex": ".*"
  },
  "behavior": {
    "id": "Publish.quota",
    "arguments": {
      "minPublishes": 0,
      "maxPublishes": 10
    }
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
              "message": "Ok, we've got a client connected. Waiting for a first PUBLISH message to start counting messages."
            }
          }
        ]
      }
    },
    {
      "fromState": "Connected",
      "toState": "Publishing",
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
              "message": "And here is the first PUBLISH message. It was counted."
            }
          }
        ]
      }
    },
    {
      "fromState": "Publishing",
      "toState": "Publishing",
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
              "message": "One more message was counted."
            }
          }
        ]
      }
    },
    {
      "fromState": "Any.*",
      "toState": "Violated",
      "Mqtt.OnInboundPublish": {
        "pipeline": [
          {
            "id": "logFunction",
            "functionId": "System.log",
            "arguments": {
              "level": "WARN",
              "message": "Behavior policy ${policyId}: ${clientId} transitioned from ${fromState} to ${toState} on ${triggerEvent} at ${timestamp}"
            }
          },
          {
            "id": "logFunctionTransitionDebug",
            "functionId": "System.log",
            "arguments": {
              "level": "WARN",
              "message": "Ok, we had enough messages! ${clientId} will now be disconnected."
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
mqtt hivemq behavior-policy delete --id max10
```


### Policy output

The abundant use of `System.log` in the policy produces a log output that facilitates understanding of the policy's behavior.

```text
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Initial to Connected on MQTT - Inbound CONNECT at 1696972060994
INFO  - Ok, we've got a client connected. Waiting for a first PUBLISH message to start counting messages.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Connected to Publishing on MQTT - Inbound PUBLISH at 1696972068694
INFO  - And here is the first PUBLISH message. It was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972076567
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972077619
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972078673
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972079648
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972080573
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972081522
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972082525
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972084614
INFO  - One more message was counted.
INFO  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Publishing on MQTT - Inbound PUBLISH at 1696972085653
INFO  - One more message was counted.
WARN  - Behavior policy max10: hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 transitioned from Publishing to Violated on MQTT - Inbound PUBLISH at 1696972086637
WARN  - Ok, we had enough messages! hmq_hqIfS_1_8aad39794e58fb849f2608750600ef27 will no be disconnected.
```