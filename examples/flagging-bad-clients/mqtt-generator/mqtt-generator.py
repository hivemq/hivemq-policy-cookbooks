import random
import string
import time
import json
import uuid
import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "hivemq"

broker_port = 1883
topic = "factory"
connected = {}

# generates 10 random UUIDs
number_of_clients = 10
client_ids = list(map(lambda _: str(uuid.uuid4()), [""] * number_of_clients))

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


def select_client(clients):
    return random.sample(list(clients), 1)[0]


# Publish MQTT messages
def publish_mqtt_message(clients, factories):
    while True:
        for factory in factories:
            message = generate_message()
            client_obj = select_client(clients)
            client = client_obj['connection']

            if connected[client_obj['client_id']]:
                client.publish(f"{topic}/{factory}", message)
                print(f"Published {client_obj['client_id']} : {message}")
            else:
                print(f"Client {client_obj['client_id']} offline ")
        time.sleep(0.5)

# Connect callback

def get_on_connect(client_id):
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("Connected to MQTT broker")
            # global connected
            connected[client_id] = True
        else:
            print("Failed to connect to MQTT broker")

    return on_connect


def connect(client_id):
    # MQTT client setup
    client = mqtt.Client(protocol=mqtt.MQTTv5, client_id=client_id)

    # Set up callbacks
    client.on_connect = get_on_connect(client_id)

    # Connect to MQTT broker
    client.connect(broker_address, broker_port)
    client.loop_start()
    while client_id not in connected:
        print(f"Waiting for {client_id}")
        time.sleep(0.1)

    return client


if __name__ == '__main__':
    clients = list(map(lambda client_id: {"connection": connect(client_id), "client_id": client_id}, client_ids))

    factories = ["factoryA", "factoryB"]
    print("Start")
    publish_mqtt_message(clients, factories)
