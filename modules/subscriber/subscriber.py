import paho.mqtt.client as mqtt
import os
import pickle

from schemas.event import Event

EVENT_TOPIC = "new_event"

def subscriber_client(hostname, client_id):
    def on_connect(client, userdata, flags, rc):
        print("on_connect: subscriber_module")
        client.subscribe(EVENT_TOPIC)

    def on_event(client, userdata, msg):
        """New event has been published"""
        data: Event = pickle.loads(msg.payload)
        print(f"New event: {data}")

    client = mqtt.Client(client_id)
    
    client.message_callback_add(EVENT_TOPIC, on_event)

    client.on_connect = on_connect
    client.connect(hostname)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt')


if __name__ == "__main__":
    broker = os.environ.get("MQTT_ENDPOINT", "0.0.0.0")
    subscriber_client(broker, "subscriber")
