import random
import string
import time
import json
import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "hivemq"
broker_port = 1883
topic = "factory"
connected = False

cutting_machine_ids = set()
cleaning_machine_ids = set()
for i in range(100):
    cutting_machine_ids.add("clean-" + ''.join(random.choice(string.ascii_letters) for _ in range(10)))
    cleaning_machine_ids.add("cut-" + ''.join(random.choice(string.ascii_letters) for _ in range(10)))


# this function intentionally may generate invalid version numbers to break the
# schema of MQTT messages
def generate_faulty_version_number():
    return random.choice(["1", "2", "3", "4", 4.5, "5"])


def random_cutting_machine_message():
    message = {
        "id": random.choice(list(cutting_machine_ids)),
        "type": "cutting-machine",
        "version": generate_faulty_version_number(),
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
        # breaking the version number is intended since we want to have invalid MQTT messages
        "version": generate_faulty_version_number(),
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
def publish_mqtt_message(client, factories):
    while True:
        if connected:
            for factory in factories:
                message = generate_message()
                client.publish(f"{topic}/{factory}", message)
                print(f"Published: {message}")
            time.sleep(0.5)


# Connect callback
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker")
        global connected
        connected = True
    else:
        print("Failed to connect to MQTT broker")


if __name__ == '__main__':
    # MQTT client setup
    client = mqtt.Client(protocol=mqtt.MQTTv5)

    # Set up callbacks
    client.on_connect = on_connect

    # Connect to MQTT broker
    client.connect(broker_address, broker_port)
    client.loop_start()
    while not connected:
        time.sleep(0.1)

    client.subscribe("#")
    factories = ["factoryA", "factoryB"]
    publish_mqtt_message(client, factories)
