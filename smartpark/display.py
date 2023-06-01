from mqtt_device import MqttDevice
import time


class Display(MqttDevice):
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.client.loop_forever()

    def display(self, *args):
        print("*"*20)

        for value in args:
            print(value)
            time.sleep(1)

        print("*"*20)

    def on_message(self, client, userdata, message):
        data = message.payload.decode("utf-8")
        self.display(*data.split(','))


if __name__ == "__main__":
    config = {'name': 'carpark display',
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'na'
              }

    display = Display(config)
