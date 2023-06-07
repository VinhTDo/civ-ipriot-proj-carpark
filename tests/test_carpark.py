import unittest
from smartpark.carpark import Carpark


class TestCarpark(unittest.TestCase):
    def test_on_enter(self):
        config = {'name': 'carpark sensor',
                  'total-spaces': 2,
                  'total-cars': 0,
                  'location': 'L306',
                  'topic-root': "lot",
                  'broker': 'localhost',
                  'port': 1883,
                  'topic-qualifier': 'entry'
                  }

        carpark = Carpark(config)
        carpark.on_enter()
        carpark.on_enter()
        carpark.on_enter()

        self.assertEqual(carpark.get_available_spaces, 0)

    def test_on_exit(self):
        config = {'name': 'carpark sensor',
                  'total-spaces': 5,
                  'total-cars': 4,
                  'location': 'L306',
                  'topic-root': "lot",
                  'broker': 'localhost',
                  'port': 1883,
                  'topic-qualifier': 'entry'
                  }

        carpark = Carpark(config)
        carpark.on_exit()
        carpark.on_exit()
        carpark.on_exit()
        carpark.on_exit()
        carpark.on_exit()

        self.assertEqual(carpark.get_available_spaces, config['total-spaces'])


if __name__ == '__main__':
    unittest.main()
