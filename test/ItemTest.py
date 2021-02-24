import unittest
from src.lib.Item import Item


class ItemTest(unittest.TestCase):
    item: Item

    def setUp(self) -> None:
        self.item = Item(100, 100, 100, 5,  "SerialNumber")

    def testGetLength(self):
        self.assertEqual(self.item.get_length(), 100)

    def testGetWidth(self):
        self.assertEqual(self.item.get_width(), 100)

    def testGetHeight(self):
        self.assertEqual(self.item.get_height(), 100)

    def testGetSize(self):
        self.assertEqual(self.item.get_size(), [100, 100, 100])

    def testGetVolume(self):
        self.assertEqual(self.item.get_volume(), 1000000)

    def testGetMass(self):
        self.assertEqual(self.item.get_mass(), 5)

    def testGetSerial(self):
        self.assertEqual(self.item.get_serial(), "SerialNumber")

    def tearDown(self) -> None:
        del self.item


if __name__ == '__main__':
    unittest.main()
