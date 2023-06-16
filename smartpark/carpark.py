from mqtt_device import MqttDevice
from datetime import datetime
import json
import sys


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
        self.client.publish('carpark', message)

        try:
            handler = open(config_path, 'r')

            try:
                config_data = json.load(handler)
            except IOError:
                print("Unexpected error! Cannot perform action!")
            finally:
                handler.close()

        except FileNotFoundError:
            print(f"{config_path} doesn't exist")

        config_data['CarParks'][0]['total-cars'] = self.total_cars

        # Updates the config file
        write_handler = open(config_path, 'w')
        write_handler.write(json.dumps(config_data, indent=4))
        write_handler.close()

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
        """This method is called when a client is published with a specified topic"""
        data = message.payload.decode("utf-8").strip()
        print(f'Received: {data}')

        self.temperature = float(data.split(", ")[1])

        if 'Entered' in data:
            self.on_enter()
        elif 'Exited' in data:
            self.on_exit()


if __name__ == '__main__':
    config_path = '../config.json'

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

    carpark = Carpark(config['CarParks'][0])
