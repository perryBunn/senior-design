import unittest

from src.lib.Container import Container
from src.lib.Item import Item
from src.palletize import *


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, [0, 0, 0], 30, 20, 100)

    def testOrient_1(self):
        item = Item(15, 10, 5, 5, "1")
        res = orient(item, self.container)
        self.assertEqual(item.get_size(), res.get_size())

    def testOrient_2(self):
        item = Item(10, 15, 5, 5, "1")
        res = orient(item, self.container)
        self.assertEqual([15, 10, 5], res.get_size())

    def testOrient_3(self):
        item = Item(7, 7, 5, 5, "1")
        res = orient(item, self.container)
        self.assertEqual([7, 7, 5], res.get_size())

    def tearDown(self) -> None:
        del self.container


if __name__ == '__main__':
    unittest.main()
