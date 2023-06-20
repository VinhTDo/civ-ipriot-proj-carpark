""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
from mqtt_device import MqttDevice
import sys
import random
import json


class Sensor(MqttDevice):
    @property
    def temperature(self):
        return round(random.uniform(0, 40), 1)

    def on_detection(self, message):
        """The method that is triggered when a detection occurs"""
        self.client.publish('sensor', f"{message}, {self.temperature}")

    def start_sensing(self):
        """a blocking event loop that waits for detection events, in this case Enter presses"""
        while True:
            user_input = input("Press E when 🚗 enters or press X when 🚗 exits: ").strip().lower()
            if user_input == "e":
                self.on_detection("Entered")
            elif user_input == "x":
                self.on_detection("Exited")
            else:
                print("Invalid input!!!")


if __name__ == '__main__':
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

    sensor = Sensor(config['CarParks'][0])
    print("Sensor initialized")
    sensor.start_sensing()
