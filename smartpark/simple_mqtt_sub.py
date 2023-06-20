import paho.mqtt.client as paho
import json

BROKER, PORT = "localhost", 1883


def on_message(client, userdata, message):
    data_text = message.payload.decode("utf-8")
    data = json.loads(data_text)

    print(f"Received data: {data}")


client = paho.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe("carpark")
client.loop_forever()
