from datetime import datetime
import paho.mqtt.client as paho
import json
import sys
import random

BROKER, PORT = "localhost", 1883

client = paho.Client()
client.connect(BROKER, PORT)

try:
    handler = open('../config.json', 'r')
    try:
        config = json.load(handler)
    except IOError:
        print("Something went wrong with this process!!!")
    finally:
        handler.close()
except FileNotFoundError:
    print("config.json doesn't exists!!!")

if not config:
    print("Error!!! Cannot proceed!")
    sys.exit()

total_spaces = config['CarParks'][0]['total-spaces']
total_cars = config['CarParks'][0]['total-cars']
spaces = total_spaces - total_cars

data = {
    'time': datetime.now().strftime("%H:%M"),
    'temperature': round(random.uniform(0, 40), 1),
    'spaces': spaces,
    'total-spaces': total_spaces
}

print(f"Publish data: {data}")
client.publish("carpark", json.dumps(data))

