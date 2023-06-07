from smartpark.mqtt_device import MqttDevice
import json


class Display(MqttDevice):
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('carpark')
        self.client.loop_forever()

    def display(self, json_data):
        print("*"*20)

        print(f"Time: {json_data['time']}")
        print(f"Available spaces: {json_data['spaces']}")
        print(f"Total spaces: {json_data['total-spaces']}")
        print(f"Temperature: {json_data['temperature']}℃")

        print("*"*20)

    def on_message(self, client, userdata, message):
        data = message.payload.decode("utf-8")
        self.display(json.loads(data))


if __name__ == "__main__":
    config = {'name': 'carpark display',
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'na'
              }

    display = Display(config)
