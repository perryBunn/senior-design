import unittest
from Container import Container
from Item import Item


class ContItemIntegration(unittest.TestCase):
    container: Container
    item: Item

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, 100, 100, 100)
        self.item = Item(100, 100, 100, "SerialNumber")

    def test_something(self):
        self.assertEqual(True, False)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
