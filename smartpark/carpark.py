from smartpark.mqtt_device import MqttDevice


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

    def on_enter(self):
        self.total_cars += 1 if self.total_cars < self.total_spaces else 0
        # TODO: Publish to MQTT

    def on_exit(self):
        self.total_cars -= 1 if self.total_cars > 0 else 0
        # TODO: Publish to MQTT

    def on_message(self, client, userdata, msg):
        print(f'Received {msg.payload.decode()}')


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
