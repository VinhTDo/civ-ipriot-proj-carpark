from mqtt_device import MqttDevice
import json
import sys


class Display(MqttDevice):
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('carpark')
        self.client.loop_forever()

    def display(self, json_data):
        print("*"*20)
        print(f"Time: {json_data['time']}")
        print(f"Available spaces: {json_data['spaces'] if json_data['spaces'] > 0 else 'FULL'}")
        print(f"Total spaces: {json_data['total-spaces']}")
        print(f"Temperature: {json_data['temperature']}℃")
        print("*"*20)

    def on_message(self, client, userdata, message):
        """This method is called when a client is published with a specified topic"""
        message_data = message.payload.decode("utf-8")
        self.display(json.loads(message_data))


if __name__ == "__main__":
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

    display = Display(config['CarParks'][0])
