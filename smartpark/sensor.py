""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
import paho.mqtt.client as paho
from smartpark.mqtt_device import MqttDevice


class Sensor(MqttDevice):
    def on_detection(self, message):
        """The method that is triggered when a detection occurs"""
        self.client.publish(self.topic, message)

    def start_sensing(self):
        """a blocking event loop that waits for detection events, in this case Enter presses"""
        while True:
            user_input = input("Press E when 🚗 enters or press X when 🚗 exits: ").strip().lower()
            if user_input == "e":
                self.on_detection("Entered")
            elif user_input == "x":
                self.on_detection("Exited")


if __name__ == '__main__':
    config = {'name': 'super sensor',
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'entry'
              }

    sensor = Sensor(config)
    print("Sensor initialized")
    sensor.start_sensing()
