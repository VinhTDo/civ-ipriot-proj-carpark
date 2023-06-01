from mqtt_device import MqttDevice
from datetime import datetime
import random


class Carpark(MqttDevice):
    """
        Creates a carpark object to store the state of cars in the lot
    """
    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('+/+/+/+')
        self.client.loop_forever()

    @property
    def get_available_spaces(self):
        return self.total_spaces - self.total_cars

    def _publish_update(self):
        current_time = datetime.now().strftime('%H:%M')
        message = f"Time: {current_time}, Spaces: {self.get_available_spaces}, Temperature: {random.uniform(0, 40)}"
        print(message)
        self.client.publish('display', message)

    def on_enter(self):
        self.total_cars += 1 if self.total_cars < self.total_spaces else 0
        # TODO: Publish to MQTT
        self._publish_update()

    def on_exit(self):
        self.total_cars -= 1 if self.total_cars > 0 else 0
        # TODO: Publish to MQTT
        self._publish_update()

    def on_message(self, client, userdata, message):
        print(f'Received {message.payload.decode("utf-8")}')


if __name__ == '__main__':
    config = {'name': 'carpark sensor',
              'total-spaces': 140,
              'total-cars': 0,
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'entry'
              }

    carpark = Carpark(config)
    print("Carpark initialized")
