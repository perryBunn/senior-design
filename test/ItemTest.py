import unittest
from Item import Item


class ItemTest(unittest.TestCase):
    item: Item

    def setUp(self) -> None:
        self.item = Item(100, 100, 100, "SerialNumber")

    def test_something(self):
        self.assertEqual(True, False)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
