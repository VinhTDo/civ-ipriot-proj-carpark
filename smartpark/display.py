from smartpark.mqtt_device import MqttDevice
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
        message_data = message.payload.decode("utf-8")
        self.display(json.loads(message_data))


if __name__ == "__main__":
    config_path = '../config.json'
    config = None

    try:
        handler = open(config_path, 'r')
        try:
            config = json.load(handler)
        except IOError:
            print("Something went wrong with this process!!!")
        finally:
            handler.close()
    except FileNotFoundError:
        print(f"{config_path} doesn't exists!!!")

    if not config:
        print("Error!!! Cannot proceed!")
        sys.exit()

    print(config)

    display = Display(config['CarParks'][0])
