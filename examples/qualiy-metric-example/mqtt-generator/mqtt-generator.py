import random
import string
import time
import json
import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "127.0.0.1"
broker_port = 1883
topic = "mqtt/demo"
connected = False

cutting_machine_ids = set()
cleaning_machine_ids = set()
for i in range(100):
    cutting_machine_ids.add("clean-" + ''.join(random.choice(string.ascii_letters) for _ in range(10)))
    cleaning_machine_ids.add("cut-" + ''.join(random.choice(string.ascii_letters) for _ in range(10)))

def random_cutting_machine_message():
    message = {
        "id": random.choice(list(cutting_machine_ids)),
        "type": "cutting-machine",
        "version": random.choice(["1", "2", "3", "4", 4.5, "5"]),
        "timestamp": time.time(),
        "value": {
            "pressure": str(random.randint(0, 4000)) + "psi",
            "packml_state": "EXECUTE"
        }
    }
    return json.dumps(message)

def random_cleaning_machine_message():
    message = {
        "id": random.choice(list(cleaning_machine_ids)),
        "type": "cleaning-machine",
        "version": random.choice(["1", "2", "3", 4]),
        "timestamp": time.time(),
        "value": {
            "consumption": "1501m",
            "packml_state": "EXECUTE"
        }
    }
    return json.dumps(message)

def generate_message():
    generator = random.choice([random_cutting_machine_message, random_cleaning_machine_message])
    return generator()

# Publish MQTT messages
def publish_mqtt_message(client):
    while True:
        if (connected):
            message = generate_message()
            client.publish(topic, message)
            print(f"Published: {message}")
            time.sleep(0.5)

# Connect callback
def on_connect(client, userdata, flags, reasonCode, properties):
    if reasonCode == 0:
        print("Connected to MQTT broker")
        global connected
        connected = True
    else:
        print("Failed to connect to MQTT broker")


# MQTT client setup
client = mqtt.Client(protocol=mqtt.MQTTv5)

# Set up callbacks
client.on_connect = on_connect

# Connect to MQTT broker
client.connect(broker_address, broker_port)
client.loop_start()
while connected != True:
    time.sleep(0.1)

client.subscribe("#")
publish_mqtt_message(client)