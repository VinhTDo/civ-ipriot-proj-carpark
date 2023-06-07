from smartpark.mqtt_device import MqttDevice
from datetime import datetime
import json


class Carpark(MqttDevice):
    """
        Creates a carpark object to store the state of cars in the lot
    """
    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self._temperature = None
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.loop_forever()

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value

    @property
    def available_spaces(self):
        """
            Gets the difference of total spaces and total cars.
            Return: int
        """
        return self.total_spaces - self.total_cars

    def _publish_update(self):
        """
            Publish data to MQTT
        """
        current_time = datetime.now().strftime("%H:%M")

        data = {
            'time': current_time,
            'temperature': self.temperature,
            'spaces': self.available_spaces,
            'total-spaces': self.total_spaces
        }
        message = json.dumps(data)
        print(message)
        self.client.publish('carpark', message)

    def on_enter(self):
        """
            Increase total cars if there's at least one empty space, then publish data to MQTT
        """
        self.total_cars += 1 if self.total_cars < self.total_spaces else 0
        # TODO: Publish to MQTT
        self._publish_update()

    def on_exit(self):
        """
            Decrease total cars if there's at least one car, then publish data to MQTT
        """
        self.total_cars -= 1 if self.total_cars > 0 else 0
        # TODO: Publish to MQTT
        self._publish_update()

    def on_message(self, client, userdata, message):
        data = message.payload.decode("utf-8").strip()
        print(f'Received {data}')

        self.temperature = float(data.split(", ")[1])

        if 'Entered' in data:
            self.on_enter()
        elif 'Exited' in data:
            self.on_exit()


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
